package com.c3equalz.user_service.domain.user.services;

import com.c3equalz.user_service.domain.common.services.BaseDomainService;
import com.c3equalz.user_service.domain.user.entities.User;
import com.c3equalz.user_service.domain.user.errors.RoleAssignmentNotPermittedError;
import com.c3equalz.user_service.domain.user.events.UserChangedEmailEvent;
import com.c3equalz.user_service.domain.user.events.UserChangedNameEvent;
import com.c3equalz.user_service.domain.user.events.UserChangedPasswordEvent;
import com.c3equalz.user_service.domain.user.events.UserCreatedEvent;
import com.c3equalz.user_service.domain.user.ports.PasswordHasher;
import com.c3equalz.user_service.domain.user.ports.UserIdGenerator;
import com.c3equalz.user_service.domain.user.values.*;

import java.time.Instant;

/**
 * Domain service for users.
 * Provides methods for user management operations such as creation, password changes, etc.
 */
public class UserService extends BaseDomainService {

    private final PasswordHasher passwordHasher;
    private final UserIdGenerator userIdGenerator;

    /**
     * Creates a new UserService.
     *
     * @param passwordHasher the password hasher service
     * @param userIdGenerator the user ID generator
     */
    public UserService(PasswordHasher passwordHasher, UserIdGenerator userIdGenerator) {
        this.passwordHasher = passwordHasher;
        this.userIdGenerator = userIdGenerator;
    }

    /**
     * Fabric method that creates a new user. Produces event that user was created
     *
     * @param email email of the user
     * @param name username of the user
     * @param rawPassword raw password of the user
     * @param role role of the user (defaults to USER if not specified)
     * @return User entity if all checks passed
     * @throws RoleAssignmentNotPermittedError if role assignment is not permitted
     */
    public User create(
            UserEmail email,
            Username name,
            RawPassword rawPassword,
            UserRole role
    ) {
        if (role == null) {
            role = UserRole.USER;
        }

        if (!role.isAssignable()) {
            String msg = String.format("Assignment of role: %s not permitted.", role);
            throw new RoleAssignmentNotPermittedError(msg);
        }

        UserPasswordHash hashedPassword = passwordHasher.hash(rawPassword);
        UserID newUserId = userIdGenerator.generate();

        User newUser = new User(
                newUserId,
                email,
                name,
                hashedPassword,
                role
        );

        UserCreatedEvent newEvent = new UserCreatedEvent(
                newUserId,
                email.getValue(),
                name.getValue(),
                role
        );

        recordEvent(newEvent);

        return newUser;
    }

    /**
     * Method that checks if the given password is valid for the given user.
     *
     * @param user user entity which contains password
     * @param rawPassword password to check
     * @return true if the password is valid, false otherwise
     */
    public boolean isPasswordValid(User user, RawPassword rawPassword) {
        return passwordHasher.verify(rawPassword, user.getHashedPassword());
    }

    /**
     * Method that changes the password of the given user. Produces event that user changed the password
     *
     * @param user user entity which contains password
     * @param rawPassword new password to change
     */
    public void changePassword(User user, RawPassword rawPassword) {
        UserPasswordHash hashedPassword = passwordHasher.hash(rawPassword);
        user.setHashedPassword(hashedPassword);
        user.setUpdatedAt(Instant.now());

        UserChangedPasswordEvent newEvent = new UserChangedPasswordEvent(
                user.getId(),
                user.getName().getValue(),
                user.getEmail().getValue(),
                user.getRole().toString()
        );

        recordEvent(newEvent);
    }

    /**
     * Method that changes the name of the given user. Produces event that user changed the name
     *
     * @param user existing user entity in a database
     * @param newUserName new username for entity
     */
    public void changeName(User user, Username newUserName) {
        Username oldUserName = user.getName();
        user.setName(newUserName);
        user.setUpdatedAt(Instant.now());

        UserChangedNameEvent newEvent = new UserChangedNameEvent(
                user.getId(),
                oldUserName.getValue(),
                newUserName.getValue(),
                user.getRole().toString(),
                user.getEmail().getValue()
        );

        recordEvent(newEvent);
    }

    /**
     * Method that changes the email of the given user. Produces event that user changed the email
     *
     * @param user existing user entity in a database
     * @param newEmail new email for entity
     */
    public void changeEmail(User user, UserEmail newEmail) {
        UserEmail oldEmail = user.getEmail();
        user.setEmail(newEmail);
        user.setUpdatedAt(Instant.now());

        UserChangedEmailEvent newEvent = new UserChangedEmailEvent(
                user.getId(),
                oldEmail.getValue(),
                newEmail.getValue(),
                user.getRole().toString(),
                user.getName().getValue()
        );

        recordEvent(newEvent);
    }
}
