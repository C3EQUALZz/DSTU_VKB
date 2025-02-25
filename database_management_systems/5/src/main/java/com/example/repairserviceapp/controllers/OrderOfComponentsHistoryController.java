package com.example.repairserviceapp.controllers;

import com.example.repairserviceapp.DTOs.orderOfComponents.OrderOfComponentsHistoryDTOResponse;
import com.example.repairserviceapp.mappers.OrderOfComponentsMapper;
import com.example.repairserviceapp.services.OrderOfComponentsService;
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

@Tag(name = "Контроллер для управления заказов компонентов", description = "Здесь реализуется свойство темпоральности")
@PreAuthorize("hasAuthority('ADMIN')")
@RestController
@RequestMapping("/api/history/order-of-components")
@AllArgsConstructor(onConstructor = @__(@Autowired))
public class OrderOfComponentsHistoryController extends BaseController {
    private OrderOfComponentsService orderOfComponentsService;
    private OrderOfComponentsMapper orderOfComponentsMapper;

    @Operation(
            summary = "Вернуть старые данные заказа компонента",
            description = "Позволяет возвращать старые данные, которые были проделаны в результате работы БД. "
    )
    @PatchMapping("/{id}")
    public OrderOfComponentsHistoryDTOResponse restore(@PathVariable("id") UUID id, @RequestBody @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) OffsetDateTime timestamp) {
        return orderOfComponentsMapper.toDTO(orderOfComponentsService.restore(id, timestamp));
    }

    @Operation(
            summary = "Показывает все заказы в темпоральной таблице со временем",
            description = "Позволяет показывать все заказы компонентов со временем изменений данных"
    )
    @GetMapping("")
    public List<OrderOfComponentsHistoryDTOResponse> readAllTemporal() {
        return orderOfComponentsService
                .readAllHistory()
                .stream()
                .map(orderOfComponentsMapper::toDTO)
                .collect(Collectors.toList());
    }
}
