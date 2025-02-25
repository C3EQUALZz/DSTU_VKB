package com.example.repairserviceapp.configs;

import com.example.repairserviceapp.entities.Client;
import com.example.repairserviceapp.enums.Roles;
import com.example.repairserviceapp.services.ClientsService;
import lombok.Setter;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.util.UUID;

@Slf4j
@Component
public class AdminSetupRunner implements CommandLineRunner {

    @Setter(onMethod_ = @Autowired)
    private ClientsService clientsService;

    @Value("${spring.my-admin.name}")
    private String name;

    @Value("${spring.my-admin.surname}")
    private String surname;

    @Value("${spring.my-admin.patronymic}")
    private String patronymic;

    @Value("${spring.my-admin.phone_number}")
    private String phoneNumber;

    @Value("${spring.my-admin.email}")
    private String email;

    @Value("${spring.my-admin.password}")
    private String password;

    @Override
    public void run(String... args) {
        log.info("Admin Setup...");
        if (!clientsService.exists(email)) {
            Client admin = Client.builder()
                    .id(UUID.randomUUID())
                    .name(name)
                    .surname(surname)
                    .patronymic(patronymic)
                    .phoneNumber(phoneNumber)
                    .email(email)
                    .password(password)
                    .role(Roles.ADMIN.getValue())
                    .build();
            clientsService.create(admin, Roles.ADMIN.getValue());
        }

    }
}
