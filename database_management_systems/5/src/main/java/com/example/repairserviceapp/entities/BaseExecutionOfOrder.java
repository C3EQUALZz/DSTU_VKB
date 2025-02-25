package com.example.repairserviceapp.entities;

import jakarta.persistence.Column;
import jakarta.persistence.Id;
import jakarta.persistence.MappedSuperclass;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.experimental.SuperBuilder;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.UUID;

@MappedSuperclass
@Getter
@Setter
@SuperBuilder
@AllArgsConstructor
@NoArgsConstructor
public abstract class BaseExecutionOfOrder extends BaseEntity {
    @Id
    @Column(name = "ex_code")
    protected UUID id;

    @Column(name = "type_of_work")
    protected String typeOfWork;

    @Column(name = "ex_cost")
    protected BigDecimal exCost;

    @Column(name = "components_cost")
    protected BigDecimal componentsCost;

    @Column(name = "ex_date")
    protected LocalDate executionDate;

    @Column(name = "total_cost")
    protected BigDecimal totalCost;
}
