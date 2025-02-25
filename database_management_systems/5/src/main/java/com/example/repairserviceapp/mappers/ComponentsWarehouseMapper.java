package com.example.repairserviceapp.mappers;

import com.example.repairserviceapp.DTOs.componentsWarehouse.ComponentsWarehouseDTORequest;
import com.example.repairserviceapp.DTOs.componentsWarehouse.ComponentsWarehouseDTOResponse;
import com.example.repairserviceapp.DTOs.componentsWarehouse.ComponentsWarehouseHistoryDTOResponse;
import com.example.repairserviceapp.entities.BaseComponentsWarehouse;
import com.example.repairserviceapp.entities.ComponentsWarehouse;
import lombok.extern.slf4j.Slf4j;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring")
@Slf4j
public abstract class ComponentsWarehouseMapper extends BaseMapper {

    public abstract ComponentsWarehouseDTOResponse toDTO(ComponentsWarehouse componentsWarehouse);

    public abstract ComponentsWarehouse toEntity(ComponentsWarehouseDTORequest dto);

    @Mapping(target = "offsetDateTime", expression = "java(convertTime(baseComponentsWarehouse.getLocalDateRange()))")
    public abstract ComponentsWarehouseHistoryDTOResponse toHistoryDTO(BaseComponentsWarehouse baseComponentsWarehouse);
}
