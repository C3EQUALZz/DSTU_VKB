from typing import Any, Optional, Dict, Union

from aiogram_dialog.api.internal import TextWidget
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text
from aiogram_i18n import I18nContext
from magic_filter import MagicFilter

I18N_FORMAT_KEY = "i18n"


class I18NFormat(Text):
    def __init__(
        self,
        text: str,
        locale: Optional[Union[TextWidget, MagicFilter, str]] = None,
        when: Optional[WhenCondition] = None,
        /,
        **mapping: Union[TextWidget, MagicFilter, str, int, float, bool],
    ) -> None:
        super().__init__(when)
        self.text = text
        self.locale = locale
        self.mapping = mapping

    @staticmethod
    async def _resolve(
        value: Union[TextWidget, MagicFilter, str, int, float, bool], data: dict, manager: DialogManager
    ) -> Any:
        if isinstance(value, TextWidget):
            return await value.render_text(data, manager)
        if isinstance(value, MagicFilter):
            return value.resolve(data)
        return value

    async def _transform(self, data: dict, manager: DialogManager) -> Dict[str, Any]:
        transformed_data = {}
        for key, val in self.mapping.items():
            resolved_val = await self._resolve(val, data, manager)
            transformed_data[key] = "" if resolved_val is None else resolved_val  # Fluent does not support None
        return transformed_data

    async def _render_text(self, data: dict, manager: DialogManager) -> str:
        i18n: Optional[I18nContext] = manager.middleware_data.get(I18N_FORMAT_KEY)
        if i18n is None:
            raise ValueError("I18nContext not found in manager.middleware_data")

        transformed_data = await self._transform(data, manager)
        locale_str = await self._resolve(self.locale, data, manager) if self.locale else None

        return i18n.get(self.text, locale_str, **transformed_data)