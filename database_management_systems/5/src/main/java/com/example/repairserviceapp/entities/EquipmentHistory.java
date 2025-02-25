package com.example.repairserviceapp.entities;

import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import lombok.*;

import java.util.List;

@Entity
@Table(name = "equipments_history")
@Getter
@Setter
@ToString
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class EquipmentHistory extends BaseEquipment {
    @OneToMany(fetch = FetchType.EAGER, mappedBy = "equipment")
    private List<OrderHistory> orders;
}
