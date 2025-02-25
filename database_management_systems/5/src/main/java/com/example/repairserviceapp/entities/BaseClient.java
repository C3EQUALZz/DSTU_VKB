package com.example.repairserviceapp.entities;

import jakarta.persistence.Column;
import jakarta.persistence.Id;
import jakarta.persistence.MappedSuperclass;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.experimental.SuperBuilder;

import java.util.UUID;

@MappedSuperclass
@Getter
@Setter
@SuperBuilder
@AllArgsConstructor
@NoArgsConstructor
public abstract class BaseClient extends BaseEntity {
    @Id
    @Column(name = "client_code")
    protected UUID id;

    protected String surname;

    protected String name;

    protected String patronymic;

    @Column(name = "phone_number")
    protected String phoneNumber;

    protected String email;

    protected String password;

    protected String role;
}
