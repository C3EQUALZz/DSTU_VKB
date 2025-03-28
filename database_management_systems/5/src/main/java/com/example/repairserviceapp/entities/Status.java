package com.example.repairserviceapp.entities;

import jakarta.persistence.*;
import lombok.*;
import lombok.experimental.SuperBuilder;

import java.util.List;

@Entity
@Table(name = "orders_statuses")
@SuperBuilder
@Setter
@Getter
@ToString
@NoArgsConstructor
@AllArgsConstructor
public class Status extends BaseStatus {

    @OneToMany(mappedBy = "status")
    @ToString.Exclude
    private List<Order> orders;
}
