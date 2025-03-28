package com.example.repairserviceapp.mappers;

import com.example.repairserviceapp.DTOs.equipment.EquipmentDTORequest;
import com.example.repairserviceapp.DTOs.equipment.EquipmentDTOResponse;
import com.example.repairserviceapp.DTOs.equipment.HistoryEquipmentDTOResponse;
import com.example.repairserviceapp.entities.Equipment;
import com.example.repairserviceapp.entities.EquipmentHistory;
import lombok.Setter;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.springframework.beans.factory.annotation.Autowired;

@Mapper(componentModel = "spring")
public abstract class EquipmentsMapper extends BaseMapper {

    @Setter(onMethod = @__(@Autowired))
    protected OrderMapper orderMapper;

    public abstract EquipmentDTOResponse toDTO(Equipment equipment);

    public abstract Equipment toEquipment(EquipmentDTORequest equipmentDTORequest);

    @Mapping(target = "orders", expression = "java(equipment.getOrders().stream().map(orderMapper::toDTO).toList())")
    @Mapping(target = "offsetDateTime", expression = "java(convertTime(equipment.getLocalDateRange()))")
    public abstract HistoryEquipmentDTOResponse toHistoryDTO(Equipment equipment);

    @Mapping(target = "orders", ignore = true)
    @Mapping(target = "offsetDateTime", expression = "java(convertTime(historyEquipment.getLocalDateRange()))")
    public abstract HistoryEquipmentDTOResponse toHistoryDTO(EquipmentHistory historyEquipment);
}
