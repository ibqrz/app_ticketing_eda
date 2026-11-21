import os
import socket
from decimal import Decimal


class Settings:
    def __init__(self):
        self.project_name = os.getenv("PROJECT_NAME", "Voucher")
        self.database_url = os.environ["DATABASE_URL"]
        self.rabbitmq_url = os.environ["RABBITMQ_URL"]
        self.payment_limit = Decimal(os.getenv("PAYMENT_LIMIT", "5000.00"))
        self.processing_delay = float(os.getenv("PROCESSING_DELAY", "2"))
        self.prefetch = int(os.getenv("PREFETCH_COUNT", "1"))
        self.sold_out_ttl_hours = float(os.getenv("SOLD_OUT_TTL_HOURS", "24"))
        self.session_days = int(os.getenv("SESSION_DAYS", "7"))
        self.attachments_dir = os.getenv("ATTACHMENTS_DIR", "/app/attachmentsProcess")
        self.cors_origins = [
            origin.strip()
            for origin in os.getenv("CORS_ORIGINS", "http://localhost:8080").split(",")
        ]
        self.instance_id = socket.gethostname()


settings = Settings()
