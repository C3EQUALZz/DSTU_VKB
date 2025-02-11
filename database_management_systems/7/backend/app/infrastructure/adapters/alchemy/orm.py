import uuid

from sqlalchemy import Column, String, Numeric, Table, UUID, VARCHAR, Computed, Date, CheckConstraint, ForeignKey, Index, INTEGER
from sqlalchemy.dialects.postgresql import TSTZRANGE

from app.infrastructure.adapters.alchemy.metadata import metadata, mapper_registry

position_of_master = Table(
    'position_of_master',
    metadata,
    Column('oid', UUID, primary_key=True, default=uuid.uuid4),
    Column('position', VARCHAR(30), unique=True),
    Column(TSTZRANGE, nullable=False, default="tsrange(current_timestamp, NULL)")
)

order_fulfillment_table = Table(
    'order_fulfillment',
    metadata,
    Column('oid', UUID, primary_key=True, default=uuid.uuid4),
    Column('type_of_work', VARCHAR(50), nullable=False),
    Column('cost', Numeric(10, 2), nullable=False),
    Column('cost_of_components', Numeric(10, 2), nullable=False),
    Column('total_cost', Numeric(10, 2), Computed('cost + COALESCE(cost_of_components, 0)', persisted=True)),
    Column('fulfillment_date', Date, nullable=False),
    CheckConstraint("fulfillment_date > '1980-01-01'", name='check_fulfillment_date')
)

status_of_booking_table = Table(
    'status_of_booking',
    metadata,
    Column('oid', UUID, primary_key=True, default=uuid.uuid4),
    Column('name', VARCHAR(50), nullable=False, unique=True),
)

equipment_table = Table(
    'equipment',
    metadata,
    Column('oid', UUID, primary_key=True, default=uuid.uuid4),
    Column('name', VARCHAR(50), nullable=False, unique=True),
    Column('serial_number', VARCHAR(50), nullable=False, unique=True),
    Column('model', VARCHAR(50), nullable=False, unique=True),
    Column('count', INTEGER),
    CheckConstraint("serial_number ~ '^[A-Za-z0-9]{5,20}$'", name='check_serial_number'),
    CheckConstraint("count > 0", name='name_check_count')
)

# Клиенты
client_table = Table(
    'client',
    metadata,
    Column('oid', UUID, primary_key=True, default=uuid.uuid4),
    Column('surname', String(30), nullable=False),
    Column('name', String(30), nullable=False),
    Column('patronymic', String(30), nullable=False),
    Column('number', String(12), nullable=False)
)

# Склад комплектующих
component_warehouse_table = Table(
    'component_warehouse',
    metadata,
    Column('oid', UUID, primary_key=True, default=uuid.uuid4),
    Column('name', String(30), nullable=False),
    Column('cost_per_unit', Numeric(10, 2), nullable=False),
)

# Список мастеров
list_of_masters_table = Table(
    'list_of_masters',
    metadata,
    Column('oid', UUID, primary_key=True, default=uuid.uuid4),
    Column('position_oid', UUID, ForeignKey('position_of_master.oid', ondelete="CASCADE"), nullable=False),
    Column('surname', String(30), nullable=False),
    Column('name', String(30), nullable=False),
    Column('patronymic', String(30), nullable=False),
    Column('address', String(100), nullable=False),
    Column('number', String(12), nullable=False),
    Column('date_of_employment', Date, nullable=False),
    CheckConstraint("date_of_employment > '1980-01-01'", name='check_date_of_employment')
)

# Заказ комплектующих
component_order_table = Table(
    'component_order',
    metadata,
    Column('oid', UUID, primary_key=True, default=uuid.uuid4),
    Column('component_oid', UUID, ForeignKey('component_warehouse.oid', ondelete="CASCADE"), nullable=False),
    Column('order_fulfillment_oid', UUID, ForeignKey('order_fulfillment.oid', ondelete="CASCADE"), nullable=False)
)

# Бронирование
booking_table = Table(
    'booking',
    metadata,
    Column('oid', UUID, primary_key=True, default=uuid.uuid4),
    Column('equipment_oid', UUID, ForeignKey('equipment.oid', ondelete="CASCADE"), nullable=False),
    Column('client_oid', UUID, ForeignKey('client.oid', ondelete="CASCADE"), nullable=False),
    Column('master_oid', UUID, ForeignKey('list_of_masters.oid', ondelete="CASCADE"), nullable=False),
    Column('status_oid', UUID, ForeignKey('status_of_booking.oid', ondelete="CASCADE"), nullable=False),
    Column('component_order_oid', UUID, ForeignKey('component_order.oid', ondelete="CASCADE"), nullable=False),
    Column('booking_date', Date, nullable=False),
    CheckConstraint("booking_date > '1980-01-01'", name='check_booking_date')
)

# Индексы для списка мастеров
Index('idx_list_of_masters_surname', list_of_masters_table.c.surname)
Index('idx_list_of_masters_name', list_of_masters_table.c.name)


def start_mappers() -> None:
    """
    Map all domain models to ORM models, for purpose of using domain models directly during work with the database,
    according to DDD.
    """
    from app.domain.entities.client import ClientEntity
    from app.domain.entities.equipment import EquipmentEntity
    from app.domain.values.master import PositionOfMaster
    from app.domain.entities.order_fullillment import OrderFulfillmentEntity
    from app.domain.values.booking import StatusOfBooking
    from app.domain.entities.component_order import ComponentOrderEntity
    from app.domain.entities.booking import BookingEntity

    mapper_registry.map_imperatively(PositionOfMaster, position_of_master)
    mapper_registry.map_imperatively(OrderFulfillmentEntity, order_fulfillment_table)
    mapper_registry.map_imperatively(StatusOfBooking, status_of_booking_table)
    mapper_registry.map_imperatively(EquipmentEntity, equipment_table)
    mapper_registry.map_imperatively(ClientEntity, client_table)
    mapper_registry.map_imperatively(ComponentOrderEntity, component_order_table)
    mapper_registry.map_imperatively(BookingEntity, booking_table)
