from abc import ABC, abstractmethod

from app.domain.entities.body import BodyOfEmailEntity
from app.domain.values.mail import TemplateName


class BaseTemplateRenderer(ABC):
    @abstractmethod
    def render(
            self,
            template_name: TemplateName,
            body: BodyOfEmailEntity
    ) -> str:
        """
        Renders an HTML template with the specified context.
        :param template_name: Template name (e.g., "verification_email.html")
        :param body: Data for the template (e.g. {"name": "John", "link": "..."})
        :return: HTML content as a string
        """
        raise NotImplementedError
