from common.logger import setup_logging
from common.messaging.consumer import Consumer
from common.messaging.publisher import EventPublisher
from common.messaging.topology import PAYMENT_QUEUE
from controllers.payment import PaymentController
from repositories.payment import PaymentRepository
from services.payment import PaymentService


def main():
    setup_logging()
    repository = PaymentRepository()
    service = PaymentService(repository, EventPublisher())
    controller = PaymentController(service)
    Consumer(PAYMENT_QUEUE, controller.handle).run()


if __name__ == "__main__":
    main()
