package dstu.csae.galois;

import dstu.csae.exceptions.ExceptionMessageConstants;
import dstu.csae.exceptions.ReverseElementEvaluationException;
import dstu.csae.math.ArithmeticFunctions;
import dstu.csae.polynomial.Polynomial;

import java.math.BigInteger;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Objects;

class FieldOperations extends Operations {

    static int addition(GaloisField galoisField, int first, int second){
        if(first == 0 && second == 0){
            return 0;
        }
        first = bringToField(galoisField, first);
        second = bringToField(galoisField, second);
        if(first == 0 || second == 0){
            return Math.max(first, second);
        }
        return  bringToField(galoisField, first + second);
    }

    static Polynomial addition(GaloisField galoisField, Polynomial first, Polynomial second){
        if(checkNullable(first, second)){
            return null;
        }
        int[] firstC = first.getCoefficients();
        int[] secondC = second.getCoefficients();
        return new Polynomial(addition(galoisField, firstC, secondC));
    }

    static int subtraction(GaloisField galoisField, int reduced, int subtracted){
        return addition(galoisField, reduced, inverseOfAddition(galoisField, subtracted));
    }

    static Polynomial subtraction(GaloisField galoisField, Polynomial reduced, Polynomial subtracted){
        if(checkNullable(galoisField, reduced, subtracted)){
            return null;
        }

        int[] reducedC = reduced.getCoefficients();
        int[] subtractedC = subtracted.getCoefficients();
        return new Polynomial(subtraction(galoisField, reducedC, subtractedC));
    }

    static int multiplication(GaloisField galoisField, int first, int second){
        if(first == 0 || second == 0){
            return 0;
        }
        first = bringToField(galoisField, first);
        second = bringToField(galoisField, second);
        return bringToField(galoisField, first * second);
    }

    static Polynomial multiplication(GaloisField galoisField, Polynomial first, Polynomial second){
        if(checkNullable(galoisField, first, second)){
            return null;
        }
        if(first.equals(Polynomial.ZERO) || second.equals(Polynomial.ZERO)){
            return Polynomial.ZERO.clone();
        }
        int[] firstC = first.getCoefficients();
        int[] secondC = second.getCoefficients();
        return new Polynomial(multiplication(galoisField, firstC, secondC));
    }

    static int division(GaloisField galoisField, int divisible, int divisor)
            throws ArithmeticException{
        if(divisible == 0){
            return 0;
        }
        if(divisor == 0){
            throw new ArithmeticException(
                    String.format(ExceptionMessageConstants.NUMBER_DIVIDE_BY_ZERO, divisible));
        }
        divisor = inverseOfMultiplication(galoisField, divisor);
        return multiplication(galoisField, divisible, divisor);
    }

    static Polynomial division(GaloisField galoisField, Polynomial divisible, Polynomial divisor)
            throws IllegalArgumentException{
        if(checkNullable(galoisField, divisible, divisor)){
            return null;
        }
        if(divisor.equals(Polynomial.ZERO)) {
            throw new IllegalArgumentException(ExceptionMessageConstants.DIVIDE_BY_ZERO);
        }
        if(divisible.equals(Polynomial.ZERO)){
            return Polynomial.ZERO.clone();
        }
        int[] divisibleC = divisible.getCoefficients();
        int[] divisorC = divisor.getCoefficients();
        return new Polynomial(division(galoisField, divisibleC, divisorC));
    }

    static int mod(GaloisField galoisField, int divisible, int divisor)
            throws ArithmeticException{
        if(divisible == 0){
            return 0;
        }
        if(divisor == 0){
            throw new ArithmeticException(
                    String.format(ExceptionMessageConstants.NUMBER_DIVIDE_BY_ZERO, divisible));
        }
        int division = division(galoisField, divisible, divisor);
        return subtraction(galoisField, divisible, multiplication(galoisField, divisor, division));
    }

    static Polynomial mod(GaloisField galoisField, Polynomial divisible, Polynomial divisor)
            throws IllegalArgumentException{
        if(checkNullable(galoisField, divisible, divisor)){
            return null;
        }
        int[] divisibleC = divisible.getCoefficients();
        int[] divisorC = divisor.getCoefficients();
        int[] rem = division(galoisField, divisibleC, divisorC);
        rem = multiplication(galoisField, divisorC, rem);
        rem = subtraction(galoisField, divisibleC, rem);
        return new Polynomial(rem);
    }

    static int inverseOfAddition(GaloisField galoisField, int number){
        if(number == 0){
            return 0;
        }
        number = bringToField(galoisField, number);
        return galoisField.getCharacteristic() - number;
    }

    static int inverseOfMultiplication(GaloisField galoisField, int number)
            throws ReverseElementEvaluationException{
        if (number == 0){
            throw new ReverseElementEvaluationException(
                    String.format(ExceptionMessageConstants.REVERSE_ELEMENT_DOES_NOT_EXIST, number)
            );
        }
        if(!isInField(galoisField, number)) {
            number = bringToField(galoisField, number);
        }
        int mod = galoisField.getCharacteristic();
        int phi = ArithmeticFunctions.getEulerFunction(mod);
        number = powMod(galoisField, number, phi - 1);
        return bringToField(galoisField, number);
    }

    static int powMod(GaloisField galoisField, int number, int degree){
        if(!isInField(galoisField, number)){
            number = bringToField(galoisField, number);
        }
        if(number == 0 || number == 1){
            return number;
        }
        if(degree == 0){
            return 1;
        }
        if(degree < 0){
            number = inverseOfMultiplication(galoisField, number);
            return powMod(galoisField, number, -degree);
        }
        int multiplier = 1;
        while(degree != 1){
            if(degree % 2 != 0){
                multiplier = bringToField(galoisField, multiplier * number);
                degree --;
            }
            number = bringToField(galoisField, (int)Math.pow(number, 2));
            degree /= 2;
        }
        number = bringToField(galoisField, multiplier * number);
        return number;
    }

    static boolean isNormalized(GaloisField galoisField, Polynomial polynomial){
        return !checkNullable(galoisField, polynomial) &&
                Arrays.stream(polynomial.getCoefficients()).allMatch(galoisField::isInField);
    }

    static boolean isIrreducible(GaloisField galoisField, Polynomial polynomial){
        return !checkNullable(galoisField, polynomial);
    }

    static boolean isPrimitive(GaloisField field, int element){
        if(Objects.isNull(field)){
            return false;
        }
        HashSet<Integer> generated = new HashSet<>(){{add(0);}};
        for(int i = 1; i <= field.getCharacteristic(); i ++){
            generated.add(powMod(field, element, i));
        }
        return generated.size() == field.getCharacteristic();
    }

    static int bringToField(GaloisField galoisField, int number){
        if(number == 0){
            return 0;
        }
        int modulo = galoisField.getCharacteristic();
        int multiplication = number % modulo;
        multiplication = multiplication >= 0 ? multiplication : multiplication + modulo;
        return multiplication;
    }

    static int bringToField(GaloisField galoisField, BigInteger number){
        if(checkNullable(galoisField, number)){
            return 0;
        }
        int modulo = galoisField.getCharacteristic();
        int multiplication = number.mod(BigInteger.valueOf(modulo)).intValue();
        multiplication = multiplication >= 0 ? multiplication : multiplication + modulo;
        return multiplication;
    }

    public static Polynomial bringToField(GaloisField galoisField, Polynomial polynomial){
        if(polynomial == null){
            return null;
        }
        int[] coefficients = bringToField(galoisField, polynomial.getCoefficients());
        return new Polynomial(coefficients);
    }

    static boolean isInField(GaloisField galoisField, int number){
        return number >= 0 && number < galoisField.getCharacteristic();
    }

    static boolean isInField(GaloisField galoisField, Polynomial polynomial){
        if(polynomial == null){
            return false;
        }
        return Arrays.stream(polynomial.getCoefficients())
                .allMatch(x -> isInField(galoisField, x));
    }

    private static int[] addition(GaloisField galoisField, int[] firstC, int[] secondC){
        firstC = bringToField(galoisField, firstC);
        secondC = bringToField(galoisField, secondC);
        return bringToField(galoisField, addition(firstC, secondC));
    }

    private static int[] subtraction(GaloisField galoisField, int[] reducedC, int[] subtractedC){
        reducedC = bringToField(galoisField, reducedC);
        subtractedC = bringToField(galoisField, subtractedC);
        return bringToField(galoisField, subtraction(reducedC, subtractedC));
    }

    private static int[] multiplication(GaloisField galoisField, int[] firstC, int[] secondC){
        firstC = bringToField(galoisField, firstC);
        secondC = bringToField(galoisField, secondC);
        return bringToField(galoisField, multiplication(firstC, secondC));
    }

    private static int[] division(GaloisField galoisField, int[] divisible, int[] divisor){
        divisible = bringToField(galoisField,divisible);
        divisor = bringToField(galoisField, divisor);
        if(divisible.length < divisor.length){
            return new int[]{0};
        }
        int[] division = new int[divisible.length - divisor.length + 1];
        int[] current;
        int divisibleDegree = divisible.length - 1;
        int divisorDegree = divisor.length - 1;
        while(divisibleDegree >= divisorDegree){
            current = new int[divisibleDegree];
            division[divisibleDegree - divisorDegree] = divisible[divisibleDegree] / divisor[divisorDegree];
            current[divisibleDegree - divisorDegree] = division[divisibleDegree - divisorDegree];
            divisible = subtraction(galoisField, divisible, multiplication(galoisField, current, divisor));
            divisibleDegree--;
        }
        return division;
    }

    private static int[] bringToField(GaloisField galoisField, int[] coefficients){
        return Arrays.stream(coefficients)
                .map(x -> bringToField(galoisField, x))
                .toArray();
    }

    private static boolean checkNullable(Object ... objects){
        return Arrays.stream(objects).anyMatch(Objects::isNull);
    }
}
