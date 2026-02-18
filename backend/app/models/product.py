import uuid
from decimal import Decimal
from datetime import datetime, timezone

from sqlalchemy import String, Text, DateTime, Numeric, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    tenant_id: Mapped[str] = mapped_column(String, index=True, nullable=False)

    nome: Mapped[str] = mapped_column(String, nullable=False)
    descricao_original: Mapped[str] = mapped_column(Text, nullable=False)
    descricao_melhorada: Mapped[str] = mapped_column(Text, nullable=False)

    valor_produto: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    valor_comissao: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    margem_percentual: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)


    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
)



