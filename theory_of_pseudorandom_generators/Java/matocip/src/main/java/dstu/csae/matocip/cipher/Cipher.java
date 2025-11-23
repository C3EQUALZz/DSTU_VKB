package dstu.csae.matocip.cipher;

import java.math.BigInteger;

public interface Cipher<P, C> {

    C encrypt(P plaintext);

    P decrypt(C ciphertext);

}
