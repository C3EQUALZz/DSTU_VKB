package com.example.repairserviceapp.entities;

import jakarta.persistence.Entity;
import jakarta.persistence.Table;

@Entity
@Table(name = "clients_history")
public class ClientHistory extends Client {}
