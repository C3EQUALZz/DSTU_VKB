package com.c3equalz.user_service.application.common.query_params.user;

import com.c3equalz.user_service.application.common.query_params.SortingOrder;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Getter
public class UserListSorting {
    private final UserSortingField sortingField;
    private final SortingOrder sortingOrder;
}
