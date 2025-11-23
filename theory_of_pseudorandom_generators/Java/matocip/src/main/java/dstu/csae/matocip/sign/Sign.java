package dstu.csae.matocip.sign;

public interface Sign<T, V>{

    V sign(T input);

    boolean check(T message, V sign);
}
