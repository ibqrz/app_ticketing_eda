from common.logger import setup_logging
from common.messaging.consumer import Consumer
from common.messaging.publisher import EventPublisher
from common.messaging.topology import INVENTORY_QUEUE
from controllers.inventory import InventoryController
from repositories.inventory import InventoryRepository
from services.inventory import InventoryService


def main():
    setup_logging()
    repository = InventoryRepository()
    service = InventoryService(repository, EventPublisher())
    controller = InventoryController(service)
    Consumer(INVENTORY_QUEUE, controller.handle).run()


if __name__ == "__main__":
    main()
