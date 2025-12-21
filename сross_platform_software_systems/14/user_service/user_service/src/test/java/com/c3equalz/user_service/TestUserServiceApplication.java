package com.c3equalz.user_service;

import org.springframework.boot.SpringApplication;

public class TestUserServiceApplication {

    public static void main(String[] args) {
        SpringApplication.from(UserServiceApplication::main).with(TestcontainersConfiguration.class).run(args);
    }

}
