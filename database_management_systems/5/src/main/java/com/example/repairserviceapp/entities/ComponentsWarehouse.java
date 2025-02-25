package com.example.repairserviceapp.entities;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import java.math.BigDecimal;
import java.util.List;
import java.util.UUID;

@Entity
@Table(name = "components_warehouse")
@Inheritance(strategy = InheritanceType.TABLE_PER_CLASS)
@Getter
@Setter
@ToString
public class ComponentsWarehouse extends BaseEntity {

    @Id
    @Column(name = "components_code")
    private UUID id;

    @Column(name = "component_name")
    private String componentName;

    @Column(name = "components_amount")
    private Integer componentsAmount;

    @Column(name = "unit_cost")
    private BigDecimal unitCost;

    @OneToMany(fetch = FetchType.EAGER, mappedBy = "componentsWarehouse")
    @ToString.Exclude
    private List<OrderOfComponents> ordersOfComponents;
}
