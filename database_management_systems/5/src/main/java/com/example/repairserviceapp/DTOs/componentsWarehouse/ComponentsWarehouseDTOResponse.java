package com.example.repairserviceapp.DTOs.componentsWarehouse;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;

import java.math.BigDecimal;
import java.util.UUID;

public record ComponentsWarehouseDTOResponse(
        UUID id,
        @NotNull(message = "Components name must be not null")
        @NotEmpty(message = "Components name must be not empty")
        String componentName,
        @NotNull(message = "Components amount must be not null")
        @Min(value = 0, message = "Components amount must be greater than 0")
        Integer componentsAmount,
        @NotNull(message = "Components cost must be not null")
        BigDecimal unitCost
) {
}
