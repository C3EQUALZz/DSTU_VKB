package com.example.repairserviceapp.mappers;

import com.example.repairserviceapp.DTOs.client.ClientDTORequest;
import com.example.repairserviceapp.DTOs.client.ClientDTOResponse;
import com.example.repairserviceapp.DTOs.client.HistoryClientDTOResponse;
import com.example.repairserviceapp.entities.BaseClient;
import com.example.repairserviceapp.entities.Client;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring")
public abstract class ClientsMapper extends BaseMapper {

    public abstract Client toClient(ClientDTORequest clientDTORequest);

    public abstract ClientDTOResponse toDTO(Client client);

    @Mapping(target = "offsetDateTime", expression = "java(convertTime(baseClient.getLocalDateRange()))")
    public abstract HistoryClientDTOResponse toHistoryDTO(BaseClient baseClient);
}
