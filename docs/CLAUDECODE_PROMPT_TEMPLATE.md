Estamos no projeto MultiNegócios AI SaaS.

Arquitetura obrigatória:
- FastAPI async
- SQLAlchemy async
- Service layer puro
- Multi-tenant obrigatório
- Toda query deve conter tenant_id
- Sem overengineering
- Sem microservices
- Async safe
- Tipagem forte
- Código auditável
- Segurança obrigatória

Não colocar lógica no controller.
Não criar abstrações desnecessárias.
Não adicionar dependências externas sem justificativa.