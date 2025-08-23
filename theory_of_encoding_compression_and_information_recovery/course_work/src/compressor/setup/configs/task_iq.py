from pydantic import BaseModel


class TaskIQConfig(BaseModel):
    default_retry_count: int = 5
    default_delay: int = 10
    use_jitter: bool = True
    use_delay_exponent: bool = True
    max_delay_exponent: int = 120
    durable_queue: bool = True
    durable_exchange: bool = True
    declare_exchange: bool = True