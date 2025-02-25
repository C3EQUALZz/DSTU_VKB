package com.example.repairserviceapp.entities;

import jakarta.persistence.Column;
import jakarta.persistence.Id;
import jakarta.persistence.MappedSuperclass;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.experimental.SuperBuilder;

import java.math.BigDecimal;
import java.util.UUID;

@MappedSuperclass
@Getter
@Setter
@SuperBuilder
@AllArgsConstructor
@NoArgsConstructor
public abstract class BaseComponentsWarehouse extends BaseEntity {
    @Id
    @Column(name = "components_code")
    protected UUID id;

    @Column(name = "component_name")
    protected String componentName;

    @Column(name = "components_amount")
    protected Integer componentsAmount;

    @Column(name = "unit_cost")
    protected BigDecimal unitCost;

    @Override
    public String toString() {
        return "{" +
                "id=" + id +
                ", componentName='" + componentName + '\'' +
                ", componentsAmount=" + componentsAmount +
                ", unitCost=" + unitCost +
                '}';
    }
}
