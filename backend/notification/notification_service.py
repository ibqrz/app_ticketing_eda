from common.logger import setup_logging
from common.messaging.consumer import Consumer
from common.messaging.topology import NOTIFICATION_QUEUE
from controllers.notification import NotificationController
from repositories.notification import NotificationRepository
from services.notification import NotificationService


def main():
    setup_logging()
    repository = NotificationRepository()
    service = NotificationService(repository)
    controller = NotificationController(service)
    Consumer(NOTIFICATION_QUEUE, controller.handle).run()


if __name__ == "__main__":
    main()