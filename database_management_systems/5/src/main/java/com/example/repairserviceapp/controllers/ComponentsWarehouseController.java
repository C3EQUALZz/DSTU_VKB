package com.example.repairserviceapp.controllers;

import com.example.repairserviceapp.DTOs.componentsWarehouse.ComponentsWarehouseDTORequest;
import com.example.repairserviceapp.DTOs.componentsWarehouse.ComponentsWarehouseDTOResponse;
import com.example.repairserviceapp.mappers.ComponentsWarehouseMapper;
import com.example.repairserviceapp.services.ComponentsWarehouseService;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.AllArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@Tag(name = "Контроллер для управления компонентами на складе", description = "Здесь есть все операции CRUD для компонентов на складе")
@RestController
@RequestMapping("/api/components-warehouse")
@AllArgsConstructor(onConstructor = @__(@Autowired))
public class ComponentsWarehouseController extends BaseController {

    private ComponentsWarehouseService componentsWarehouseService;
    private ComponentsWarehouseMapper componentsWarehouseMapper;

    @GetMapping("")
    public List<ComponentsWarehouseDTOResponse> readAll() {
        return componentsWarehouseService.readAll()
                .stream()
                .map(elem -> componentsWarehouseMapper.toDTO(elem))
                .toList();
    }

    @GetMapping("/{id}")
    public ComponentsWarehouseDTOResponse read(
            @PathVariable("id") @Parameter(description = "Уникальный идентификатор набора компонентов на складе", required = true) UUID id
    ) {
        return componentsWarehouseMapper.toDTO(componentsWarehouseService.read(id));
    }

    @PostMapping("")
    public ComponentsWarehouseDTOResponse create(
            @RequestBody @Valid ComponentsWarehouseDTORequest componentsWarehouse,
            BindingResult bindingResult
    ) {
        validate(bindingResult, "Create components warehouse failed");
        return componentsWarehouseMapper.toDTO(
                componentsWarehouseService.create(
                        componentsWarehouseMapper.toEntity(componentsWarehouse)
                )
        );
    }

    @PatchMapping("/{id}")
    public ComponentsWarehouseDTOResponse update(
            @PathVariable("id") UUID id,
            @RequestBody @Valid ComponentsWarehouseDTORequest componentsWarehouse,
            BindingResult bindingResult
    ) {
        validate(bindingResult, "Update components warehouse failed");
        return componentsWarehouseMapper.toDTO(componentsWarehouseService.update(id, componentsWarehouseMapper.toEntity(componentsWarehouse)));
    }

    @DeleteMapping("/{id}")
    public ComponentsWarehouseDTOResponse delete(@PathVariable("id") UUID id) {
        return componentsWarehouseMapper.toDTO(componentsWarehouseService.delete(id));
    }
}
