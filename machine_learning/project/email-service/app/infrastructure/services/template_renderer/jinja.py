from typing import Final, override

from jinja2 import Environment

from app.domain.entities.body import BodyOfEmailEntity
from app.domain.values.mail import TemplateName
from app.infrastructure.services.template_renderer.base import BaseTemplateRenderer


class Jinja2TemplateRenderer(BaseTemplateRenderer):
    def __init__(self, env: Environment) -> None:
        self._env: Final[Environment] = env

    @override
    def render(self, template_name: TemplateName, body: BodyOfEmailEntity) -> str:
        template = self._env.get_template(template_name.as_generic_type())
        return template.render(body.to_dict(save_classes_value_objects=False))
