package com.example.repairserviceapp.entities;

import jakarta.persistence.Entity;
import jakarta.persistence.Table;

@Entity
@Table(name = "components_order_history")
public class OrderOfComponentsHistory extends OrderOfComponents { }
