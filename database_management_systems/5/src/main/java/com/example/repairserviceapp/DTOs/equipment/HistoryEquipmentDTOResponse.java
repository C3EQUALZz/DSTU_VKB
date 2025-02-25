package com.example.repairserviceapp.DTOs.equipment;

import com.example.repairserviceapp.DTOs.order.OrderDTOResponse;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

import java.time.OffsetDateTime;
import java.util.List;
import java.util.UUID;

@Schema(description = "a equipment entity, this entity is displayed only by the admin for temporality")
public record HistoryEquipmentDTOResponse(
        @Schema(
                description = "Unique identifier of equipment (uuid)",
                example = "4f6652f1-b61c-4b30-8776-e73a107cd97f",
                accessMode = Schema.AccessMode.READ_ONLY
        )
        @NotEmpty(message = "name field can't be empty, please provide it")
        UUID id,

        @NotEmpty(message = "name field can't be empty, please provide it")
        @Size(min = 2, max = 30, message = "Size must be between 2 and 30")
        String name,

        @NotEmpty(message = "serialNumber field can't be empty, please provide it")
        @Size(min = 2, max = 30, message = "Size must be between 2 and 30")
        String serialNumber,

        @NotEmpty(message = "model field can't be empty, please provide it")
        @Size(min = 2, max = 30, message = "Size must be between 2 and 30")
        String model,

        @NotNull(message = "orders field can't be null, please provide some data")
        List<OrderDTOResponse> orders,

        @Schema(description = "Time that shows the relevance and status of the data", example = "2007-12-03T10:15:30+01:00")
        @NotEmpty(message = "offsetDateTime field can't be empty, please provide it")
        OffsetDateTime offsetDateTime
) {
}
