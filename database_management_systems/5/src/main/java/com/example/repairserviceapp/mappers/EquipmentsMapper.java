package com.example.repairserviceapp.mappers;

import com.example.repairserviceapp.DTOs.equipment.HistoryEquipmentDTOResponse;
import com.example.repairserviceapp.DTOs.order.OrderDTOResponse;
import com.example.repairserviceapp.entities.EquipmentHistory;
import lombok.Setter;
import org.mapstruct.Mapper;
import org.springframework.beans.factory.annotation.Autowired;

import java.time.OffsetDateTime;
import java.time.ZoneOffset;
import java.util.List;
import java.util.UUID;

@Mapper(componentModel = "spring")
public abstract class EquipmentsMapper {

    @Setter(onMethod = @__(@Autowired))
    private OrderMapper orderMapper;

    public HistoryEquipmentDTOResponse toDTO(EquipmentHistory equipmentHistory) {
        if (equipmentHistory == null) {
            return null;
        }

        UUID id;
        String name;
        String serialNumber;
        String model;
        List<OrderDTOResponse> orders;
        OffsetDateTime localDateRange;

        id = equipmentHistory.getId();
        name = equipmentHistory.getName();
        serialNumber = equipmentHistory.getSerialNumber();
        model = equipmentHistory.getModel();
        orders = equipmentHistory.getOrders().stream().map(order -> orderMapper.toDTO(order)).toList();
        localDateRange = equipmentHistory.getLocalDateRange().lower().toOffsetDateTime().withOffsetSameInstant(ZoneOffset.UTC);

        return new HistoryEquipmentDTOResponse(id, name, serialNumber, model, orders, localDateRange);
    }
}
