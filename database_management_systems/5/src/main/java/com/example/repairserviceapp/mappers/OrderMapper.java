package com.example.repairserviceapp.mappers;

import com.example.repairserviceapp.DTOs.order.OrderDTORequest;
import com.example.repairserviceapp.DTOs.order.OrderDTOResponse;
import com.example.repairserviceapp.DTOs.order.OrderHistoryDTOResponse;
import com.example.repairserviceapp.entities.Order;
import com.example.repairserviceapp.entities.OrderHistory;
import com.example.repairserviceapp.services.*;
import lombok.Setter;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.springframework.beans.factory.annotation.Autowired;

import java.time.LocalDate;
import java.time.OffsetDateTime;
import java.time.ZoneOffset;
import java.util.UUID;

@Mapper(componentModel = "spring")
public abstract class OrderMapper {

    @Setter(onMethod = @__(@Autowired))
    protected ClientsService clientsService;
    @Setter(onMethod = @__(@Autowired))
    protected EquipmentsService equipmentsService;
    @Setter(onMethod = @__(@Autowired))
    protected MastersService mastersService;
    @Setter(onMethod = @__(@Autowired))
    protected StatusesService statusesService;
    @Setter(onMethod = @__(@Autowired))
    protected OrderOfComponentsService orderOfComponentsService;

    @Mapping(target = "clientId", expression = "java(order.getClient().getId())")
    @Mapping(target = "equipmentId", expression = "java(order.getEquipment().getId())")
    @Mapping(target = "masterId", expression = "java(order.getMaster().getId())")
    @Mapping(target = "statusId", expression = "java(order.getStatus().getId())")
    @Mapping(target = "orderOfComponentsId", expression = "java(order.getOrderOfComponents()==null ? null  : order.getOrderOfComponents().getId())")
    public abstract OrderDTOResponse toDTO(Order order);

    @Mapping(target = "client", expression = "java(clientsService.read(orderDTORequest.clientId()))")
    @Mapping(target = "equipment", expression = "java(equipmentsService.read(orderDTORequest.equipmentId()))")
    @Mapping(target = "master", expression = "java(mastersService.read(orderDTORequest.masterId()))")
    @Mapping(target = "status", expression = "java(statusesService.read(orderDTORequest.statusId()))")
    @Mapping(target = "orderOfComponents", expression = "java(orderOfComponentsService.read(orderDTORequest.orderOfComponentsId()))")
    public abstract Order toOrder(OrderDTORequest orderDTORequest);

    public OrderHistoryDTOResponse toDTO(OrderHistory orderHistory) {
        if (orderHistory == null) {
            return null;
        }

        UUID id;
        UUID clientId;
        UUID equipmentId;
        LocalDate date;
        UUID masterId;
        UUID statusId;
        UUID orderOfComponentsId;
        OffsetDateTime offsetDateTime;

        id = orderHistory.getId();
        clientId = orderHistory.getClient().getId();
        equipmentId = orderHistory.getEquipment().getId();
        masterId = orderHistory.getMaster().getId();
        statusId = orderHistory.getStatus().getId();
        date = orderHistory.getDate();
        orderOfComponentsId = orderHistory.getOrderOfComponents().getId();
        offsetDateTime = orderHistory.getLocalDateRange().lower().toOffsetDateTime().withOffsetSameInstant(ZoneOffset.UTC);

        return new OrderHistoryDTOResponse(
                id,
                date,
                clientId,
                equipmentId,
                masterId,
                statusId,
                orderOfComponentsId,
                offsetDateTime
        );
    }

}
