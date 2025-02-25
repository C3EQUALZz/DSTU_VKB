package com.example.repairserviceapp.entities;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

@Entity
@Table(name = "masters_list")
@Inheritance(strategy = InheritanceType.TABLE_PER_CLASS)
@Setter
@Getter
@ToString
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Master extends BaseEntity {

    @Id
    @Column(name = "master_code")
    private UUID id;

    @Column(name = "surname")
    private String surname;

    @Column(name = "name")
    private String name;

    @Column(name = "patronymic")
    private String patronymic;

    @Column(name = "address")
    private String address;

    @Column(name = "phone_number")
    private String phoneNumber;

    @Column(name = "date_of_employment")
    private LocalDate dateOfEmployment;

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "post_code", referencedColumnName = "post_code")
    private Post post;

    @OneToMany(mappedBy = "master")
    @ToString.Exclude
    private List<Order> orders;
}
