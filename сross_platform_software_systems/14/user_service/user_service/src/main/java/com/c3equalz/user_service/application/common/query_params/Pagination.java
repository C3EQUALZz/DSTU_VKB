package com.c3equalz.user_service.application.common.query_params;

import com.c3equalz.user_service.application.errors.OffsetCantBeNegativeError;
import lombok.Getter;

@Getter
public class Pagination {
    private final int offset;
    private final int limit;

    public Pagination(int offset, int limit) {
        if (offset < 0) {
            throw new OffsetCantBeNegativeError("");
        }

        if (limit < 0) {

        }

        this.offset = offset;
        this.limit = limit;
    }

}
