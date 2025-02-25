package com.example.repairserviceapp.DTOs.master;

import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;

import java.time.LocalDate;
import java.util.UUID;

public record MasterDTOResponse(
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
        UUID postId
) {
}
