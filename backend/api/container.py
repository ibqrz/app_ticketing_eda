from common.config import settings
from common.messaging.publisher import EventPublisher
from repositories.orders import OrderRepository
from repositories.sessions import SessionRepository
from repositories.tickets import TicketRepository
from repositories.users import UserRepository
from services.account import AccountService
from services.attachments import AttachmentService
from services.auth import AuthService
from services.orders import OrderService
from services.tickets import TicketService

users = UserRepository()
auth_service = AuthService(users, SessionRepository())
account_service = AccountService(users)
attachments = AttachmentService(settings.attachments_dir)
ticket_service = TicketService(TicketRepository(), attachments)
order_service = OrderService(OrderRepository(), ticket_service, EventPublisher(), attachments)