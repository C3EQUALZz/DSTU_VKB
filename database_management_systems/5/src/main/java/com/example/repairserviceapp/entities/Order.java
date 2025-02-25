package com.example.repairserviceapp.entities;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import java.time.LocalDate;
import java.util.UUID;

@Entity
@Table(name="orders")
@Inheritance(strategy = InheritanceType.TABLE_PER_CLASS)
@Setter
@Getter
@ToString
public class Order extends BaseEntity {

    @Id
    @Column(name="order_code")
    private UUID id;

    @Column(name="order_date")
    private LocalDate date;

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
