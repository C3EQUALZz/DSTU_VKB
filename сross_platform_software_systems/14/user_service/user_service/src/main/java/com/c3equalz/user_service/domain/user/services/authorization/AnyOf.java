package com.c3equalz.user_service.domain.user.services.authorization;

import java.util.Arrays;
import java.util.List;

/**
 * Permission that is satisfied if any of the provided permissions are satisfied.
 *
 * @param <PC> the type of permission context
 */
public class AnyOf<PC extends PermissionContext> implements Permission<PC> {

    private final List<Permission<PC>> permissions;

    /**
     * Creates a new AnyOf permission.
     *
     * @param permissions the permissions to check
     */
    @SafeVarargs
    public AnyOf(Permission<PC>... permissions) {
        this.permissions = Arrays.asList(permissions);
    }

    @Override
    public boolean isSatisfiedBy(PC context) {
        return permissions.stream()
                .anyMatch(permission -> permission.isSatisfiedBy(context));
    }
}

