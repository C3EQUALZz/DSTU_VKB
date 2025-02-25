package com.example.repairserviceapp.mappers;

import com.example.repairserviceapp.DTOs.client.ClientDTORequest;
import com.example.repairserviceapp.DTOs.client.ClientDTOResponse;
import com.example.repairserviceapp.DTOs.client.HistoryClientDTOResponse;
import com.example.repairserviceapp.entities.Client;
import com.example.repairserviceapp.entities.ClientHistory;
import org.mapstruct.Mapper;

import java.time.OffsetDateTime;
import java.time.ZoneOffset;
import java.util.UUID;

@Mapper(componentModel = "spring")
public abstract class ClientsMapper {

    public abstract Client toClient(ClientDTORequest clientDTORequest);

    public abstract ClientDTOResponse toDTO(Client client);

    public HistoryClientDTOResponse toDTO(ClientHistory clientDTO) {
        if (clientDTO == null) {
            return null;
        }

        UUID id;
        String surname;
        String name;
        String patronymic;
        String phoneNumber;
        OffsetDateTime offsetDateTime;

        id = clientDTO.getId();
        surname = clientDTO.getSurname();
        name = clientDTO.getName();
        patronymic = clientDTO.getPatronymic();
        phoneNumber = clientDTO.getPhoneNumber();
        offsetDateTime = clientDTO.getLocalDateRange().lower().toOffsetDateTime().withOffsetSameInstant(ZoneOffset.UTC);

        return new HistoryClientDTOResponse(id, surname, name, patronymic, phoneNumber, offsetDateTime);
    }
}
