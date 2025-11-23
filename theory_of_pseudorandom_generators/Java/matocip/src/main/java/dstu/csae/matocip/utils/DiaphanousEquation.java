package dstu.csae.matocip.utils;

import java.math.BigInteger;

public record DiaphanousEquation(BigInteger a, BigInteger b, BigInteger c) {
    public boolean isEquated(BigInteger x, BigInteger y){
        BigInteger u = a.multiply(x);
        BigInteger v = b.multiply(y);
        return u.add(v).equals(c);
    }
}
