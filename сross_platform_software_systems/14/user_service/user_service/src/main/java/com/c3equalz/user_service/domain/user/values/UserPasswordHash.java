package com.c3equalz.user_service.domain.user.values;

import com.c3equalz.user_service.domain.common.values.BaseValueObject;
import com.c3equalz.user_service.domain.user.errors.EmptyPasswordWasProvidedError;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
public class UserPasswordHash extends BaseValueObject {
    private final byte[] value;

    @Override
    protected void validate() {
        if (value.length == 0) {
            throw new EmptyPasswordWasProvidedError(
                    "hash value cant be empty"
            );
        }
    }
}
