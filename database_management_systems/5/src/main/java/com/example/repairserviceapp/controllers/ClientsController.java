package com.example.repairserviceapp.controllers;

import com.example.repairserviceapp.DTOs.client.ClientDTORequest;
import com.example.repairserviceapp.DTOs.client.ClientDTOResponse;
import com.example.repairserviceapp.enums.Roles;
import com.example.repairserviceapp.mappers.ClientsMapper;
import com.example.repairserviceapp.services.ClientsService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

@Slf4j
@Tag(name = "Контроллер для управления клиентами", description = "Здесь есть все операции CRUD для клиента")
@RestController
@RequestMapping("/api/client")
@AllArgsConstructor(onConstructor = @__(@Autowired))
public class ClientsController extends BaseController {

    private ClientsService clientsService;
    private ClientsMapper clientsMapper;

    @Operation(
            summary = "Просмотр данных всех пользователей",
            description = "Позволяет просмотреть всех пользователей."
    )
    @GetMapping("")
    @PreAuthorize("hasAnyAuthority('ROLE_USER', 'ROLE_ADMIN')")
    public List<ClientDTOResponse> readAll() {
        return clientsService
                .readAll()
                .stream()
                .map(client -> clientsMapper.toDTO(client))
                .collect(Collectors.toList());
    }

    @Operation(
            summary = "Просмотр данных об одном пользователя",
            description = "Позволяет посмотреть данные об одном пользователе, зная его уникальный идентификатор. "
    )
    @GetMapping("/{id}")
    @PreAuthorize("hasAnyAuthority('ROLE_USER', 'ROLE_ADMIN')")
    public ClientDTOResponse read(
            @PathVariable("id") @Parameter(description = "Уникальный идентификатор клиента", required = true) UUID id
    ) {
        return clientsMapper.toDTO(clientsService.read(id));
    }

    @Operation(
            summary = "Создание одного пользователя",
            description = "Позволяет создать одного отдельного пользователя"
    )
    @PostMapping("")
//    @PreAuthorize("hasAnyAuthority('ROLE_USER')")
    public ClientDTOResponse create(@RequestBody @Valid ClientDTORequest clientDTORequest, BindingResult bindingResult) {
        return create(clientDTORequest, bindingResult, Roles.USER.getValue());
    }

    @Operation(
            summary = "Обновление данных отдельного пользователя",
            description = "Позволяет обновлять данные об отдельном пользователе, зная его id. "
    )
    @PatchMapping("/{id}")
    @PreAuthorize("hasAnyAuthority('ROLE_ADMIN')")
    public ClientDTOResponse update(
            @PathVariable("id") @Parameter(description = "Уникальный идентификатор клиента", required = true) UUID id,
            @RequestBody @Valid ClientDTORequest clientDTORequest,
            BindingResult bindingResult
    ) {
        validate(bindingResult, "Update client failed");
        return clientsMapper.toDTO(clientsService.update(id, clientsMapper.toClient(clientDTORequest)));
    }

    @Operation(
            summary = "Удаление данных об отдельном пользователе",
            description = "Позволяет удалять данные об отдельном пользователе, зная его id"
    )
    @DeleteMapping("/{id}")
    @PreAuthorize("hasAnyAuthority('ROLE_ADMIN')")
    public ClientDTOResponse delete(
            @PathVariable("id") @Parameter(description = "Уникальный идентификатор клиента", required = true) UUID id
    ) {
        return clientsMapper.toDTO(clientsService.delete(id));
    }


    @PostMapping("/create-admin")
    @PreAuthorize("hasAnyAuthority('ROLE_ADMIN')")
    public ClientDTOResponse createAdmin(@RequestBody @Valid ClientDTORequest clientDTORequest, BindingResult bindingResult) {
        return create(clientDTORequest, bindingResult, Roles.ADMIN.getValue());
    }

    private ClientDTOResponse create(ClientDTORequest clientDTORequest, BindingResult bindingResult, String role) {
        validate(bindingResult, String.format("Create %s failed", role));
        log.info("Create {} {}", role, clientDTORequest);
        return clientsMapper.toDTO(clientsService.create(clientsMapper.toClient(clientDTORequest), role));
    }
}
