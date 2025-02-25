package com.example.repairserviceapp.controllers;

import com.example.repairserviceapp.DTOs.master.MasterDTORequest;
import com.example.repairserviceapp.DTOs.master.MasterDTOResponse;
import com.example.repairserviceapp.entities.Master;
import com.example.repairserviceapp.mappers.MasterMapper;
import com.example.repairserviceapp.services.MastersService;
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

@Tag(name = "Контроллер для управления мастерами", description = "Здесь есть все операции CRUD для мастера")
@RestController
@RequestMapping("/api/master")
@AllArgsConstructor(onConstructor = @__(@Autowired))
public class MastersController extends BaseController {

    private final MastersService mastersService;
    private final MasterMapper masterMapper;

    @Operation(
            summary = "Просмотр данных всех мастеров",
            description = "Позволяет просмотреть всех мастеров."
    )
    @GetMapping("")
    @PreAuthorize("hasAnyAuthority('ROLE_USER', 'ROLE_ADMIN')")
    public List<MasterDTOResponse> readAll() {
        return mastersService.readAll().stream().map(masterMapper::toMasterDTO).collect(Collectors.toList());
    }

    @Operation(
            summary = "Просмотр данных об одном мастере",
            description = "Позволяет посмотреть данные об одном мастере, зная его уникальный идентификатор. "
    )
    @GetMapping("/{id}")
    @PreAuthorize("hasAnyAuthority('ROLE_USER', 'ROLE_ADMIN')")
    public MasterDTOResponse read(@PathVariable UUID id) {
        return masterMapper.toMasterDTO(mastersService.read(id));
    }

    @Operation(
            summary = "Создание одного мастера",
            description = "Позволяет создать одного отдельного мастера"
    )
    @PostMapping("")
    @PreAuthorize("hasAnyAuthority('ROLE_ADMIN')")
    public MasterDTOResponse create(@RequestBody @Valid MasterDTORequest masterDTORequest, BindingResult bindingResult) {
        validate(bindingResult, "Create master failed");
        Master master = masterMapper.toMaster(masterDTORequest);
        return masterMapper.toMasterDTO(mastersService.create(master));
    }

    @Operation(
            summary = "Обновление данных отдельного мастера",
            description = "Позволяет обновлять данные об отдельном мастере, зная его id. "
    )
    @PatchMapping("/{id}")
    @PreAuthorize("hasAnyAuthority('ROLE_ADMIN')")
    public MasterDTOResponse update(@PathVariable UUID id, @RequestBody @Valid MasterDTORequest masterDTORequest, BindingResult bindingResult) {
        validate(bindingResult, "Update master failed");
        return masterMapper.toMasterDTO(mastersService.update(id, masterMapper.toMaster(masterDTORequest)));
    }

    @Operation(
            summary = "Удаление данных отдельного мастера",
            description = "Позволяет удалять данные об отдельном мастере, зная его id"
    )
    @DeleteMapping("/{id}")
    @PreAuthorize("hasAnyAuthority('ROLE_ADMIN')")
    public MasterDTOResponse delete(@PathVariable UUID id) {
        return masterMapper.toMasterDTO(mastersService.delete(id));
    }

}
