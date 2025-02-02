from src.schemas.user import NotifyType
from src.models.fund import Fund
from src.schemas.fund import FundOut
from src.repositories.fund import FundRepository
from src.repositories.user import UserRepository
from src.repositories.transaction import TransactionRepository
from src.schemas.transaction import TransactionOut, TransactionType, Transaction, TransactionCreate, TransactionType
from src.services.email import EmailService
from src.services.whatsapp import WhatsappService
from typing import List
from datetime import datetime

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

    def _notify_user(self, user: dict, fund: Fund, transaction: Transaction) -> None:
        notify = user["notify"]
        message = f"Hola {user['name']}, se ha suscrito al fondo {fund['name']} por un monto de {fund['minimum_amount']}"

        if notify["type"] == NotifyType.EMAIL:
            self.email_service.send_email(to=notify["value"], message_str=message)
        elif notify["type"] == NotifyType.SMS:
            self.whatsapp_service.send_message(user, fund, transaction)

    def get_funds(self) -> List[FundOut]:
        funds = self.fund_repository.get_funds()
        for fund in funds:
            last_transaction = self.transaction_repository.get_last_transaction_by_fund_id(fund['id'])
            fund['last_transaction'] = last_transaction
        return funds

    def subscribe(self, transaction_create: TransactionCreate) -> TransactionOut:
        fund = self.fund_repository.get_fund_by_id(transaction_create.fund_id)
        if not fund:
            raise ValueError("Fund not found")

        user = self.user_repository.get()
        if not user:
            raise ValueError("User not found")

        last_transaction = self.transaction_repository.get_last_transaction_by_user_id(user['id'])

        if last_transaction and last_transaction['transaction_type'] == TransactionType.SUBSCRIBE.value and last_transaction['fund_id'] == fund['id']:
            raise ValueError(f"Ya tiene una suscripción activa al fondo {fund['name']}")

        user_amount = float(user["amount"])
        sub_amount = float(transaction_create.amount)
        minimum_amount = float(fund["minimum_amount"])

        if sub_amount < minimum_amount:
            raise ValueError(f"El monto mínimo para suscribirse al fondo {fund['name']} es de {minimum_amount}")

        if user_amount < minimum_amount or sub_amount > user_amount:
            raise ValueError(f"No tiene saldo disponible para vincularse al fondo {fund['name']} con un monto de {sub_amount}")

        new_amount = float(user_amount - sub_amount)
        self.user_repository.update_user_amount(user['id'], new_amount)

        transaction = self.transaction_repository.create_transaction(Transaction(
            user_id=user['id'],
            fund_id=fund['id'],
            amount=sub_amount,
            transaction_type=TransactionType.SUBSCRIBE.value,
            created_at=datetime.now()
        ))

        self._notify_user(user, fund, transaction)

        return TransactionOut(
            id=str(transaction.id),
            fund=fund,
            amount=sub_amount,
            transaction_type=TransactionType.SUBSCRIBE,
            created_at=transaction.created_at
        )

    def unsubscribe(self, fund_id: str) -> TransactionOut:
        fund = self.fund_repository.get_fund_by_id(fund_id)
        if not fund:
            raise ValueError("Fund not found")

        user = self.user_repository.get()

        last_transaction = self.transaction_repository.get_last_transaction_by_fund_id(fund['id'])

        # Si no existe una última transacción o la última transacción no es una suscripción al fondo
        if (not last_transaction or last_transaction['transaction_type'] != TransactionType.SUBSCRIBE.value):
            raise ValueError(f"No tiene una suscripción activa al fondo {fund['name']}")

        amount = float(user["amount"])
        minimum_amount = float(fund["minimum_amount"])
        transaction_amount = float(last_transaction["amount"])

        new_amount = float(amount + transaction_amount)
        self.user_repository.update_user_amount(user['id'], new_amount)

        transaction = self.transaction_repository.create_transaction(Transaction(
            user_id=user['id'],
            fund_id=fund_id,
            amount=transaction_amount,
            transaction_type=TransactionType.UNSUBSCRIBE.value,
            created_at=datetime.now()
        ))

        return TransactionOut(
            id=str(transaction.id),
            fund=fund,
            amount=minimum_amount,
            transaction_type=TransactionType.UNSUBSCRIBE,
            created_at=transaction.created_at
        )
