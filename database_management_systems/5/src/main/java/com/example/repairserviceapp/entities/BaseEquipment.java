package com.example.repairserviceapp.entities;

import jakarta.persistence.Column;
import jakarta.persistence.Id;
import jakarta.persistence.MappedSuperclass;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.experimental.SuperBuilder;

import java.util.UUID;

@MappedSuperclass
@Getter
@Setter
@SuperBuilder
@AllArgsConstructor
@NoArgsConstructor
public abstract class BaseEquipment extends BaseEntity {
    @Id
    @Column(name = "eq_code")
    protected UUID id;

    @Column(name = "eq_name")
    protected String name;

    @Column(name = "eq_serial_number")
    protected String serialNumber;

    @Column(name = "model")
    protected String model;
}
