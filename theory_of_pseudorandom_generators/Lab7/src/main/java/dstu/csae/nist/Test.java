package dstu.csae.nist;

public interface Test<T> {

    double test(T sequence);

    boolean isSuccessful(double actual, double required);

}
