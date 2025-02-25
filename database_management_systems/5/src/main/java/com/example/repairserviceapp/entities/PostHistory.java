package com.example.repairserviceapp.entities;

import jakarta.persistence.Entity;
import jakarta.persistence.Table;

@Entity
@Table(name = "posts_history")
public class PostHistory extends Post {
}
