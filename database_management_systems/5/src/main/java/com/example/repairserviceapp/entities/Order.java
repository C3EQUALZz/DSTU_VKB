package com.example.repairserviceapp.entities;

import jakarta.persistence.*;
import lombok.*;
import lombok.experimental.SuperBuilder;

@Entity
@Table(name="orders")
@Getter
@Setter
@ToString
@SuperBuilder
@AllArgsConstructor
@NoArgsConstructor
public class Order extends BaseOrder {

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name="client_code", referencedColumnName = "client_code")
    private Client client;

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name="equipment_code", referencedColumnName = "eq_code")
    private Equipment equipment;

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name="master_code")
    private Master master;

    @ManyToOne(fetch=FetchType.EAGER)
    @JoinColumn(name="order_status", referencedColumnName="status_code")
    private Status status;

    @OneToOne(fetch = FetchType.EAGER, orphanRemoval=true)
    @JoinColumn(name="order_components_code", referencedColumnName = "co_code")
    private OrderOfComponents orderOfComponents;

}
