package com.example.repairserviceapp.entities;

import jakarta.persistence.Entity;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import lombok.*;
import lombok.experimental.SuperBuilder;

import java.util.List;

@Entity
@Table(name = "posts")
@Setter
@Getter
@ToString
@SuperBuilder
@NoArgsConstructor
@AllArgsConstructor
public class Post extends BasePost {
    @OneToMany(mappedBy = "post")
    @ToString.Exclude
    private List<Master> masters;
}
