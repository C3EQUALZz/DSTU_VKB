package com.example.repairserviceapp.controllers;

import com.example.repairserviceapp.DTOs.master.MasterDTORequest;
import com.example.repairserviceapp.DTOs.master.MasterDTOResponse;
import com.example.repairserviceapp.entities.Master;
import com.example.repairserviceapp.mappers.MasterMapper;
import com.example.repairserviceapp.services.MastersService;
import jakarta.validation.Valid;
import lombok.AllArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;


@RestController
@RequestMapping("/api/master")
@AllArgsConstructor(onConstructor = @__(@Autowired))
public class MastersController extends BaseController {

    private final MastersService mastersService;
    private final MasterMapper masterMapper;

    @GetMapping("")
    public List<MasterDTOResponse> readAll() {
        return mastersService.readAll().stream().map(masterMapper::toMasterDTO).collect(Collectors.toList());
    }

    @GetMapping("/{id}")
    public MasterDTOResponse read(@PathVariable UUID id) {
        return masterMapper.toMasterDTO(mastersService.read(id));
    }

    @PostMapping("")
    public MasterDTOResponse create(@RequestBody @Valid MasterDTORequest masterDTORequest, BindingResult bindingResult) {
        validate(bindingResult, "Create master failed");
        Master master = masterMapper.toMaster(masterDTORequest);
        return masterMapper.toMasterDTO(mastersService.create(master));
    }

    @PatchMapping("/{id}")
    public MasterDTOResponse update(@PathVariable UUID id, @RequestBody @Valid MasterDTORequest masterDTORequest, BindingResult bindingResult) {
        validate(bindingResult, "Update master failed");
        return masterMapper.toMasterDTO(mastersService.update(id, masterMapper.toMaster(masterDTORequest)));
    }

    @DeleteMapping("/{id}")
    public MasterDTOResponse delete(@PathVariable UUID id) {
        return masterMapper.toMasterDTO(mastersService.delete(id));
    }

}
