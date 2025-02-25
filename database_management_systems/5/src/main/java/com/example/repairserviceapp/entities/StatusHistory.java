package com.example.repairserviceapp.entities;

import jakarta.persistence.Entity;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import lombok.*;

import java.util.List;

@Entity
@Table(name = "orders_statuses_history")
@Setter
@Getter
@ToString
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class StatusHistory extends BaseStatus {

    @OneToMany(mappedBy = "status")
    @ToString.Exclude
    private List<OrderHistory> orders;
}
