import logging

from common.config import settings
from common.events import ORDER_CREATED, PAYMENT_APPROVED

logger = logging.getLogger(__name__)

REASONS = {
    "LIMIT_EXCEEDED": "valor acima do limite permitido",
    "SOLD_OUT": "ingressos esgotados",
}


class NotificationService:
    def __init__(self, repository):
        self.repository = repository

    def notify(self, key, event):
        message = self.compose(key, event)
        self.repository.save(event.order_id, key, message)
        logger.info("email to %s: %s", event.customer_email, message)

    def compose(self, key, event):
        name = event.customer_name
        if key == ORDER_CREATED:
            return (
                f"Olá, {name}! Recebemos seu pedido de {event.quantity} "
                f"ingresso(s) {event.ticket_type} no {settings.project_name} "
                f"e já estamos processando."
            )
        if key == PAYMENT_APPROVED:
            return f"Pagamento aprovado, {name}! Seus ingressos estão confirmados."
        reason = REASONS.get(event.reason, "não foi possível concluir o pagamento")
        return f"Pagamento recusado, {name}: {reason}."
