package com.example.repairserviceapp.entities;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import java.util.List;
import java.util.UUID;

@Entity
@Table(name = "equipments")
@Inheritance(strategy = InheritanceType.TABLE_PER_CLASS)
@ToString
@Getter
@Setter
public class Equipment extends BaseEntity {

    @Id
    @Column(name = "eq_code")
    private UUID id;

    @Column(name = "eq_name")
    private String name;

    @Column(name = "eq_serial_number")
    private String serialNumber;

    @Column(name = "model")
    private String model;

    @OneToMany(fetch = FetchType.EAGER, mappedBy = "equipment")
    private List<Order> orders;
}
