package com.example.repairserviceapp.DTOs.order;

import com.example.repairserviceapp.annotations.MinDate;
import jakarta.validation.constraints.NotNull;

import java.time.LocalDate;
import java.util.UUID;

public record OrderDTORequest(
        @NotNull(message = "Date must be not empty")
        @MinDate(value = "2000-01-01")
        LocalDate date,
        @NotNull(message = " Client id must be not empty")
        UUID clientId,
        @NotNull(message = "Equipment id must be not empty")
        UUID equipmentId,
        @NotNull(message = "Master id must be not empty")
        UUID masterId,
        @NotNull(message = "Status id must be not empty")
        UUID statusId,
        UUID orderOfComponentsId
) {
}
