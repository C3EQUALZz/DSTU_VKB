package com.example.repairserviceapp;

import io.jsonwebtoken.Jwts;
import jakarta.xml.bind.DatatypeConverter;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class RepairServiceAppApplicationTests {

    @Test
    void contextLoads() {
    }

    @Test
    void generateSecretKey() {
        System.out.println(DatatypeConverter.printHexBinary(Jwts.SIG.HS512.key().build().getEncoded()));
    }

}
