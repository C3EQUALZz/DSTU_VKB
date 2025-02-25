package com.example.repairserviceapp.mappers;

import com.example.repairserviceapp.DTOs.orderOfComponents.OrderOfComponentsDTORequest;
import com.example.repairserviceapp.DTOs.orderOfComponents.OrderOfComponentsDTOResponse;
import com.example.repairserviceapp.DTOs.orderOfComponents.OrderOfComponentsHistoryDTOResponse;
import com.example.repairserviceapp.entities.OrderOfComponents;
import com.example.repairserviceapp.entities.OrderOfComponentsHistory;
import com.example.repairserviceapp.services.ComponentsWarehouseService;
import com.example.repairserviceapp.services.ExecutionOfOrderService;
import lombok.Setter;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.springframework.beans.factory.annotation.Autowired;

import java.time.OffsetDateTime;
import java.time.ZoneOffset;
import java.util.UUID;

@Mapper(componentModel = "spring")
public abstract class OrderOfComponentsMapper {

    @Setter(onMethod = @__(@Autowired))
    protected ComponentsWarehouseService componentsWarehouseService;

    @Setter(onMethod = @__(@Autowired))
    protected ExecutionOfOrderService executionOfOrderService;


    @Mapping(target = "componentsWarehouse", expression = "java(componentsWarehouseService.read(orderOfComponentsDTORequest.componentsWarehouseId()))")
    @Mapping(target = "executionOfOrder", expression = "java(executionOfOrderService.read(orderOfComponentsDTORequest.executionOfOrderId()))")
    public abstract OrderOfComponents toOrderOfComponents(OrderOfComponentsDTORequest orderOfComponentsDTORequest);

    @Mapping(target = "componentsWarehouseId", expression = "java(orderOfComponents.getComponentsWarehouse().getId())")
    @Mapping(target = "executionOfOrderId", expression = "java(orderOfComponents.getExecutionOfOrder().getId())")
    public abstract OrderOfComponentsDTOResponse toDTO(OrderOfComponents orderOfComponents);

    public OrderOfComponentsHistoryDTOResponse toDTO(OrderOfComponentsHistory orderOfComponentsHistory) {
        if (orderOfComponentsHistory == null) {
            return null;
        }

        UUID id;
        UUID componentsWarehouseId;
        UUID executionOfOrderId;
        OffsetDateTime offsetDateTime;

        id = orderOfComponentsHistory.getId();
        componentsWarehouseId = orderOfComponentsHistory.getComponentsWarehouse().getId();
        executionOfOrderId = orderOfComponentsHistory.getExecutionOfOrder().getId();
        offsetDateTime = orderOfComponentsHistory.getLocalDateRange().lower().toOffsetDateTime().withOffsetSameInstant(ZoneOffset.UTC);

        return new OrderOfComponentsHistoryDTOResponse(
                id,
                componentsWarehouseId,
                executionOfOrderId,
                offsetDateTime
        );
    }
}
