from typing import Final

from faststream.rabbit import RabbitExchange, ExchangeType

USER_EXCHANGE: Final[RabbitExchange] = RabbitExchange(
    "user_exchange",
    auto_delete=True,
    type=ExchangeType.TOPIC,
)


