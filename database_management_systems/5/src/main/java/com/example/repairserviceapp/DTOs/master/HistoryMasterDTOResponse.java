package com.example.repairserviceapp.DTOs.master;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;

import java.time.LocalDate;
import java.time.OffsetDateTime;
import java.util.UUID;

@Schema(description = "a master entity, this entity is displayed only by the admin for temporality")
public record HistoryMasterDTOResponse(

        @Schema(
                description = "Unique identifier of equipment (uuid)",
                example = "4f6652f1-b61c-4b30-8776-e73a107cd97f",
                accessMode = Schema.AccessMode.READ_ONLY
        )
        @NotEmpty(message = "name field can't be empty, please provide it")
        UUID id,

        @NotNull(message = "Surname must be not empty")
        @Size(min = 2, max = 30, message = "Size must be between 2 and 30")
        String surname,

        @NotNull(message = "Name must be not empty")
        @Size(min = 2, max = 30, message = "Size must be between 2 and 30")
        String name,

        @NotNull(message = "Patronymic must be not empty")
        @Size(min = 2, max = 30, message = "Size must be between 2 and 30")
        String patronymic,

        @NotNull(message = "Address must be not empty")
        @Size(min = 2, max = 30, message = "Size must be between 2 and 30")
        String address,

        @NotNull(message = "Phone number must be not empty")
        @Pattern(regexp = "^(\\+7|8)[0-9]{10}$", message = "Phone number must be valid")
        String phoneNumber,

        @NotNull(message = "Date of employment must be not empty")
        LocalDate dateOfEmployment,

        @NotNull(message = "post id must be not empty")
        UUID postId,

        @Schema(description = "Time that shows the relevance and status of the data", example = "2007-12-03T10:15:30+01:00")
        @NotNull(message = "Zoned date time must be not empty")
        OffsetDateTime offsetDateTime
) {
}

