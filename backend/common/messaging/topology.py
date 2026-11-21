from common.events import (
    ORDER_CREATED,
    PAYMENT_APPROVED,
    PAYMENT_REFUSED,
    STOCK_RESERVED,
    STOCK_SOLD_OUT,
    TICKET_REFUND_REQUESTED,
    TICKET_REFUNDED,
)

EXCHANGE = "tickets.events"
DEAD_EXCHANGE = "tickets.dlx"
DEAD_QUEUE = "tickets.dlq"
DEAD_KEY = "dead"

INVENTORY_QUEUE = "inventory.queue"
PAYMENT_QUEUE = "payment.queue"
NOTIFICATION_QUEUE = "notification.queue"

BINDINGS = {
    INVENTORY_QUEUE: [ORDER_CREATED, PAYMENT_APPROVED, PAYMENT_REFUSED, TICKET_REFUND_REQUESTED],
    PAYMENT_QUEUE: [STOCK_RESERVED, STOCK_SOLD_OUT],
    NOTIFICATION_QUEUE: [ORDER_CREATED, PAYMENT_APPROVED, PAYMENT_REFUSED, TICKET_REFUNDED],
}


def declare_topology(channel):
    channel.exchange_declare(exchange=EXCHANGE, exchange_type="topic", durable=True)
    channel.exchange_declare(exchange=DEAD_EXCHANGE, exchange_type="direct", durable=True)
    channel.queue_declare(queue=DEAD_QUEUE, durable=True)
    channel.queue_bind(queue=DEAD_QUEUE, exchange=DEAD_EXCHANGE, routing_key=DEAD_KEY)
    arguments = {
        "x-dead-letter-exchange": DEAD_EXCHANGE,
        "x-dead-letter-routing-key": DEAD_KEY,
    }
    for queue, keys in BINDINGS.items():
        channel.queue_declare(queue=queue, durable=True, arguments=arguments)
        for key in keys:
            channel.queue_bind(queue=queue, exchange=EXCHANGE, routing_key=key)