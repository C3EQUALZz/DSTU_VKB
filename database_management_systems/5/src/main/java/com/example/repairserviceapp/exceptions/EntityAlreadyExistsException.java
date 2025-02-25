package com.example.repairserviceapp.exceptions;

import org.springframework.http.HttpStatus;

public class EntityAlreadyExistsException extends ApplicationException {

    public EntityAlreadyExistsException(String message) {
        super(message);
        this.status = HttpStatus.CONFLICT;
    }
}
