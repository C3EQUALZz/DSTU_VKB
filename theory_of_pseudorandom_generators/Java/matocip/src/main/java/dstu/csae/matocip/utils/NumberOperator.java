package dstu.csae.matocip.utils;

import java.math.BigInteger;
import java.util.Random;

public class NumberOperator {

    private static final int TEST_COUNT = 100;

    public static BigInteger nextBigInt(int bitCount, BigInteger origin, BigInteger bound){
        BigInteger next;
        do{
            next = nextBigInt(bitCount);
        }while (next.compareTo(origin) < 0 || next.compareTo(bound) >= 0);
        return next;
    }


    public static BigInteger nextBigInt(int bigCount){
        return new BigInteger(bigCount, new Random());
    }

    public static BigInteger nextPrimeBigInt(int bitCount, BigInteger origin, BigInteger bound) {
        BigInteger next;
        do {
            next = nextPrimeBigInt(bitCount);
        }while (isOutOfBounds(next, origin, bound));
        return next;
    }

    public static BigInteger nextPrimeBigInt(int bitCount){
        Random random = new Random();
        BigInteger next;
        do {
            next = BigInteger.probablePrime(bitCount, random);
        } while (!isProbablePrime(next));
        return next;
    }

    public static boolean isProbablePrime(BigInteger number){
        for(int i = 0; i < TEST_COUNT; i ++){
            if(!number.isProbablePrime(i)){
                return false;
            }
        }
        return true;
    }


    private static boolean isOutOfBounds(BigInteger number, BigInteger origin, BigInteger bound){
        return number.compareTo(origin) < 0 || number.compareTo(bound) >= 0;
    }
}
