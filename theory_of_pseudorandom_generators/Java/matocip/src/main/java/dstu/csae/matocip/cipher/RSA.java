package dstu.csae.matocip.cipher;

import dstu.csae.matocip.utils.EuclidAlgorithms;
import dstu.csae.matocip.utils.NumberOperator;
import lombok.Getter;
import lombok.NonNull;
import lombok.Setter;

import java.math.BigInteger;
import java.util.*;

@Getter
public class RSA implements Cipher<BigInteger, BigInteger> {
    private static final String NUMBERS_ARE_NOT_PRIME = "Числа p и q не являются простыми";
    private static final String ILLEGAL_BIT_COUNT = "Количество бит открытого ключа не соответствует заданной конфигурации";
    private static final String NOT_MUTUALLY_SIMPLE = "Параметр e не взаимно простой со значением m = %s";
    private static final String E_OUT_OF_BOUNDS = "Параметр находится за пределами допустимых значений";


   @Setter
   private static int minKeyBitCount = 512;

    private final BigInteger p;
    private final BigInteger q;
    private final BigInteger n;
    private final BigInteger m;
    private final BigInteger e;
    private final BigInteger d;

    public RSA(@NonNull BigInteger p,
               @NonNull BigInteger q,
               @NonNull BigInteger e)
            throws IllegalArgumentException{
        if(!(NumberOperator.isProbablePrime(p) &&
                NumberOperator.isProbablePrime(q))){
            throw new IllegalArgumentException(NUMBERS_ARE_NOT_PRIME);
        }
        BigInteger n =  p.multiply(q);
        if(Integer.sum(n.bitCount(), e.bitCount()) < minKeyBitCount){
            throw new IllegalArgumentException(ILLEGAL_BIT_COUNT);
        }

        this.p = p;
        this.q = q;
        this.n = n;
        m = setM();
        if(e.compareTo(BigInteger.ONE) <= 0 || e.compareTo(m) >= 0){
            throw new IllegalArgumentException(E_OUT_OF_BOUNDS);
        }
        if(!m.gcd(e).equals(BigInteger.ONE)){
            throw new IllegalArgumentException(NOT_MUTUALLY_SIMPLE);
        }
        this.e = e;
        this.d = setD(e, m);
    }


    private BigInteger setM(){
        BigInteger first = p.subtract(BigInteger.ONE);
        BigInteger second = q.subtract(BigInteger.ONE);
        return first.multiply(second);
    }

    private BigInteger setD(BigInteger e, BigInteger m){
        return EuclidAlgorithms.gcdEx(e, m).a().mod(m);
    }

    public Map.Entry<BigInteger, BigInteger> getPublicKey(){
        return new AbstractMap.SimpleEntry<>(e, n);
    }

    @Override
    public BigInteger encrypt(BigInteger plaintext)
            throws IndexOutOfBoundsException{
        if(plaintext.signum() < 0 || plaintext.compareTo(n) >= 0){
            throw new IndexOutOfBoundsException();
        }
        return plaintext.modPow(e, n);
    }

    @Override
    public BigInteger decrypt(BigInteger ciphertext) {
        return ciphertext.modPow(d, n);
    }

    @Override
    public boolean equals(Object o) {
        if (o == null || getClass() != o.getClass()) return false;
        RSA rsa = (RSA) o;
        return Objects.equals(p, rsa.p) && Objects.equals(q, rsa.q);
    }

    @Override
    public int hashCode() {
        return Objects.hash(p, q);
    }

    @Override
    public String toString() {
        List<String> out = new ArrayList<>();
        out.add("Объект криптосистемы RSA");
        out.add("n = " + getN());
        out.add(String.format("public key: (%s , %s)", e, n));
        return String.join("\n", out);
    }
}
