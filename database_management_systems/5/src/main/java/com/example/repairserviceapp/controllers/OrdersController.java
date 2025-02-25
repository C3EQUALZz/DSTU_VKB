package com.example.repairserviceapp.controllers;

import com.example.repairserviceapp.DTOs.order.OrderDTORequest;
import com.example.repairserviceapp.DTOs.order.OrderDTOResponse;
import com.example.repairserviceapp.mappers.OrderMapper;
import com.example.repairserviceapp.services.OrdersService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.AllArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

@Tag(name = "Контроллер для управления заказами клиентов", description = "Здесь есть все CRUD операции")
@RestController
@RequestMapping("api/order")
@AllArgsConstructor(onConstructor = @__(@Autowired))
public class OrdersController extends BaseController {

    private OrdersService ordersService;
    private OrderMapper orderMapper;

    @Operation(
            summary = "Просмотр данных всех заказов",
            description = "Позволяет просмотреть всех заказы, которые совершил каждый клиент."
    )
    @GetMapping("")
    @PreAuthorize("hasAnyAuthority('ROLE_USER', 'ROLE_ADMIN')")
    public List<OrderDTOResponse> readAll() {
        return ordersService.readAll().stream().map(order -> orderMapper.toDTO(order)).collect(Collectors.toList());
    }

    @Operation(
            summary = "Просмотр данных отдельного заказов",
            description = "Позволяет просмотреть отдельный заказ, указав его ID."
    )
    @GetMapping("/{id}")
    @PreAuthorize("hasAnyAuthority('ROLE_USER', 'ROLE_ADMIN')")
    public OrderDTOResponse read(@PathVariable UUID id) {
        return orderMapper.toDTO(ordersService.read(id));
    }

    @Operation(
            summary = "Создание одного заказа",
            description = "Позволяет создать отдельный заказ"
    )
    @PostMapping("")
    @PreAuthorize("hasAnyAuthority('ROLE_ADMIN')")
    public OrderDTOResponse create(@RequestBody @Valid OrderDTORequest orderDTORequest, BindingResult bindingResult) {
        validate(bindingResult, "Create order failed");
        return orderMapper.toDTO(ordersService.create(orderMapper.toOrder(orderDTORequest)));
    }

    @Operation(
            summary = "Обновление данных отдельного заказа",
            description = "Позволяет обновлять данные об отдельном заказе, зная его id. "
    )
    @PatchMapping("/{id}")
    @PreAuthorize("hasAnyAuthority('ROLE_ADMIN')")
    public OrderDTOResponse update(@PathVariable UUID id, @RequestBody @Valid OrderDTORequest orderDTORequest, BindingResult bindingResult) {
        validate(bindingResult, "Update order failed");
        return orderMapper.toDTO(ordersService.update(id, orderMapper.toOrder(orderDTORequest)));
    }

    @Operation(
            summary = "Удаление данных об отдельном заказе",
            description = "Позволяет удалять данные об отдельном заказе, зная его id"
    )
    @DeleteMapping("/{id}")
    @PreAuthorize("hasAnyAuthority('ROLE_ADMIN')")
    public OrderDTOResponse delete(@PathVariable UUID id) {
        return orderMapper.toDTO(ordersService.delete(id));
    }
}
