package dstu.csae.matocip.sign;

import java.math.BigInteger;

public class SignGhost implements Sign<BigInteger, BigInteger>{
    @Override
    public BigInteger sign(BigInteger input) {
        return null;
    }

    @Override
    public boolean check(BigInteger message, BigInteger sign) {
        return false;
    }
}
