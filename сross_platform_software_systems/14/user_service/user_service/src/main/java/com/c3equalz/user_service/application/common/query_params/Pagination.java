package com.c3equalz.user_service.application.common.query_params;

import com.c3equalz.user_service.application.errors.pagination.LimitCantBeNegativeError;
import com.c3equalz.user_service.application.errors.pagination.OffsetCantBeNegativeError;
import lombok.Getter;

@Getter
public class Pagination {
    private final int offset;
    private final int limit;

    public Pagination(int offset, int limit) {
        if (offset < 0) {
            throw new OffsetCantBeNegativeError("Offset cant be negative, got " + offset);
        }

        if (limit < 0) {
            throw new LimitCantBeNegativeError("Limit cant be negative, got " + limit);
        }

        this.offset = offset;
        this.limit = limit;
    }

}
