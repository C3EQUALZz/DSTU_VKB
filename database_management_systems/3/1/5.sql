SELECT "INV", COALESCE("C_GROUP", 'Штатная группа не задана')
FROM "AUTO" 
WHERE "C_GROUP" = (
	SELECT "C_MENU"||"C_REC" 
	FROM "MENU"
	WHERE "NAME_REC"='стандартный'
)
OR "C_GROUP" IS NULL
