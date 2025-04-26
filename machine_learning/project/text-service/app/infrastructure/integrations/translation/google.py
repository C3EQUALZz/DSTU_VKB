from typing import override

from deep_translator import GoogleTranslator

from app.domain.entities.message import TextMessageEntity
from app.domain.values.message import Text
from app.infrastructure.integrations.translation.base import Translator


class GoogleTranslation(Translator):
    @override
    async def translate_message(self, source: str, target: str, message: TextMessageEntity) -> TextMessageEntity:
        translator = GoogleTranslator(source=source, target=target)
        translated_string: str = translator.translate(message.content.as_generic_type())
        return TextMessageEntity(Text(translated_string))

    def translate_file(self, file):
        ...
