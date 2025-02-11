CREATE TRIGGER versioning_trigger_position_of_master
BEFORE INSERT OR UPDATE OR DELETE ON position_of_master
FOR EACH ROW EXECUTE PROCEDURE versioning(
  'sys_period', 'position_of_master_history', true
);

CREATE TRIGGER versioning_trigger_order_fulfillment
BEFORE INSERT OR UPDATE OR DELETE ON order_fulfillment
FOR EACH ROW EXECUTE PROCEDURE versioning(
  'sys_period', 'order_fulfillment_history', true
);

CREATE TRIGGER versioning_trigger_status_of_booking
BEFORE INSERT OR UPDATE OR DELETE ON status_of_booking
FOR EACH ROW EXECUTE PROCEDURE versioning(
  'sys_period', 'status_of_booking_history', true
);

CREATE TRIGGER versioning_trigger_equipment
BEFORE INSERT OR UPDATE OR DELETE ON equipment
FOR EACH ROW EXECUTE PROCEDURE versioning(
  'sys_period', 'equipment_history', true
);

CREATE TRIGGER versioning_trigger_client
BEFORE INSERT OR UPDATE OR DELETE ON client
FOR EACH ROW EXECUTE PROCEDURE versioning(
  'sys_period', 'client_history', true
);

CREATE TRIGGER versioning_trigger_component_warehouse
BEFORE INSERT OR UPDATE OR DELETE ON component_warehouse
FOR EACH ROW EXECUTE PROCEDURE versioning(
  'sys_period', 'component_warehouse_history', true
);

CREATE TRIGGER versioning_trigger_list_of_masters
BEFORE INSERT OR UPDATE OR DELETE ON list_of_masters
FOR EACH ROW EXECUTE PROCEDURE versioning(
  'sys_period', 'list_of_masters_history', true
);

CREATE TRIGGER versioning_trigger_component_order
BEFORE INSERT OR UPDATE OR DELETE ON component_order
FOR EACH ROW EXECUTE PROCEDURE versioning(
  'sys_period', 'component_order_history', true
);

CREATE TRIGGER versioning_trigger_booking
BEFORE INSERT OR UPDATE OR DELETE ON booking
FOR EACH ROW EXECUTE PROCEDURE versioning(
  'sys_period', 'booking_history', true
);



