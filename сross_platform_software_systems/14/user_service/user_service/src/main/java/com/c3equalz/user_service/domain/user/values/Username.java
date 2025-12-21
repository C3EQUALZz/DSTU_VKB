package com.c3equalz.user_service.domain.user.values;

import com.c3equalz.user_service.domain.user.errors.BadUsernameError;
import com.c3equalz.user_service.domain.common.values.BaseValueObject;
import lombok.Getter;

import java.util.regex.Pattern;

/**
 * Username value object with validation.
 * <p>
 * Validation rules:
 * <ul>
 *     <li>Must be between {@value MIN_LEN} and {@value MAX_LEN} characters</li>
 *     <li>Must start with a letter (A-Z, a-z) or a digit (0-9)</li>
 *     <li>Can contain letters, digits, dots (.), hyphens (-), and underscores (_)</li>
 *     <li>Cannot contain consecutive special characters (.., --, __)</li>
 *     <li>Must end with a letter (A-Z, a-z) or a digit (0-9)</li>
 * </ul>
 *
 */
@Getter
public class Username extends BaseValueObject {

    /**
     * Minimum length of a username.
     */
    public static final int MIN_LEN = 5;

    /**
     * Maximum length of a username.
     */
    public static final int MAX_LEN = 20;

    /**
     * Pattern for validating that username starts with a letter or digit.
     */
    private static final Pattern PATTERN_START = Pattern.compile("^[a-zA-Z0-9]");

    /**
     * Pattern for validating allowed characters (letters, digits, dots, hyphens, underscores).
     */
    private static final Pattern PATTERN_ALLOWED_CHARS = Pattern.compile("[a-zA-Z0-9._-]*");

    /**
     * Pattern for validating no consecutive special characters.
     */
    private static final Pattern PATTERN_NO_CONSECUTIVE_SPECIALS = Pattern.compile(
            "^[a-zA-Z0-9]+([._-]?[a-zA-Z0-9]+)*[._-]?$"
    );

    /**
     * Pattern for validating that username ends with a letter or digit.
     */
    private static final Pattern PATTERN_END = Pattern.compile(".*[a-zA-Z0-9]$");

    private final String value;

    /**
     * Creates a new Username value object.
     *
     * @param value the username string value
     * @throws BadUsernameError if validation fails
     */
    public Username(String value) {
        this.value = value;
        super();
    }

    @Override
    protected void validate() {

        if (value == null) {
            throw new BadUsernameError("Username cannot be null");
        }
        validateUsernameLength(value);
        validateUsernamePattern(value);
    }

    /**
     * Validates the length of the username.
     *
     * @param usernameValue the username value to validate
     * @throws BadUsernameError if length is invalid
     */
    private void validateUsernameLength(String usernameValue) {
        int length = usernameValue.length();
        if (length < MIN_LEN || length > MAX_LEN) {
            throw new BadUsernameError(
                    String.format(
                            "Username must be between %d and %d characters.",
                            MIN_LEN,
                            MAX_LEN
                    )
            );
        }
    }

    /**
     * Validates the pattern of the username.
     *
     * @param usernameValue the username value to validate
     * @throws BadUsernameError if pattern validation fails
     */
    private void validateUsernamePattern(String usernameValue) {
        if (!PATTERN_START.matcher(usernameValue).find()) {
            throw new BadUsernameError(
                    "Username must start with a letter (A-Z, a-z) or a digit (0-9)."
            );
        }

        if (!PATTERN_ALLOWED_CHARS.matcher(usernameValue).matches()) {
            throw new BadUsernameError(
                    "Username can only contain letters (A-Z, a-z), digits (0-9), dots (.), hyphens (-), and underscores (_)."
            );
        }

        if (!PATTERN_NO_CONSECUTIVE_SPECIALS.matcher(usernameValue).matches()) {
            throw new BadUsernameError(
                    "Username cannot contain consecutive special characters "
                            + "like .., --, or __."
            );
        }

        if (!PATTERN_END.matcher(usernameValue).matches()) {
            throw new BadUsernameError(
                    "Username must end with a letter (A-Z, a-z) or a digit (0-9)."
            );
        }
    }
}

