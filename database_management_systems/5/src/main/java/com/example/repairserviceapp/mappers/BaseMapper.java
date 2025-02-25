package com.example.repairserviceapp.mappers;

import io.hypersistence.utils.hibernate.type.range.Range;
import org.mapstruct.Mapper;

import java.time.OffsetDateTime;
import java.time.ZoneOffset;
import java.time.ZonedDateTime;

@Mapper(componentModel = "spring")
public abstract class BaseMapper {
    protected OffsetDateTime convertTime(Range<ZonedDateTime> zonedDateTimeRange) {
        return zonedDateTimeRange != null ? zonedDateTimeRange.lower().toOffsetDateTime().withOffsetSameInstant(ZoneOffset.UTC) : null;
    }
}
