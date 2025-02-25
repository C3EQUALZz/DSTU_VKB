package com.example.repairserviceapp.controllers;

import com.example.repairserviceapp.DTOs.componentsWarehouse.ComponentsWarehouseHistoryDTOResponse;
import com.example.repairserviceapp.mappers.ComponentsWarehouseMapper;
import com.example.repairserviceapp.services.ComponentsWarehouseService;
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

@Tag(name = "Контроллер для управления компонентами на складе", description = "Здесь реализуется свойство темпоральности")
@PreAuthorize("hasAuthority('ADMIN')")
@RestController
@RequestMapping("/api/history/components-warehouse")
@AllArgsConstructor(onConstructor = @__(@Autowired))
public class ComponentsWarehouseHistoryController extends BaseController {

    private final ComponentsWarehouseService componentsWarehouseService;
    private final ComponentsWarehouseMapper componentsWarehouseMapper;

    @Operation(
            summary = "Вернуть старые данные набора компонентов на складе по UUID",
            description = "Позволяет возвращать старые данные, которые были проделаны в результате работы БД. "
    )
    @PatchMapping("/{id}")
    public ComponentsWarehouseHistoryDTOResponse restore(
            @PathVariable("id") @Parameter(description = "Уникальный идентификатор оборудования", required = true) UUID id,
            @RequestBody @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) OffsetDateTime timestamp
    ) {
        return componentsWarehouseMapper.toDTO(componentsWarehouseService.restore(id, timestamp));
    }

    @Operation(
            summary = "Показывает все оборудование в темпоральной таблице со временем",
            description = "Позволяет показывать всех пользователей с временем изменений данных"
    )
    @GetMapping("")
    public List<ComponentsWarehouseHistoryDTOResponse> readAllTemporal() {
        return componentsWarehouseService
                .readAllHistory()
                .stream()
                .map(componentsWarehouseMapper::toDTO)
                .collect(Collectors.toList());
    }

}
