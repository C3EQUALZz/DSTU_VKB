package com.c3equalz.user_service.domain.user.services;

import com.c3equalz.user_service.domain.common.services.BaseDomainService;
import com.c3equalz.user_service.domain.user.entities.User;
import com.c3equalz.user_service.domain.user.errors.ActivationChangeNotPermittedError;
import com.c3equalz.user_service.domain.user.errors.AuthorizationError;
import com.c3equalz.user_service.domain.user.errors.RoleChangeNotPermittedError;
import com.c3equalz.user_service.domain.user.events.UserChangedRoleEvent;
import com.c3equalz.user_service.domain.user.events.UserToggleActivationEvent;
import com.c3equalz.user_service.domain.user.services.authorization.Permission;
import com.c3equalz.user_service.domain.user.services.authorization.PermissionContext;
import com.c3equalz.user_service.domain.user.values.UserRole;

/**
 * Service for managing user access, roles, and authorization.
 */
public class AccessService extends BaseDomainService {

    /**
     * Toggles the admin role of a user.
     *
     * @param user the user to modify
     * @param isAdmin true to assign ADMIN role, false to assign USER role
     * @throws RoleChangeNotPermittedError if the user's role cannot be changed
     */
    public void toggleUserAdminRole(User user, boolean isAdmin) {
        if (!user.getRole().isChangeable()) {
            String msg = String.format(
                    "Changing role of user '%s' (%s) is not permitted.",
                    user.getName().getValue(),
                    user.getRole()
            );
            throw new RoleChangeNotPermittedError(msg);
        }

        UserRole oldRole = user.getRole();
        user.setRole(isAdmin ? UserRole.ADMIN : UserRole.USER);

        UserChangedRoleEvent newEvent = new UserChangedRoleEvent(
                user.getId(),
                oldRole,
                user.getRole()
        );

        recordEvent(newEvent);
    }

    /**
     * Toggles the activation status of a user.
     *
     * @param user the user to modify
     * @param isActive true to activate, false to deactivate
     * @throws ActivationChangeNotPermittedError if the user's activation cannot be changed
     */
    public void toggleUserActivation(User user, boolean isActive) {
        if (!user.getRole().isChangeable()) {
            String msg = String.format(
                    "Changing activation of user '%s' (%s) is not permitted.",
                    user.getName().getValue(),
                    user.getRole()
            );
            throw new ActivationChangeNotPermittedError(msg);
        }

        user.setActive(isActive);

        UserToggleActivationEvent newEvent = new UserToggleActivationEvent(
                user.getId(),
                isActive
        );

        recordEvent(newEvent);
    }

    /**
     * Authorizes a permission against a context.
     *
     * @param permission the permission to check
     * @param context the permission context
     * @param <PC> the type of permission context
     * @throws AuthorizationError if the permission is not satisfied
     */
    public <PC extends PermissionContext> void authorize(Permission<PC> permission, PC context) {
        if (!permission.isSatisfiedBy(context)) {
            throw new AuthorizationError("Not authorized.");
        }
    }
}

