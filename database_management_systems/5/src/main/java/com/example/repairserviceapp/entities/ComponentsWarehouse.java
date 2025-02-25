package com.example.repairserviceapp.entities;

import jakarta.persistence.*;
import lombok.*;
import lombok.experimental.SuperBuilder;

import java.util.List;

@Entity
@Table(name = "components_warehouse")
@Getter
@Setter
@SuperBuilder
@AllArgsConstructor
@NoArgsConstructor
public class ComponentsWarehouse extends BaseComponentsWarehouse {
    @OneToMany(fetch = FetchType.EAGER, mappedBy = "componentsWarehouse")
    @ToString.Exclude
    private List<OrderOfComponents> ordersOfComponents;

    @Override
    public String toString() {
        return "ComponentsWarehouse" + super.toString();
    }
}
