import logging
from typing import Any

logger = logging.getLogger("audit")

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

logger.setLevel(logging.INFO)


def log_event(
    tenant_id: str,
    event: str,
    metadata: dict[str, Any] | None = None,
) -> None:

    logger.info(
        {
            "tenant_id": tenant_id,
            "event": event,
            "metadata": metadata or {},
        }
    )
