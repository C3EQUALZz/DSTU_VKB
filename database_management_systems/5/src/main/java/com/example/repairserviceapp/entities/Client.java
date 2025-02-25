package com.example.repairserviceapp.entities;

import jakarta.persistence.*;
import lombok.*;

import java.util.List;
import java.util.UUID;

@Entity
@Table(name = "clients")
@Inheritance(strategy = InheritanceType.TABLE_PER_CLASS)
@Getter
@Setter
@ToString
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Client extends BaseEntity {

    @Id
    @Column(name = "client_code")
    private UUID id;

    private String surname;

    private String name;

    private String patronymic;

    @Column(name = "phone_number")
    private String phoneNumber;

    private String email;

    private String password;

    private String role;

    @OneToMany(fetch = FetchType.EAGER, mappedBy = "client", cascade = CascadeType.ALL)
    @ToString.Exclude
    private List<Order> orders;
}