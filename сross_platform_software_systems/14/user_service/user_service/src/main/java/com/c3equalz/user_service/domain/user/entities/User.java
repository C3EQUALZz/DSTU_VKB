package com.c3equalz.user_service.domain.user.entities;

import com.c3equalz.user_service.domain.common.entities.BaseAggregateRoot;
import com.c3equalz.user_service.domain.user.values.*;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class User extends BaseAggregateRoot<UserID> {
    private UserEmail email;
    private Username name;
    private UserPasswordHash hashedPassword;
    private UserRole role;
    private boolean isActive;

    public User(UserID id, UserEmail email, Username name, UserPasswordHash hashedPassword, UserRole role) {
        super(id);
        this.email = email;
        this.name = name;
        this.hashedPassword = hashedPassword;
        this.role = role;
        this.isActive = true;
    }
}
