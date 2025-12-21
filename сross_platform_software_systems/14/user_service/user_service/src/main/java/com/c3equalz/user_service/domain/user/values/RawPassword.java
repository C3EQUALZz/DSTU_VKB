package com.c3equalz.user_service.domain.user.values;

import com.c3equalz.user_service.domain.common.values.BaseValueObject;
import com.c3equalz.user_service.domain.user.errors.EmptyPasswordWasProvidedError;
import com.c3equalz.user_service.domain.user.errors.WeakPasswordWasProvidedError;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

/**
 * Raw password value object with validation.
 * <p>
 * Validation rules:
 * <ul>
 *     <li>Cannot be empty or whitespace only</li>
 *     <li>Cannot contain only digits</li>
 *     <li>Must be between {@value MIN_PASSWORD_LENGTH} and {@value MAX_PASSWORD_LENGTH} characters</li>
 * </ul>
 */
@Getter
@RequiredArgsConstructor
public class RawPassword extends BaseValueObject {

    /**
     * Minimum password length.
     */
    public static final int MIN_PASSWORD_LENGTH = 8;

    /**
     * Maximum password length.
     */
    public static final int MAX_PASSWORD_LENGTH = 255;

    private final String value;

    @Override
    protected void validate() {
        if (value == null || value.isBlank()) {
            String msg = "Please enter a password with digits and alphas, not empty string";
            throw new EmptyPasswordWasProvidedError(msg);
        }

        if (isOnlyDigits(value)) {
            String msg = "Please enter password with digits and alphas, not only digits";
            throw new WeakPasswordWasProvidedError(msg);
        }

        int length = value.length();
        if (length < MIN_PASSWORD_LENGTH) {
            String msg = "Password too short. Please provide bigger than 8 characters";
            throw new WeakPasswordWasProvidedError(msg);
        }

        if (length > MAX_PASSWORD_LENGTH) {
            String msg = "Password too long. Please provide less than 255 characters";
            throw new WeakPasswordWasProvidedError(msg);
        }
    }

    /**
     * Checks if the string contains only digits.
     *
     * @param str the string to check
     * @return true if the string contains only digits, false otherwise
     */
    private boolean isOnlyDigits(String str) {
        if (str == null || str.isEmpty()) {
            return false;
        }
        for (char c : str.toCharArray()) {
            if (!Character.isDigit(c)) {
                return false;
            }
        }
        return true;
    }

    /**
     * Returns the string representation of the password value.
     *
     * @return the password value as string
     */
    @Override
    public String toString() {
        return value;
    }
}

