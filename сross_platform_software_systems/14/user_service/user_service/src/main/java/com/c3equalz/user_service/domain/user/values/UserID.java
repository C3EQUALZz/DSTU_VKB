package com.c3equalz.user_service.domain.user.values;

import com.c3equalz.user_service.domain.common.values.BaseValueObject;
import com.c3equalz.user_service.domain.user.errors.BadUserIDError;
import lombok.AllArgsConstructor;
import lombok.Getter;

import java.util.UUID;

@Getter
@AllArgsConstructor
public class UserID extends BaseValueObject {
    private final UUID value;

    @Override
    protected void validate() {
        if (value == null) {
            throw new BadUserIDError("User ID cant be null value");
        }
    }
}
