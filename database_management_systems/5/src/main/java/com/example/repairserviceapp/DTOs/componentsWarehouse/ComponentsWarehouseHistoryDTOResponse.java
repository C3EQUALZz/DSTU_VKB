package com.example.repairserviceapp.DTOs.componentsWarehouse;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;

import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.UUID;

@Schema(description = "a component warehouse entity, this entity is displayed only by the admin for temporality")
public record ComponentsWarehouseHistoryDTOResponse(
        @Schema(
                description = "Unique identifier of component warehouse (uuid)",
                example = "4f6652f1-b61c-4b30-8776-e73a107cd97f",
                accessMode = Schema.AccessMode.READ_ONLY
        )
        UUID id,

        @Schema(description = "Name of component", example = "Резистор")
        @NotNull(message = "Components name must be not null")
        @NotEmpty(message = "Components name must be not empty")
        String componentName,

        @Schema(description = "Amount of component", example = "100")
        @NotNull(message = "Components amount must be not null")
        @Min(value = 0, message = "Components amount must be greater than 0")
        Integer componentsAmount,

        @Schema(description = "Cost of component in dollars", example = "0.10")
        @NotNull(message = "Components cost must be not null")
        BigDecimal unitCost,

        @Schema(description = "Time that shows the relevance and status of the data", example = "2007-12-03T10:15:30+01:00")
        @NotNull(message = "Zoned date time must be not empty")
        OffsetDateTime offsetDateTime
) {
}
