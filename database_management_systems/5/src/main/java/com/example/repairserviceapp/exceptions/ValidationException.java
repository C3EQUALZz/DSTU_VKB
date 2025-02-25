package com.example.repairserviceapp.exceptions;

import lombok.Getter;
import org.springframework.http.HttpStatus;

import java.util.Map;

@Getter
public class ValidationException extends ApplicationException {
    protected Map<String, String> descriptionOfErrors;

    public ValidationException(String message, Map<String, String> descriptionOfErrors) {
        super(message);
        this.descriptionOfErrors = descriptionOfErrors;
        this.status = HttpStatus.UNPROCESSABLE_ENTITY;
    }
}
