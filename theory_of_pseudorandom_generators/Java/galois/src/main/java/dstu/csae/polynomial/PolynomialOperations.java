package dstu.csae.polynomial;

import dstu.csae.exceptions.ExceptionMessageConstants;
import dstu.csae.galois.Operations;

import java.util.Arrays;
import java.util.Objects;

public class PolynomialOperations extends Operations {

    static Polynomial addition(Polynomial first, Polynomial second){
        if(checkNullable(first, second)){
            return null;
        }
        int[] firstC = Polynomial.removeLastZero(first);
        int[] secondC = Polynomial.removeLastZero(second);

        return new Polynomial(addition(firstC, secondC));
    }

    static Polynomial subtraction(Polynomial reduced, Polynomial subtracted){
        if(checkNullable(reduced, subtracted)){
            return null;
        }
        int[] reducedC = Polynomial.removeLastZero(reduced);
        int[] subtractedC = Polynomial.removeLastZero(subtracted);
        return new Polynomial(subtraction(reducedC, subtractedC));
    }


    static Polynomial multiplication (Polynomial first, Polynomial second){
        if(checkNullable(first, second)){
            return null;
        }
        int[] firstC = first.getCoefficients();
        int[] secondC = second.getCoefficients();
        return new Polynomial(multiplication(firstC, secondC));
    }

    static Polynomial division(Polynomial divisible, Polynomial divisor){
        if(checkNullable(divisible, divisor)){
            return null;
        }
        if(divisor.getDegree() == 0){
            throw new ArithmeticException(String.format(
                    ExceptionMessageConstants.POLYNOMIAL_DIVIDE_BY_ZERO,
                    divisor
            ));
        }
        if ((divisible.getDegree() == 0) || divisible.getDegree() < divisor.getDegree()){
            return Polynomial.ZERO.clone();
        }
        int[] divisibleC = Polynomial.removeLastZero(divisible);
        int[] divisorC = Polynomial.removeLastZero(divisor);
        return new Polynomial(division(divisibleC, divisorC));
    }

    static Polynomial mod(Polynomial divisible, Polynomial divisor){
        if(checkNullable(divisible, divisor)){
            return null;
        }
        if(divisor.getDegree() == 0){
            throw new ArithmeticException(String.format(
                    ExceptionMessageConstants.POLYNOMIAL_DIVIDE_BY_ZERO,
                    divisor
            ));
        }
        if ((divisible.getDegree() == 0)){
            return Polynomial.ZERO.clone();
        }
        if(divisible.getDegree() < divisor.getDegree()){
            return divisible.clone();
        }
        int[] divisibleC = Polynomial.removeLastZero(divisible);
        int[] divisorC = Polynomial.removeLastZero(divisor);
        return new Polynomial(
                subtraction(divisibleC,
                        multiplication(
                                division(divisibleC, divisorC),
                                divisorC
                        )));
    }

    private static boolean checkNullable(Object ... objects){
        return Arrays.stream(objects).anyMatch(Objects::isNull);
    }
}
