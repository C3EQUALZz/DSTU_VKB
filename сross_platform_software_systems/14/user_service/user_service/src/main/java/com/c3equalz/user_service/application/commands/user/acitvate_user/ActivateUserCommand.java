package com.c3equalz.user_service.application.commands.user.acitvate_user;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

import java.util.UUID;

@RequiredArgsConstructor
@Getter
public class ActivateUserCommand {
    private final UUID userID;
}
