package com.example.repairserviceapp.controllers;

import com.example.repairserviceapp.DTOs.master.HistoryMasterDTOResponse;
import com.example.repairserviceapp.mappers.MasterMapper;
import com.example.repairserviceapp.services.MastersService;
import io.swagger.v3.oas.annotations.Operation;
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

@Tag(name = "Контроллер для управления историей мастеров", description = "Здесь реализуется свойство темпоральности")
@PreAuthorize("hasAuthority('ADMIN')")
@RestController
@RequestMapping("/api/history/master")
@AllArgsConstructor(onConstructor = @__(@Autowired))
public class MastersHistoryController extends BaseController {
    private MastersService masterService;
    private MasterMapper masterMapper;

    @Operation(
            summary = "Вернуть старые данные мастера по UUID",
            description = "Позволяет возвращать старые данные, которые были проделаны в результате работы БД. "
    )
    @PatchMapping("/{id}")
    public HistoryMasterDTOResponse restore(@PathVariable("id") UUID id, @RequestBody @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) OffsetDateTime timestamp) {
        return masterMapper.toDTO(masterService.restore(id, timestamp));
    }

    @Operation(
            summary = "Показывает всех мастеров в темпоральной таблице со временем",
            description = "Позволяет показывать всех мастеров с временем изменений данных"
    )
    @GetMapping("")
    public List<HistoryMasterDTOResponse> readAllTemporal() {
        return masterService
                .readAllHistory()
                .stream()
                .map(masterMapper::toDTO)
                .collect(Collectors.toList());
    }
}
