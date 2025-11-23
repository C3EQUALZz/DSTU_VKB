package dstu.csae.exceptions;

public class EmptyCoefficientsException extends RuntimeException{

    public EmptyCoefficientsException() {
    }

    public EmptyCoefficientsException(String message) {
        super(message);
    }
}
