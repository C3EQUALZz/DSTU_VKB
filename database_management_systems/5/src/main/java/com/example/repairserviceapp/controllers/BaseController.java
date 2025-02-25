package com.example.repairserviceapp.controllers;

import com.example.repairserviceapp.exceptions.ValidationException;
import org.springframework.validation.BindingResult;

import java.util.HashMap;
import java.util.Map;

public abstract class BaseController {
    protected void validate(BindingResult bindingResult, String message) {
        if (bindingResult.hasErrors()) {
            Map<String, String> errors = new HashMap<>();
            bindingResult.getFieldErrors().forEach(error -> errors.put(error.getField(), error.getDefaultMessage()));
            throw new ValidationException(String.format("Validation Error: %s", message), errors);
        }
    }
}
