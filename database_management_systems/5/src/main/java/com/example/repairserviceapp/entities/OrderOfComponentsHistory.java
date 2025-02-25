package com.example.repairserviceapp.entities;

import jakarta.persistence.*;
import lombok.*;

import java.util.UUID;

@Entity
@Table(name = "components_order_history")
@Setter
@Getter
@ToString
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class OrderOfComponentsHistory extends BaseOrderOfComponents {

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "component_code", referencedColumnName = "components_code")
    private ComponentsWarehouseHistory componentsWarehouse;

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "execution_code", referencedColumnName = "ex_code")
    private ExecutionOfOrderHistory executionOfOrder;

    @Column(name = "component_code", insertable = false, updatable = false)
    private UUID componentCode;

    @Column(name = "execution_code", insertable = false, updatable = false)
    private UUID executionCode;
}
