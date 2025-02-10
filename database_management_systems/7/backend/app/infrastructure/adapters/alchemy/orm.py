from sqlalchemy import Column, String, Numeric, Table, UUID, VARCHAR, Computed, DATE, Date, CheckConstraint

from app.infrastructure.adapters.alchemy.metadata import metadata

position_of_master = Table(
    'position_of_master',
    metadata,
    Column('oid', UUID, primary_key=True),
    Column('position', VARCHAR(30), unique=True),
)

order_fulfillment_table = Table(
    'order_fulfillment',
    metadata,
    Column('oid', UUID, primary_key=True),
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
    Column('oid', UUID, primary_key=True),
    Column('name', VARCHAR(50), nullable=False, unique=True),
)

equipment_table = Table(
    'equipment',
    metadata,
    Column('oid', UUID, primary_key=True),
    Column('name', VARCHAR(50), nullable=False, unique=True),
    Column('serial_number', VARCHAR(50), nullable=False, unique=True),
    CheckConstraint("serial_number ~ '^[A-Za-z0-9]{5,20}$'", name='check_serial_number')
)

client_table = Table(
    'client',
    metadata,
    Column('oid', UUID, primary_key=True),
    Column('surname', String(30), nullable=False),
    Column('name', String(30), nullable=False),
    Column('patronymic', String(30), nullable=False),
    Column('number', String(12), nullable=False)
)

component_warehouse_table = Table(
    'component_warehouse',
    metadata,
    Column('oid', UUID, primary_key=True),
    Column('name', String(30), nullable=False),
    Column('cost_per_unit', Numeric(10, 2), nullable=False),
)


