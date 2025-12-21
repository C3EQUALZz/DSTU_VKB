package com.c3equalz.user_service.application.common.query_params.user;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Getter
public enum UserSortingField {
    NAME("name"),
    ROLE("role"),
    ID("id"),
    EMAIL("email");

    private final String value;
}
