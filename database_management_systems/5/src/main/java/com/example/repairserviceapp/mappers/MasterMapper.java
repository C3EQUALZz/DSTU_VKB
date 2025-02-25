package com.example.repairserviceapp.mappers;

import com.example.repairserviceapp.DTOs.master.HistoryMasterDTOResponse;
import com.example.repairserviceapp.DTOs.master.MasterDTORequest;
import com.example.repairserviceapp.DTOs.master.MasterDTOResponse;
import com.example.repairserviceapp.entities.Master;
import com.example.repairserviceapp.entities.MasterHistory;
import com.example.repairserviceapp.services.PostsService;
import lombok.Setter;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.springframework.beans.factory.annotation.Autowired;


@Mapper(componentModel = "spring")
public abstract class MasterMapper extends BaseMapper {

    @Setter(onMethod = @__(@Autowired))
    protected PostsService postsService;

    @Mapping(target = "post", expression = "java(postsService.read(masterDTORequest.postId()))")
    public abstract Master toMaster(MasterDTORequest masterDTORequest);

    @Mapping(target = "postId", expression = "java(master.getPost().getId())")
    public abstract MasterDTOResponse toMasterDTO(Master master);

    @Mapping(target = "postId", expression = "java(master.getPost().getId())")
    @Mapping(target = "offsetDateTime", expression = "java(convertTime(master.getLocalDateRange()))")
    public abstract HistoryMasterDTOResponse toHistoryDTO(Master master);

    @Mapping(target = "postId", expression = "java(master.getPostCode())")
    @Mapping(target = "offsetDateTime", expression = "java(convertTime(master.getLocalDateRange()))")
    public abstract HistoryMasterDTOResponse toHistoryDTO(MasterHistory master);
}

