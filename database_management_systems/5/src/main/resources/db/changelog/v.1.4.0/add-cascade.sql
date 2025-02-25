--liquibase formatted sql
--changeset DDD:300
ALTER TABLE orders
    DROP CONSTRAINT fk_orders_order_components_code;


--changeset DDD:301
ALTER TABLE orders
    ADD CONSTRAINT fk_orders_order_components_code
        FOREIGN KEY (order_components_code) REFERENCES components_order(co_code) ON DELETE SET NULL;