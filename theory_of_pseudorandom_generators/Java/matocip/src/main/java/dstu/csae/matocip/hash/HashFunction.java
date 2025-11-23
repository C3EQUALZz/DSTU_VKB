package dstu.csae.matocip.hash;

public interface HashFunction<T, V>{

    V hash(T input);

}
