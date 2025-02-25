package com.example.repairserviceapp.entities;

import jakarta.persistence.Entity;
import jakarta.persistence.Table;

@Entity
@Table(name="order_executions_history")
public class ExecutionOfOrderHistory extends ExecutionOfOrder { }
