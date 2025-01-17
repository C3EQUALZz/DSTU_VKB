/**
  Для всех ключевых полей (как первичных ключей, так и внешних) создать индексы командой CREATE INDEX.
 */

CREATE INDEX ON electronic_equipment (manufacturer);
CREATE INDEX ON furniture (material);