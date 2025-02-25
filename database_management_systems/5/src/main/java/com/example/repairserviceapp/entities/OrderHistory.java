package com.example.repairserviceapp.entities;

import jakarta.persistence.Entity;
import jakarta.persistence.Table;

@Entity
@Table(name = "orders_history")
public class OrderHistory extends Order {
}
