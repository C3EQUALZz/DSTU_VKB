package com.example.repairserviceapp.entities;

import jakarta.persistence.Column;
import jakarta.persistence.Id;
import jakarta.persistence.MappedSuperclass;
import lombok.*;
import lombok.experimental.SuperBuilder;

import java.util.UUID;

@MappedSuperclass
@Getter
@Setter
@ToString
@SuperBuilder
@AllArgsConstructor
@NoArgsConstructor
public abstract class BasePost extends BaseEntity {
    @Id
    @Column(name = "post_code")
    private UUID id;

    @Column(name = "post_name")
    private String postName;
}
