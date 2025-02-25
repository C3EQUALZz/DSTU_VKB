package com.example.repairserviceapp.DTOs.client;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;

import java.util.UUID;

public record ClientDTORequest(
        @Schema(
                description = "Unique identifier of client (uuid)",
                example = "4f6652f1-b61c-4b30-8776-e73a107cd97f",
                accessMode = Schema.AccessMode.READ_ONLY
        )
        UUID id,

        @Schema(description = "Surname of client", example = "Ivanov")
        @NotNull(message = "Surname must be not empty")
        @Size(min = 2, max = 30, message = "Size of surname must be between 2 and 30")
        String surname,

        @Schema(description = "Name of client", example = "Ivan")
        @NotNull(message = "Name must be not empty")
        @Size(min = 2, max = 30, message = "Size of name must be between 2 and 30")
        String name,

        @Schema(description = "Patronymic of client", example = "Ivanovich")
        @NotNull(message = "Patronymic must be not empty")
        @Size(min = 2, max = 30, message = "Size of patronymic must be between 2 and 30")
        String patronymic,

        @Schema(description = "Phone number of client", example = "+71812554589")
        @NotNull(message = "Phone number must be not empty")
        @Pattern(regexp = "^(\\+7|8)[0-9]{10}$", message = "Phone number must be valid")
        String phoneNumber,

        @NotNull(message = "Email must be not null")
        @Email(message = "Email must be valid")
        @Size(min = 2, max = 30, message = "Size must be between 2 and 30")
        String email,

        @NotNull(message = "Password must be not null")
        String password
) {
}
