package com.example.repairserviceapp.controllers;

import com.example.repairserviceapp.DTOs.client.HistoryClientDTOResponse;
import com.example.repairserviceapp.mappers.ClientsMapper;
import com.example.repairserviceapp.services.ClientsService;
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

@Tag(name = "Контроллер для управления историей клиентов", description = "Здесь реализуется свойство темпоральности")
@PreAuthorize("hasAuthority('ADMIN')")
@RestController
@RequestMapping("/api/history/client")
@AllArgsConstructor(onConstructor = @__(@Autowired))
public class ClientsHistoryController extends BaseController {
    private ClientsService clientsService;
    private ClientsMapper clientsMapper;

    @Operation(
            summary = "Вернуть старые данные пользователя по UUID",
            description = "Позволяет возвращать старые данные, которые были проделаны в результате работы БД. "
    )
    @PatchMapping("/{id}")
    public HistoryClientDTOResponse restore(
            @PathVariable("id") @Parameter(description = "Уникальный идентификатор клиента", required = true) UUID id,
            @RequestBody @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) OffsetDateTime timestamp
    ) {
        return clientsMapper.toDTO(clientsService.restore(id, timestamp));
    }

    @Operation(
            summary = "Показывает всех пользователей в темпоральной таблице со временем",
            description = "Позволяет показывать всех пользователей с временем изменений данных"
    )
    @GetMapping("")
    public List<HistoryClientDTOResponse> readAllTemporal() {
            return clientsService
                    .readAllHistory()
                    .stream()
                    .map(clientsMapper::toDTO)
                    .collect(Collectors.toList());
    }
}
