package com.example.repairserviceapp.controllers;

import com.example.repairserviceapp.DTOs.orderOfComponents.OrderOfComponentsDTORequest;
import com.example.repairserviceapp.DTOs.orderOfComponents.OrderOfComponentsDTOResponse;
import com.example.repairserviceapp.mappers.OrderOfComponentsMapper;
import com.example.repairserviceapp.services.OrderOfComponentsService;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.AllArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@Tag(name = "Контроллер для управления заказов компонентов", description = "Здесь есть все операции CRUD")
@RestController
@RequestMapping("/api/order-of-components")
@AllArgsConstructor(onConstructor = @__(@Autowired))
public class OrderOfComponentsController extends BaseController {

    private OrderOfComponentsService orderOfComponentsService;
    private OrderOfComponentsMapper orderOfComponentsMapper;

    @GetMapping("")
    @PreAuthorize("hasAnyAuthority('ROLE_USER', 'ROLE_ADMIN')")
    public List<OrderOfComponentsDTOResponse> readAll() {
        return orderOfComponentsService
                .readAll()
                .stream()
                .map(elem -> orderOfComponentsMapper.toDTO(elem))
                .toList();
    }

    @GetMapping("/{id}")
    @PreAuthorize("hasAnyAuthority('ROLE_USER', 'ROLE_ADMIN')")
    public OrderOfComponentsDTOResponse read(@PathVariable UUID id) {
        return orderOfComponentsMapper.toDTO(orderOfComponentsService.read(id));
    }

    @PostMapping("")
    @PreAuthorize("hasAnyAuthority('ROLE_ADMIN')")
    public OrderOfComponentsDTOResponse create(@RequestBody @Valid OrderOfComponentsDTORequest dto, BindingResult bindingResult) {
        validate(bindingResult, "Create OrderOfComponents failed");
        return orderOfComponentsMapper.toDTO(orderOfComponentsService.create(orderOfComponentsMapper.toOrderOfComponents(dto)));
    }

    @PatchMapping("/{id}")
    @PreAuthorize("hasAnyAuthority('ROLE_ADMIN')")
    public OrderOfComponentsDTOResponse update(@PathVariable UUID id, @RequestBody @Valid OrderOfComponentsDTORequest dto, BindingResult bindingResult) {
        validate(bindingResult, "Update OrderOfComponents failed");
        return orderOfComponentsMapper.toDTO(orderOfComponentsService.update(id, orderOfComponentsMapper.toOrderOfComponents(dto)));
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasAnyAuthority('ROLE_ADMIN')")
    public OrderOfComponentsDTOResponse delete(@PathVariable UUID id) {
        return orderOfComponentsMapper.toDTO(orderOfComponentsService.delete(id));
    }

}
