from abc import ABC, abstractmethod
from typing import Any

from app.domain.values.mail import TemplateName


class BaseTemplateRenderer(ABC):
    @abstractmethod
    def render(self, template_name: TemplateName, context: dict[str, Any]) -> str:
        """
        Renders an HTML template with the specified context.
        :param template_name: Template name (e.g., "verification_email.html")
        :param context: Data for the template (e.g. {"name": "John", "link": "..."})
        :return: HTML content as a string
        """
        raise NotImplementedError
