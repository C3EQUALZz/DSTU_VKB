package com.example.repairserviceapp.entities;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import java.util.List;
import java.util.UUID;

@Entity
@Table(name = "posts")
@Inheritance(strategy = InheritanceType.TABLE_PER_CLASS)
@Setter
@Getter
@ToString
public class Post extends BaseEntity {

    @Id
    @Column(name = "post_code")
    private UUID id;

    @Column(name = "post_name")
    private String postName;

    @OneToMany(mappedBy="post")
    @ToString.Exclude
    private List<Master> masters;
}
