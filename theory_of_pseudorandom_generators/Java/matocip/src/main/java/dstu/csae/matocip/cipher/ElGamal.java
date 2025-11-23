package dstu.csae.matocip.cipher;

import dstu.csae.matocip.utils.NumberOperator;
import lombok.Getter;
import lombok.Setter;

import java.math.BigInteger;
import java.util.*;

public class ElGamal implements Cipher<BigInteger, Map.Entry<BigInteger, BigInteger>> {
    private static final String P_IS_NOT_PRIME = "Значение p не является простым числом";
    private static final String Q_IS_OUT_OF_BOUNDS = "Значение q выходит за рамки допустимых значений";
    private static final String X_IS_OUT_OF_BOUNDS = "Значение x выходит за рамки допустимых значений";
    private static final String M_IS_OUT_OF_BOUNDS = "Значение M выходит за рамки допустимых значений";
    private static final String GCD_IS_NOT_ONE = "НОД(p, q) не равен 1";

    @Getter @Setter
    private static int kBitCount = 32;
    @Getter @Setter
    private static int pBitCount = 1024;

    @Getter private final BigInteger p;
    @Getter private final BigInteger g;
    private final BigInteger x;
    @Getter private final BigInteger y;

    public ElGamal(BigInteger p, BigInteger g, BigInteger x)
            throws IllegalArgumentException{
        if(!NumberOperator.isProbablePrime(p)){
            throw new IllegalArgumentException(P_IS_NOT_PRIME);
        }
        if(g.compareTo(BigInteger.ZERO) <= 0 || g.compareTo(p) >= 0){
            throw new IllegalArgumentException(Q_IS_OUT_OF_BOUNDS);
        }
        if(!p.gcd(g).equals(BigInteger.ONE)){
            throw new IllegalArgumentException(GCD_IS_NOT_ONE);
        }
        if(x.compareTo(BigInteger.ONE) <= 0 || x.compareTo(p.subtract(BigInteger.ONE)) >= 0){
            throw new IllegalArgumentException(X_IS_OUT_OF_BOUNDS);
        }
        this.p = p;
        this.g = g;
        this.x = x;
        this.y = g.modPow(x, p);
    }

    @Override
    public Map.Entry<BigInteger, BigInteger> encrypt(BigInteger plaintext) {
        if(plaintext.compareTo(BigInteger.ZERO) < 0 || plaintext.compareTo(p) >= 0){
            throw new IllegalArgumentException(M_IS_OUT_OF_BOUNDS);
        }
        BigInteger k = NumberOperator.nextBigInt(32, BigInteger.TWO, p.subtract(BigInteger.ONE));
        BigInteger a = g.modPow(k, p);
        BigInteger b = y.modPow(k, p)
                .multiply(plaintext).mod(p);
        return new AbstractMap.SimpleEntry<>(a, b);
    }

    @Override
    public BigInteger decrypt(Map.Entry<BigInteger, BigInteger> ciphertext) {
        BigInteger a = ciphertext.getKey();
        BigInteger b = ciphertext.getValue();
        return a.modPow(
                p.subtract(BigInteger.ONE)
                            .subtract(x), p)
                .multiply(b)
                .mod(p);
    }

    @Override
    public boolean equals(Object o) {
        if (o == null || getClass() != o.getClass()) return false;
        ElGamal elGamal = (ElGamal) o;
        return Objects.equals(p, elGamal.p) && Objects.equals(g, elGamal.g) && Objects.equals(y, elGamal.y);
    }

    @Override
    public int hashCode() {
        return Objects.hash(p, g, y);
    }

    @Override
    public String toString() {
        List<String> out = new ArrayList<>();
        out.add("Шифр Эль-Гамаля");
        out.add("p = " + p);
        out.add("g = " + g);
        out.add("y = " + y);
        return String.join("\n", out);
    }
}
