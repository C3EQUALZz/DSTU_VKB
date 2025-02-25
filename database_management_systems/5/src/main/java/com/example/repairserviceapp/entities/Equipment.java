package com.example.repairserviceapp.entities;

import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import lombok.*;
import lombok.experimental.SuperBuilder;

import java.util.List;

@Entity
@Table(name = "equipments")
@Getter
@Setter
@ToString
@SuperBuilder
@AllArgsConstructor
@NoArgsConstructor
public class Equipment extends BaseEquipment {

    @OneToMany(fetch = FetchType.EAGER, mappedBy = "equipment")
    private List<Order> orders;
}
