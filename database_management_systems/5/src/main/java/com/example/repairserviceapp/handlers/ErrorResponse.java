package com.example.repairserviceapp.handlers;


import lombok.Getter;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;

import java.time.LocalDateTime;

@RequiredArgsConstructor()
@Getter
public class ErrorResponse {
    private final String message;
    private final LocalDateTime timestamp;
    private final HttpStatus status;
}
