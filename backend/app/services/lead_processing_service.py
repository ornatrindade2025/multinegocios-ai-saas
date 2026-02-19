import uuid
from decimal import Decimal, ROUND_HALF_UP
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from asyncio import to_thread

from app.models.lead import Lead
from app.models.product import Product
from app.schemas.processing import LeadProcessingResult
from app.ai.crew_lead_processor import run_lead_processing

from app.core.security.validation import sanitize_text
from app.core.security.audit import log_event
from app.core.security.rate_limit import rate_limiter
from app.core.security.exceptions import (
    ValidationError,
)


class LeadProcessingService:

    async def process_lead(
        self,
        db: AsyncSession,
        tenant_id: str,
        lead_id: uuid.UUID,
    ) -> LeadProcessingResult:

        log_event(
            tenant_id,
            "lead_processing_started",
            {"lead_id": str(lead_id)},
        )

        try:

            # Buscar lead isolado por tenant
            lead_stmt = select(Lead).where(
                Lead.id == lead_id,
                Lead.tenant_id == tenant_id,
            )

            lead_result = await db.execute(lead_stmt)
            lead = lead_result.scalar_one_or_none()

            if not lead:
                raise ValidationError("Lead not found")

            # Sanitizar input
            sanitized_text = sanitize_text(lead.descricao_original)

            # Buscar produtos do tenant
            product_stmt = select(Product).where(
                Product.tenant_id == tenant_id
            )

            product_result = await db.execute(product_stmt)
            products: List[Product] = list(product_result.scalars().all())

            if not products:
                raise ValidationError("No products available")

            product_dicts = [
                {
                    "id": str(p.id),
                    "nome": p.nome,
                    "valor_produto": p.valor_produto,
                    "margem_percentual": p.margem_percentual,
                }
                for p in products
            ]

            # Rate limit antes da AI
            rate_limiter.check(tenant_id)

            ai_result = await to_thread(
                run_lead_processing,
                sanitized_text,
                product_dicts,
            )

            if not isinstance(ai_result, dict):
                raise ValidationError("Invalid AI response")

            produto_id = ai_result.get("produto_id")
            descricao_melhorada = ai_result.get("descricao_melhorada")

            # Conversão segura
            try:
                confianca = float(ai_result.get("confianca", 0))
            except (TypeError, ValueError):
                confianca = 0.0

            justificativa = ai_result.get("justificativa", "")

            if not produto_id or not descricao_melhorada:
                raise ValidationError("AI returned incomplete data")

            # Sanitizar output AI
            descricao_melhorada = sanitize_text(descricao_melhorada)

            selected_product = next(
                (p for p in products if str(p.id) == str(produto_id)),
                None,
            )

            if not selected_product:
                raise ValidationError("AI selected invalid product")

            margem = selected_product.margem_percentual
            valor_produto = selected_product.valor_produto

            valor_comissao = (
                valor_produto * (margem / Decimal(100))
            ).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )

            log_event(
                tenant_id,
                "lead_processing_completed",
                {
                    "lead_id": str(lead_id),
                    "produto_id": str(selected_product.id),
                    "confianca": confianca,
                },
            )

            return LeadProcessingResult(
                lead_id=lead.id,
                descricao_original=lead.descricao_original,
                descricao_melhorada=descricao_melhorada,
                produto_id=selected_product.id,
                produto_nome=selected_product.nome,
                valor_produto=valor_produto,
                valor_comissao=valor_comissao,
                margem_percentual=margem,
                confianca=confianca,
                justificativa_ai=justificativa,
            )

        except Exception as e:

            log_event(
                tenant_id,
                "lead_processing_error",
                {
                    "lead_id": str(lead_id),
                    "error": str(e),
                },
            )

            raise
