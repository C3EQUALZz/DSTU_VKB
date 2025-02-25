package com.example.repairserviceapp;

import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.info.Contact;
import io.swagger.v3.oas.annotations.info.Info;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@OpenAPIDefinition(
        info = @Info(
                title = "Repair Service App",
                description = "API системы компьютерной мастерской",
                version = "1.0.0",
                contact = @Contact(name = "Grishkov Egor")
        )
)
@SpringBootApplication
public class RepairServiceAppApplication {

    public static void main(String[] args) {
        SpringApplication.run(RepairServiceAppApplication.class, args);
    }

}
