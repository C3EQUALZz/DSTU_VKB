package com.example.repairserviceapp.entities;

import jakarta.persistence.Entity;
import jakarta.persistence.Table;

@Entity
@Table(name = "components_warehouse_history")
public class ComponentsWarehouseHistory extends ComponentsWarehouse { }
