from abc import ABC, abstractmethod

from app.domain.entities.mail import EmailEntity


class BaseMailSender(ABC):
    """
    Interface for class to sending emails
    """

    @abstractmethod
    async def send_message(self, email_entity: EmailEntity) -> None:
        """
        Method to send emails.
        :param email_entity: Domain entity which describes email
        :return: Nothing
        """
        raise NotImplementedError
