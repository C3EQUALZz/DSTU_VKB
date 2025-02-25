package com.example.repairserviceapp.entities;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "components_order")
@Setter
@Getter
@ToString
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class OrderOfComponents extends BaseOrderOfComponents {

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "component_code", referencedColumnName = "components_code")
    private ComponentsWarehouse componentsWarehouse;

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "execution_code", referencedColumnName = "ex_code")
    private ExecutionOfOrder executionOfOrder;

}
