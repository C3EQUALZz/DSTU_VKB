package com.example.repairserviceapp.DTOs.orderOfComponents;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;

import java.time.OffsetDateTime;
import java.util.UUID;

public record OrderOfComponentsHistoryDTOResponse(

        @Schema(
                description = "Unique identifier of order (uuid)",
                example = "4f6652f1-b61c-4b30-8776-e73a107cd97f",
                accessMode = Schema.AccessMode.READ_ONLY
        )
        @NotEmpty(message = "name field can't be empty, please provide it")
        UUID id,

        @NotNull(message = "Components of warehouse id must be not empty")
        UUID componentsWarehouseId,

        @NotNull(message = "Execution of order id must be not empty")
        UUID executionOfOrderId,

        @Schema(description = "Time that shows the relevance and status of the data", example = "2007-12-03T10:15:30+01:00")
        @NotNull(message = "Offset date time must be not empty")
        OffsetDateTime offsetDateTime
) {
}
