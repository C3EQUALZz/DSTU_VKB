package com.c3equalz.user_service.application.common.query_params.user;

import com.c3equalz.user_service.application.common.query_params.Pagination;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Getter
public class UserListParams {
    private final Pagination pagination;
    private final UserListSorting userListSorting;
}
