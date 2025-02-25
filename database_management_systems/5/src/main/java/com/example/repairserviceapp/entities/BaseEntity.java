package com.example.repairserviceapp.entities;

import io.hypersistence.utils.hibernate.type.range.PostgreSQLRangeType;
import io.hypersistence.utils.hibernate.type.range.Range;
import jakarta.persistence.Column;
import jakarta.persistence.MappedSuperclass;
import lombok.Getter;
import lombok.Setter;
import org.hibernate.annotations.Type;

import java.time.ZonedDateTime;

@MappedSuperclass
@Getter
@Setter
public abstract class BaseEntity {

    @Type(PostgreSQLRangeType.class)
    @Column(
            name="sys_period",
            columnDefinition = "tstzrange"
    )
    public Range<ZonedDateTime> localDateRange;
}
