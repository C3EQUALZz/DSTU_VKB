package com.example.repairserviceapp.handlers;

import lombok.Getter;
import org.springframework.http.HttpStatus;

import java.time.LocalDateTime;
import java.util.Map;

@Getter
public class ValidationErrorResponse extends ErrorResponse {
    private final Map<String, String> descriptionOfErrors;

    public ValidationErrorResponse(
            String message,
            LocalDateTime timestamp,
            Map<String, String> descriptionOfErrors,
            HttpStatus status
    ) {
        super(message, timestamp, status);
        this.descriptionOfErrors = descriptionOfErrors;
    }
}
