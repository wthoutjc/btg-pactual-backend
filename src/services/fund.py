from src.schemas.user import NotifyType
from src.models.fund import Fund
from src.repositories.fund import FundRepository
from src.repositories.user import UserRepository
from src.repositories.transaction import TransactionRepository
from src.schemas.transaction import TransactionOut, TransactionType, Transaction, TransactionCreate, TransactionType
from src.services.email import EmailService
from src.services.whatsapp import WhatsappService
from typing import List

class FundService:
    def __init__(self,
            fund_repository: FundRepository,
            user_repository: UserRepository,
            transaction_repository: TransactionRepository,
            email_service:EmailService,
            whatsapp_service:WhatsappService
        ) -> None:
        self.fund_repository = fund_repository
        self.user_repository = user_repository
        self.transaction_repository = transaction_repository
        self.email_service = email_service
        self.whatsapp_service = whatsapp_service

    def __notify_user__(self, user: dict, fund: Fund):
        notify = user["notify"]
        message = f"Hola {user['name']}, se ha suscrito al fondo {fund['name']} por un monto de {fund['minimum_amount']}"

        if notify["type"] == NotifyType.EMAIL:
            self.email_service.send_email(to=notify["value"], message_str=message)
        elif notify["type"] == NotifyType.SMS:
            self.whatsapp_service.send_message(user, fund)

    def get_funds(self) -> List[Fund]:
        return self.fund_repository.get_funds()

    def subscribe(self, transaction_create: TransactionCreate) -> TransactionOut:
        fund = self.fund_repository.get_fund_by_id(transaction_create.fund_id)
        if not fund:
            raise ValueError("Fund not found")

        user = self.user_repository.get()
        if not user:
            raise ValueError("User not found")

        last_transaction = self.transaction_repository.get_last_transaction_by_user_id(user['id'])

        if last_transaction and last_transaction['transaction_type'] == TransactionType.SUBSCRIBE.value:
            raise ValueError(f"Ya tiene una suscripción activa al fondo {fund['name']}")

        amount = float(user["amount"])
        minimum_amount = float(fund["minimum_amount"])

        if amount < minimum_amount:
            raise ValueError(f"No tiene saldo disponible para vincularse al fondo {fund['name']}")

        new_amount = float(amount- minimum_amount)
        self.user_repository.update_user_amount(user['id'], new_amount)

        transaction = Transaction(
            user_id=user['id'],
            fund_id=fund['id'],
            amount=minimum_amount,
            transaction_type=TransactionType.SUBSCRIBE.value
        )

        self.__notify_user__(user, fund)
        return self.transaction_repository.create_transaction(transaction)

    def unsubscribe(self, fund_id: str) -> TransactionOut:
        fund = self.fund_repository.get_fund_by_id(fund_id)
        if not fund:
            raise ValueError("Fund not found")

        user = self.user_repository.get()

        amount = float(user["amount"])
        minimum_amount = float(fund["minimum_amount"])

        last_transaction = self.transaction_repository.get_last_transaction_by_user_id(user['id'])

        if not last_transaction or last_transaction['transaction_type'] != TransactionType.SUBSCRIBE.value:
            raise ValueError(f"No tiene una suscripción activa al fondo {fund['name']}")

        new_amount = float(amount + minimum_amount)
        self.user_repository.update_user_amount(user['id'], new_amount)

        transaction = Transaction(
            user_id=user['id'],
            fund_id=fund_id,
            amount=minimum_amount,
            transaction_type=TransactionType.UNSUBSCRIBE.value
        )
        return self.transaction_repository.create_transaction(transaction)
