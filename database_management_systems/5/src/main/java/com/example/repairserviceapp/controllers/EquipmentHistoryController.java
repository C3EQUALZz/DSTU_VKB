package com.example.repairserviceapp.controllers;

import com.example.repairserviceapp.DTOs.equipment.HistoryEquipmentDTOResponse;
import com.example.repairserviceapp.mappers.EquipmentsMapper;
import com.example.repairserviceapp.services.EquipmentsService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.AllArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.time.OffsetDateTime;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

@Tag(name = "Контроллер для управления историей оборудования", description = "Здесь реализуется свойство темпоральности")
@PreAuthorize("hasAuthority('ROLE_ADMIN')")
@RestController
@RequestMapping("/api/history/equipment")
@AllArgsConstructor(onConstructor = @__(@Autowired))
public class EquipmentHistoryController extends BaseController {
    private EquipmentsService equipmentsService;
    private EquipmentsMapper equipmentsMapper;

    @Operation(
            summary = "Вернуть старые данные оборудования по UUID",
            description = "Позволяет возвращать старые данные, которые были проделаны в результате работы БД. "
    )
    @PatchMapping("/{id}")
    public HistoryEquipmentDTOResponse restore(
            @PathVariable("id") @Parameter(description = "Уникальный идентификатор оборудования", required = true) UUID id,
            @RequestBody @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) OffsetDateTime timestamp
    ) {
        return equipmentsMapper.toHistoryDTO(equipmentsService.restore(id, timestamp));
    }

    @Operation(
            summary = "Показывает все оборудование в темпоральной таблице со временем",
            description = "Позволяет показывать всех пользователей с временем изменений данных"
    )
    @GetMapping("")
    public List<HistoryEquipmentDTOResponse> readAllTemporal() {
        return equipmentsService
                .readAllHistory()
                .stream()
                .map(equipmentsMapper::toHistoryDTO)
                .collect(Collectors.toList());
    }
}
