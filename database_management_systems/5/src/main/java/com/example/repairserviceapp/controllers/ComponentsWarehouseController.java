package com.example.repairserviceapp.controllers;

import com.example.repairserviceapp.DTOs.componentsWarehouse.ComponentsWarehouseDTORequest;
import com.example.repairserviceapp.DTOs.componentsWarehouse.ComponentsWarehouseDTOResponse;
import com.example.repairserviceapp.mappers.ComponentsWarehouseMapper;
import com.example.repairserviceapp.services.ComponentsWarehouseService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.AllArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
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
    @PreAuthorize("hasAnyAuthority('ROLE_USER', 'ROLE_ADMIN')")
    public List<ComponentsWarehouseDTOResponse> readAll() {
        return componentsWarehouseService.readAll()
                .stream()
                .map(elem -> componentsWarehouseMapper.toDTO(elem))
                .toList();
    }

    @Operation(
            summary = "Создание одного компонента на складе",
            description = "Позволяет создать отдельный компонент на складе"
    )
    @GetMapping("/{id}")
    @PreAuthorize("hasAnyAuthority('ROLE_USER', 'ROLE_ADMIN')")
    public ComponentsWarehouseDTOResponse read(
            @PathVariable("id") @Parameter(description = "Уникальный идентификатор набора компонентов на складе", required = true) UUID id
    ) {
        return componentsWarehouseMapper.toDTO(componentsWarehouseService.read(id));
    }

    @Operation(
            summary = "Создание отдельного заказа на складе",
            description = "Позволяет обновлять данные об отдельном заказе на складе, зная его id. "
    )
    @PostMapping("")
    @PreAuthorize("hasAnyAuthority('ROLE_ADMIN')")
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

    @Operation(
            summary = "Обновление данных отдельного заказа на складе",
            description = "Позволяет обновлять данные об отдельном заказе на складе, зная его id. "
    )
    @PatchMapping("/{id}")
    @PreAuthorize("hasAnyAuthority('ROLE_ADMIN')")
    public ComponentsWarehouseDTOResponse update(
            @PathVariable("id") UUID id,
            @RequestBody @Valid ComponentsWarehouseDTORequest componentsWarehouse,
            BindingResult bindingResult
    ) {
        validate(bindingResult, "Update components warehouse failed");
        return componentsWarehouseMapper.toDTO(componentsWarehouseService.update(id, componentsWarehouseMapper.toEntity(componentsWarehouse)));
    }

    @Operation(
            summary = "Удаление данных об отдельном компоненте на складе",
            description = "Позволяет удалять данные об отдельном компоненте на складе, зная его id"
    )
    @DeleteMapping("/{id}")
    @PreAuthorize("hasAnyAuthority('ROLE_ADMIN')")
    public ComponentsWarehouseDTOResponse delete(@PathVariable("id") UUID id) {
        return componentsWarehouseMapper.toDTO(componentsWarehouseService.delete(id));
    }
}
