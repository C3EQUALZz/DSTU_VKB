package com.example.repairserviceapp.DTOs.order;

import com.example.repairserviceapp.annotations.MinDate;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;

import java.time.LocalDate;
import java.time.OffsetDateTime;
import java.util.UUID;

@Schema(description = "a order entity, this entity is displayed only by the admin for temporality")
public record OrderHistoryDTOResponse(

        @Schema(
                description = "Unique identifier of order (uuid)",
                example = "4f6652f1-b61c-4b30-8776-e73a107cd97f",
                accessMode = Schema.AccessMode.READ_ONLY
        )
        @NotNull
        UUID id,
        @NotNull(message = "Date must be not empty")
        @MinDate(value = "2000-01-01")
        LocalDate date,
        @Schema(
                description = "Unique identifier of client (uuid)",
                example = "4f6652f1-b61c-4b30-8776-e73a107cd97f",
                accessMode = Schema.AccessMode.READ_ONLY
        )
        @NotNull(message = " Client id must be not empty")
        UUID clientId,

        @Schema(
                description = "Unique identifier of equipment (uuid)",
                example = "4f6652f1-b61c-4b30-8776-e73a107cd97f",
                accessMode = Schema.AccessMode.READ_ONLY
        )
        @NotNull(message = "Equipment id must be not empty")
        UUID equipmentId,

        @Schema(
                description = "Unique identifier of master (uuid)",
                example = "4f6652f1-b61c-4b30-8776-e73a107cd97f",
                accessMode = Schema.AccessMode.READ_ONLY
        )
        @NotNull(message = "Master id must be not empty")
        UUID masterId,

        @Schema(
                description = "Unique identifier of status (uuid)",
                example = "4f6652f1-b61c-4b30-8776-e73a107cd97f",
                accessMode = Schema.AccessMode.READ_ONLY
        )
        @NotNull(message = "Status id must be not empty")
        UUID statusId,

        @Schema(
                description = "Unique identifier of order component (uuid)",
                example = "4f6652f1-b61c-4b30-8776-e73a107cd97f",
                accessMode = Schema.AccessMode.READ_ONLY
        )
        UUID orderOfComponentsId,

        @Schema(description = "Time that shows the relevance and status of the data", example = "2007-12-03T10:15:30+01:00")
        @NotEmpty(message = "offsetDateTime field can't be empty, please provide it")
        OffsetDateTime offsetDateTime
) {
}
