package com.example.repairserviceapp.entities;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import java.util.List;
import java.util.UUID;

@Entity
@Table(name = "orders_statuses")
@Inheritance(strategy = InheritanceType.TABLE_PER_CLASS)
@Setter
@Getter
@ToString
public class Status extends BaseEntity {

    @Id
    @Column(name = "status_code")
    private UUID id;

    @Column(name = "status_name")
    private String name;

    @OneToMany(mappedBy = "status")
    @ToString.Exclude
    private List<Order> orders;
}
