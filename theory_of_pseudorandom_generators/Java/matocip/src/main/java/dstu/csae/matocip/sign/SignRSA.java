package dstu.csae.matocip.sign;

import dstu.csae.matocip.cipher.RSA;
import lombok.NonNull;

import java.math.BigInteger;

public class SignRSA implements Sign<BigInteger, BigInteger> {

    private final RSA cipher;

    public SignRSA(@NonNull RSA cipher){
        this.cipher = cipher;
    }

    @Override
    public BigInteger sign(BigInteger input) {
        return cipher.decrypt(input);
    }

    @Override
    public boolean check(BigInteger message, BigInteger sign ) {
        BigInteger primitive = cipher.encrypt(sign);
        return primitive.equals(message);
    }
}
