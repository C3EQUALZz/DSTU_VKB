package com.example.repairserviceapp.mappers;

import com.example.repairserviceapp.DTOs.master.HistoryMasterDTOResponse;
import com.example.repairserviceapp.DTOs.master.MasterDTORequest;
import com.example.repairserviceapp.DTOs.master.MasterDTOResponse;
import com.example.repairserviceapp.entities.Master;
import com.example.repairserviceapp.services.PostsService;
import lombok.Setter;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.springframework.beans.factory.annotation.Autowired;

import java.time.LocalDate;
import java.time.OffsetDateTime;
import java.time.ZoneOffset;
import java.util.UUID;


@Mapper(componentModel = "spring")
public abstract class MasterMapper {

    @Setter(onMethod = @__(@Autowired))
    protected PostsService postsService;

    @Mapping(target = "post", expression = "java(postsService.read(masterDTORequest.postId()))")
    public abstract Master toMaster(MasterDTORequest masterDTORequest);

    @Mapping(target = "postId", expression = "java(master.getPost().getId())")
    public abstract MasterDTOResponse toMasterDTO(Master master);

    public HistoryMasterDTOResponse toDTO(Master master) {
        if (master == null) {
            return null;
        }

        UUID id;
        String surname;
        String name;
        String patronymic;
        String address;
        LocalDate dateOfEmployment;
        String phoneNumber;
        UUID postId;
        OffsetDateTime offsetDateTime;

        id = master.getId();
        surname = master.getSurname();
        name = master.getName();
        patronymic = master.getPatronymic();
        address = master.getAddress();
        dateOfEmployment = master.getDateOfEmployment();
        phoneNumber = master.getPhoneNumber();
        postId = master.getPost().getId();
        offsetDateTime = master.getLocalDateRange().lower().toOffsetDateTime().withOffsetSameInstant(ZoneOffset.UTC);

        return new HistoryMasterDTOResponse(
                id,
                surname,
                name,
                patronymic,
                address,
                phoneNumber,
                dateOfEmployment,
                postId,
                offsetDateTime
        );
    }
}

