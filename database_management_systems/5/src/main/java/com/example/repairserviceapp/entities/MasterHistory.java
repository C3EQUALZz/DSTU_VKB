package com.example.repairserviceapp.entities;

import jakarta.persistence.*;
import lombok.*;
import lombok.experimental.SuperBuilder;

import java.util.List;
import java.util.UUID;

@Entity
@Table(name = "masters_list_history")
@Getter
@Setter
@SuperBuilder
@AllArgsConstructor
@NoArgsConstructor
public class MasterHistory extends BaseMaster {
    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "post_code", referencedColumnName = "post_code")
    private PostHistory post;

    @OneToMany(mappedBy = "master")
    @ToString.Exclude
    private List<OrderHistory> orders;

    @Column(name = "post_code", insertable = false, updatable = false)
    private UUID postCode;

    @Override
    public String toString() {
        return "MasterHistory" + super.toString();
    }
}
