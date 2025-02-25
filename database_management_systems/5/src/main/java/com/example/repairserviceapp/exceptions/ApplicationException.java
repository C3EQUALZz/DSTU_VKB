package com.example.repairserviceapp.exceptions;

import lombok.Getter;
import org.springframework.http.HttpStatus;

@Getter
public abstract class ApplicationException extends RuntimeException {
    protected HttpStatus status;

    public ApplicationException(String message) {
        super(message);
    }
}
