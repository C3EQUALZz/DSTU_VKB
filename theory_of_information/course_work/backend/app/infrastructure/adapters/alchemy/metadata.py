from sqlalchemy import MetaData
from sqlalchemy.orm import registry

metadata: MetaData = MetaData()
mapper_registry: registry = registry(metadata=metadata)
