package com.example.repairserviceapp.entities;

import jakarta.persistence.Entity;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import lombok.*;

import java.util.List;

@Entity
@Table(name = "posts")
@Setter
@Getter
@ToString
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Post extends BasePost {
    @OneToMany(mappedBy = "post")
    @ToString.Exclude
    private List<Master> masters;
}
