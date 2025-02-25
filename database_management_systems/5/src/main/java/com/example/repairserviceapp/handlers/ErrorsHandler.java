package com.example.repairserviceapp.handlers;

import com.example.repairserviceapp.exceptions.ApplicationException;
import com.example.repairserviceapp.exceptions.ValidationException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

import java.time.LocalDateTime;

@ControllerAdvice
@Slf4j
public class ErrorsHandler {

    @ExceptionHandler(ApplicationException.class)
    public ResponseEntity<ErrorResponse> exceptionHandler(ApplicationException ex) {
        log.warn("{} {}", ex.getClass().getSimpleName(), ex.getMessage());
        return ResponseEntity.status(ex.getStatus()).body(new ErrorResponse(ex.getMessage(), LocalDateTime.now(), ex.getStatus()));
    }

    @ExceptionHandler(ValidationException.class)
    public ResponseEntity<ValidationErrorResponse> validationExceptionHandler(ValidationException ex) {
        log.warn("{} {} {}", ex.getClass().getSimpleName(), ex.getMessage(), ex.getDescriptionOfErrors());
        return ResponseEntity.status(ex.getStatus())
                .body(
                        new ValidationErrorResponse(ex.getMessage(),
                                LocalDateTime.now(),
                                ex.getDescriptionOfErrors(),
                                ex.getStatus())
                );
    }
}
