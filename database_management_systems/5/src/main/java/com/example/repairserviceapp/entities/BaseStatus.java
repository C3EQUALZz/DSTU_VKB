package com.example.repairserviceapp.entities;

import jakarta.persistence.Column;
import jakarta.persistence.Id;
import jakarta.persistence.MappedSuperclass;
import lombok.*;
import lombok.experimental.SuperBuilder;

import java.util.UUID;

@MappedSuperclass
@Getter
@Setter
@ToString
@SuperBuilder
@AllArgsConstructor
@NoArgsConstructor
public abstract class BaseStatus extends BaseEntity {
    @Id
    @Column(name = "status_code")
    private UUID id;

    @Column(name = "status_name")
    private String name;
}
