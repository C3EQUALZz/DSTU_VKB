package dstu.csae.generator;

public interface Generator<T>{

    T next(T last);

}
