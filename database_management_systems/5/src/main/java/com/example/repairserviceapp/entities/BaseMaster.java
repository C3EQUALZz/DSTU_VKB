package com.example.repairserviceapp.entities;

import jakarta.persistence.Column;
import jakarta.persistence.Id;
import jakarta.persistence.MappedSuperclass;
import lombok.*;
import lombok.experimental.SuperBuilder;

import java.time.LocalDate;
import java.util.UUID;

@MappedSuperclass
@Getter
@Setter
@SuperBuilder
@AllArgsConstructor
@NoArgsConstructor
public abstract class BaseMaster extends BaseEntity {
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

    @Override
    public String toString() {
        return "{" +
                "id =" + id +
                ", surname ='" + surname + '\'' +
                ", name ='" + name + '\'' +
                ", patronymic ='" + patronymic + '\'' +
                ", address ='" + address + '\'' +
                ", phoneNumber ='" + phoneNumber + '\'' +
                ", dateOfEmployment =" + dateOfEmployment +
                " }";
    }
}
