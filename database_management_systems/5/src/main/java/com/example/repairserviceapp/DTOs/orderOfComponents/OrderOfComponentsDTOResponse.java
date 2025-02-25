package com.example.repairserviceapp.DTOs.orderOfComponents;

import jakarta.validation.constraints.NotNull;

import java.util.UUID;

public record OrderOfComponentsDTOResponse(
        UUID id,
        @NotNull(message = "Components of warehouse id must be not empty")
        UUID componentsWarehouseId,
        @NotNull(message = "Execution of order id must be not empty")
        UUID executionOfOrderId
) {
}
