ALTER TABLE position_of_master
  ADD COLUMN sys_period tstzrange NOT NULL DEFAULT tstzrange(current_timestamp, null);

ALTER TABLE order_fulfillment
  ADD COLUMN sys_period tstzrange NOT NULL DEFAULT tstzrange(current_timestamp, null);

ALTER TABLE status_of_booking
  ADD COLUMN sys_period tstzrange NOT NULL DEFAULT tstzrange(current_timestamp, null);

ALTER TABLE equipment
  ADD COLUMN sys_period tstzrange NOT NULL DEFAULT tstzrange(current_timestamp, null);

ALTER TABLE client
  ADD COLUMN sys_period tstzrange NOT NULL DEFAULT tstzrange(current_timestamp, null);

ALTER TABLE component_warehouse
  ADD COLUMN sys_period tstzrange NOT NULL DEFAULT tstzrange(current_timestamp, null);

ALTER TABLE list_of_masters
  ADD COLUMN sys_period tstzrange NOT NULL DEFAULT tstzrange(current_timestamp, null);

ALTER TABLE component_order
  ADD COLUMN sys_period tstzrange NOT NULL DEFAULT tstzrange(current_timestamp, null);

ALTER TABLE booking
  ADD COLUMN sys_period tstzrange NOT NULL DEFAULT tstzrange(current_timestamp, null);

CREATE TABLE position_of_master_history (LIKE position_of_master);
CREATE TABLE order_fulfillment_history (LIKE order_fulfillment);
CREATE TABLE status_of_booking_history (LIKE status_of_booking);
CREATE TABLE equipment_history (LIKE equipment);
CREATE TABLE client_history (LIKE client);
CREATE TABLE component_warehouse_history (LIKE component_warehouse);
CREATE TABLE list_of_masters_history (LIKE list_of_masters);
CREATE TABLE component_order_history (LIKE component_order);
CREATE TABLE booking_history (LIKE booking)