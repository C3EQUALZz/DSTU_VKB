package com.example.repairserviceapp.mappers;

import com.example.repairserviceapp.DTOs.componentsWarehouse.ComponentsWarehouseDTORequest;
import com.example.repairserviceapp.DTOs.componentsWarehouse.ComponentsWarehouseDTOResponse;
import com.example.repairserviceapp.DTOs.componentsWarehouse.ComponentsWarehouseHistoryDTOResponse;
import com.example.repairserviceapp.entities.ComponentsWarehouse;
import com.example.repairserviceapp.entities.ComponentsWarehouseHistory;
import org.mapstruct.Mapper;

import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.time.ZoneOffset;
import java.util.UUID;

@Mapper(componentModel = "spring")
public abstract class ComponentsWarehouseMapper {

    public abstract ComponentsWarehouseDTOResponse toDTO(ComponentsWarehouse componentsWarehouse);

    public abstract ComponentsWarehouse toEntity(ComponentsWarehouseDTORequest dto);

    public ComponentsWarehouseHistoryDTOResponse toDTO(ComponentsWarehouseHistory componentsWarehouseHistory) {

        UUID id;
        String componentName;
        Integer componentsAmount;
        BigDecimal unitCost;
        OffsetDateTime offsetDateTime;
        
        id = componentsWarehouseHistory.getId();
        componentName = componentsWarehouseHistory.getComponentName();
        componentsAmount = componentsWarehouseHistory.getComponentsAmount();
        unitCost = componentsWarehouseHistory.getUnitCost();
        offsetDateTime = componentsWarehouseHistory.getLocalDateRange().lower().toOffsetDateTime().withOffsetSameInstant(ZoneOffset.UTC);
        
        return new ComponentsWarehouseHistoryDTOResponse(
                id,
                componentName,
                componentsAmount,
                unitCost,
                offsetDateTime
        );
    }
}
