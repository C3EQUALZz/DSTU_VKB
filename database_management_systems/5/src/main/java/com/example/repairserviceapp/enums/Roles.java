package com.example.repairserviceapp.enums;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public enum Roles {

    ADMIN("ADMIN"),

    USER("USER");

    private final String value;


}
