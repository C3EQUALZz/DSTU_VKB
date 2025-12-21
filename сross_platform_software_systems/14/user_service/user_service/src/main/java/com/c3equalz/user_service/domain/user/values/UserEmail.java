package com.c3equalz.user_service.domain.user.values;

import com.c3equalz.user_service.domain.common.values.BaseValueObject;
import com.c3equalz.user_service.domain.user.errors.BadUserEmailError;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

import java.util.regex.Pattern;

/**
 * User email value object with validation.
 */
@Getter
@RequiredArgsConstructor
public class UserEmail extends BaseValueObject {

    /**
     * Email pattern for validation.
     */
    private static final Pattern EMAIL_PATTERN = Pattern.compile(
        "^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$"
    );

    private final String value;

    @Override
    protected void validate() {
        if (value == null || value.isBlank()) {
            throw new BadUserEmailError("Email cannot be null or empty");
        }

        if (!EMAIL_PATTERN.matcher(value).matches()) {
            throw new BadUserEmailError("Invalid email format");
        }
    }
}

