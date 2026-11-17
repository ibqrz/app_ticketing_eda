from common.events import STOCK_RESERVED
from common.messaging.publisher import EventPublisher

EventPublisher().publish(STOCK_RESERVED, {"order_id": "invalido", "quantity": "abc"})
print("mensagem invalida publicada em stock.reserved")
