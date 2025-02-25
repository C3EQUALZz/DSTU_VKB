--liquibase formatted sql
--changeset DDD:240
CREATE OR REPLACE FUNCTION decrease_component_amount()
    RETURNS TRIGGER AS
'
    BEGIN

        UPDATE components_warehouse
        SET components_amount = components_amount - 1
        WHERE components_code = NEW.component_code;

        RETURN NEW;
    END;
' LANGUAGE plpgsql;
--rollback DROP FUNCTION IF EXISTS decrease_component_amount();

--changeset DDD:241
CREATE TRIGGER update_component_amount
    AFTER INSERT
    ON components_order
    FOR EACH ROW
EXECUTE FUNCTION decrease_component_amount();
--rollback DROP TRIGGER IF EXISTS update_component_amount;


