package com.example.repairserviceapp.entities;

import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import lombok.*;

import java.util.List;

@Entity
@Table(name = "components_warehouse_history")
@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class ComponentsWarehouseHistory extends BaseComponentsWarehouse {
    @OneToMany(fetch = FetchType.EAGER, mappedBy = "componentsWarehouse")
    @ToString.Exclude
    private List<OrderOfComponentsHistory> ordersOfComponents;

    @Override
    public String toString() {
        return "ComponentsWarehouseHistory" + super.toString();
    }
}
