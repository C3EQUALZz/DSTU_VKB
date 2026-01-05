import re
from dataclasses import dataclass
from typing import Final
from typing_extensions import override

from chat_service.domain.chat.errors import EmptyContentMessageError, RussianSwearWordsMessageError
from chat_service.domain.common.values.base import BaseValueObject

RUSSIAN_SWEAR_WORDS_PATTERN: Final[re.Pattern[str]] = re.compile(
    "(?iu)(?<![а-яё])(?:(?:(?:у|[нз]а|(?:хитро|не)?вз?[ыьъ]|с[ьъ]|(?:и|ра)[зс]ъ?|(?:о[тб]|п[оа]д)[ьъ]?|(?:\S(?=[а-яё]))"
    "+?[оаеи-])-?)?(?:[её](?:б(?!о[рй]|рач)|п[уа](?:ц|тс))|и[пб][ае][тцд][ьъ]).*?|(?:(?:н[иеа]|(?:ра|и)[зс]|[зд]?[ао]"
    "(?:т|дн[оа])?|с(?:м[еи])?|а[пб]ч|в[ъы]?|пр[еи])-?)?ху(?:[яйиеёю]|л+и(?!ган)).*?|бл(?:[эя]|еа?)(?:[дт][ьъ]?)?|\S*?"
    "(?:п(?:[иеё]зд|ид[аое]?р|ед(?:р(?!о)|[аое]р|ик)|охую)|бля(?:[дбц]|тс)|[ое]ху[яйиеё]|хуйн).*?|(?:о[тб]?|про|на|вы)"
    "?м(?:анд(?:[ауеыи](?:л(?:и[сзщ])?[ауеиы])?|ой|[ао]в.*?|юк(?:ов|[ауи])?|е[нт]ь|ища)|уд(?:[яаиое].+?|е?н"
    "(?:[ьюия]|ей))|[ао]л[ао]ф[ьъ](?:[яиюе]|[еёо]й))|елд[ауые].*?|ля[тд]ь|(?:[нз]а|по)х)(?![а-яё])"
)


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class MessageContent(BaseValueObject):
    value: str

    @override
    def _validate(self) -> None:
        if (
                self.value.isspace()
                or self.value.strip() == ""
                or len(self.value) == 0
        ):
            raise EmptyContentMessageError("message content can't be empty")

        if RUSSIAN_SWEAR_WORDS_PATTERN.match(self.value):
            raise RussianSwearWordsMessageError("Russian swear words occurred")

    @override
    def __str__(self) -> str:
        return self.value
