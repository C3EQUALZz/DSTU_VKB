package com.example.repairserviceapp.controllers;

import com.example.repairserviceapp.DTOs.order.OrderDTORequest;
import com.example.repairserviceapp.DTOs.order.OrderDTOResponse;
import com.example.repairserviceapp.mappers.OrderMapper;
import com.example.repairserviceapp.services.OrdersService;
import jakarta.validation.Valid;
import lombok.AllArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

@RestController
@RequestMapping("api/order")
@AllArgsConstructor(onConstructor = @__(@Autowired))
public class OrdersController extends BaseController {

    private OrdersService ordersService;
    private OrderMapper orderMapper;

    @GetMapping("")
    public List<OrderDTOResponse> readAll() {
        return ordersService.readAll().stream().map(order -> orderMapper.toDTO(order)).collect(Collectors.toList());
    }

    @GetMapping("/{id}")
    public OrderDTOResponse read(@PathVariable UUID id) {
        return orderMapper.toDTO(ordersService.read(id));
    }

    @PostMapping("")
    public OrderDTOResponse create(@RequestBody @Valid OrderDTORequest orderDTORequest, BindingResult bindingResult) {
        validate(bindingResult, "Create order failed");
        return orderMapper.toDTO(ordersService.create(orderMapper.toOrder(orderDTORequest)));
    }

    @PatchMapping("/{id}")
    public OrderDTOResponse update(@PathVariable UUID id, @RequestBody @Valid OrderDTORequest orderDTORequest, BindingResult bindingResult) {
        validate(bindingResult, "Update order failed");
        return orderMapper.toDTO(ordersService.update(id, orderMapper.toOrder(orderDTORequest)));
    }

    @DeleteMapping("/{id}")
    public OrderDTOResponse delete(@PathVariable UUID id) {
        return orderMapper.toDTO(ordersService.delete(id));
    }


}
