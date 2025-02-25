package com.example.repairserviceapp.entities;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import java.util.List;

@Entity
@Table(name = "orders_statuses")
@Inheritance(strategy = InheritanceType.TABLE_PER_CLASS)
@Setter
@Getter
@ToString
public class Status extends BaseStatus {

    @OneToMany(mappedBy = "status")
    @ToString.Exclude
    private List<Order> orders;
}
