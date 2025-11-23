package dstu.csae.galois.extended;

import dstu.csae.exceptions.ExceptionMessageConstants;
import dstu.csae.galois.GaloisField;
import dstu.csae.polynomial.Polynomial;

import java.util.*;
import java.util.stream.IntStream;

public class ExtendedFieldOperations {

    static int addition(GaloisFieldExtension galoisFieldExtension, int first, int second){
        if(Objects.isNull(galoisFieldExtension)){
            return -1;
        }
        first = bringToField(galoisFieldExtension, first);
        second = bringToField(galoisFieldExtension, second);
        return galoisFieldExtension.additionMatrix[first][second];
    }

    static Polynomial addition(GaloisFieldExtension galoisFieldExtension, Polynomial first, Polynomial second){
        if(checkNullable(galoisFieldExtension, first, second)){
            return null;
        }
        int firstI = galoisFieldExtension.indexOf(bringToField(galoisFieldExtension, first));
        int secondI = galoisFieldExtension.indexOf(bringToField(galoisFieldExtension, second));
        int additionI = galoisFieldExtension.additionMatrix[firstI][secondI];
        return galoisFieldExtension.get(additionI);
    }

    static int subtraction(GaloisFieldExtension galoisFieldExtension, int reduced, int subtracted){
        if(Objects.isNull(galoisFieldExtension)){
            return -1;
        }
        reduced = bringToField(galoisFieldExtension, reduced);
        subtracted = bringToField(galoisFieldExtension, subtracted);
        subtracted = inverseOfAddition(galoisFieldExtension, subtracted);
        return galoisFieldExtension.additionMatrix[reduced][subtracted];
    }

    static Polynomial subtraction(GaloisFieldExtension galoisFieldExtension, Polynomial reduced, Polynomial subtracted){
        if(checkNullable(galoisFieldExtension, reduced, subtracted)){
            return null;
        }
        int reducedI = galoisFieldExtension.indexOf(bringToField(galoisFieldExtension, reduced));
        int subtractedI = galoisFieldExtension.indexOf(
                inverseOfAddition(galoisFieldExtension, bringToField(galoisFieldExtension, subtracted)));
        int subtractionI = galoisFieldExtension.additionMatrix[reducedI][subtractedI];
        return galoisFieldExtension.get(subtractionI);
    }

    static int multiplication(GaloisFieldExtension galoisFieldExtension, int first, int second){
        if(Objects.isNull(galoisFieldExtension)){
            return -1;
        }
        first = bringToField(galoisFieldExtension, first);
        second = bringToField(galoisFieldExtension, second);
        return galoisFieldExtension.multiplicationMatrix[first][second];
    }

    static Polynomial multiplication(GaloisFieldExtension galoisFieldExtension, Polynomial first, Polynomial second){
        if(checkNullable(galoisFieldExtension, first, second)){
            return null;
        }
        int firstI = galoisFieldExtension.indexOf(bringToField(galoisFieldExtension, first));
        int secondI = galoisFieldExtension.indexOf(bringToField(galoisFieldExtension, second));
        int multiplicationI = galoisFieldExtension.multiplicationMatrix[firstI][secondI];
        return galoisFieldExtension.get(multiplicationI);
    }

    static Polynomial division(GaloisFieldExtension galoisFieldExtension, Polynomial divisible, Polynomial divisor)
            throws IllegalArgumentException{
        if(checkNullable(galoisFieldExtension, divisible, divisor)){
            return null;
        }
        if(divisor.equals(Polynomial.ZERO)){
            throw new IllegalArgumentException(ExceptionMessageConstants.DIVIDE_BY_ZERO);
        }
        int divisibleI = galoisFieldExtension.indexOf(bringToField(galoisFieldExtension, divisible));
        int divisorI = galoisFieldExtension.indexOf(
                inverseOfMultiplication(galoisFieldExtension, bringToField(galoisFieldExtension, divisor)));
        int divisionI = galoisFieldExtension.multiplicationMatrix[divisibleI][divisorI];
        return galoisFieldExtension.get(divisionI);
    }

    static int division(GaloisFieldExtension galoisFieldExtension, int divisible, int divisor)
            throws IllegalArgumentException{
        if(Objects.isNull(galoisFieldExtension)){
            return -1;
        }
        if(divisor == 0){
            throw new IllegalArgumentException(ExceptionMessageConstants.DIVIDE_BY_ZERO);
        }
        divisible = bringToField(galoisFieldExtension, divisible);
        divisor = bringToField(galoisFieldExtension, divisor);
        divisor = inverseOfMultiplication(galoisFieldExtension, divisor);
        return galoisFieldExtension.multiplicationMatrix[divisible][divisor];
    }

    static int mod(GaloisFieldExtension galoisFieldExtension, int divisible, int divisor){
        if(Objects.isNull(galoisFieldExtension)){
            return -1;
        }
        int division = division(galoisFieldExtension, divisible, divisor);
        int multiplication = multiplication(galoisFieldExtension, division, divisor);
        return subtraction(galoisFieldExtension, divisible, multiplication);
    }

    static int powMod(GaloisFieldExtension galoisFieldExtension, int number, int degree){
        if(Objects.isNull(galoisFieldExtension)){
            return -1;
        }
        if(!isInBounds(galoisFieldExtension, number)){
            number = bringToField(galoisFieldExtension, number);
        }
        if(degree < 0){
            number = inverseOfMultiplication(galoisFieldExtension, number);
            degree = -degree;
        }
        if(degree == 0){
            return 1;
        }
        if(degree == 1){
            return number;
        }
        int multiplier = 1;
        while (degree != 1){
            if(degree % 2 != 0){
                multiplier = multiplication(galoisFieldExtension, multiplier, number);
                degree --;
            }
            number = multiplication(galoisFieldExtension, number, number);
            degree /= 2;
        }
        return multiplication(galoisFieldExtension, multiplier, number);
    }

    static Polynomial powMod(GaloisFieldExtension galoisFieldExtension, Polynomial polynomial, int degree){
        if(checkNullable(galoisFieldExtension, polynomial)){
            return null;
        }
        int polynomialI = galoisFieldExtension.indexOf(bringToField(galoisFieldExtension, polynomial));
        return galoisFieldExtension.get(powMod(galoisFieldExtension, polynomialI, degree));
    }

    static Polynomial inverseOfAddition(GaloisFieldExtension galoisFieldExtension, Polynomial polynomial){
        if(checkNullable(galoisFieldExtension, polynomial)){
            return null;
        }
        Polynomial bring = Optional.ofNullable(bringToField(galoisFieldExtension, polynomial))
                .orElse(galoisFieldExtension.ZERO);
        int indexOfBring = galoisFieldExtension.indexOf(bring);
        return galoisFieldExtension.get(inverseOfAddition(galoisFieldExtension, indexOfBring));
    }

    static Polynomial inverseOfMultiplication(GaloisFieldExtension galoisFieldExtension, Polynomial polynomial) {
        if (checkNullable(galoisFieldExtension, polynomial)) {
            return null;
        }
        Polynomial bring = Optional.ofNullable(bringToField(galoisFieldExtension, polynomial))
                .orElse(galoisFieldExtension.ZERO);
        if (bring.equals(galoisFieldExtension.ZERO)) {
            return null;
        }
        int indexOfBring = galoisFieldExtension.indexOf(bring);
        return galoisFieldExtension.get(inverseOfMultiplication(galoisFieldExtension, indexOfBring));
    }

    static int bringToField(GaloisFieldExtension galoisFieldExtension, int index){
        if(checkNullable(galoisFieldExtension)){
            return 0;
        }
        int elementCount = galoisFieldExtension.getCharacteristic();
        index %= elementCount;
        return index < 0 ? inverseOfAddition(galoisFieldExtension, -index) : index;
    }

    static Polynomial bringToField(GaloisFieldExtension galoisFieldExtension, Polynomial polynomial){
        if(checkNullable(galoisFieldExtension, polynomial)){
            return null;
        }
        GaloisField galoisField = galoisFieldExtension.getGaloisField();
        Polynomial bringPolynomial = galoisField.bringToField(polynomial);
        if(bringPolynomial == null) {
            return null;
        }
        bringPolynomial = galoisField.mod(bringPolynomial, galoisFieldExtension.getPolynomial());
        return bringPolynomial;
    }

    static int inverseOfAddition(GaloisFieldExtension galoisFieldExtension, int index){
        if(!isInBounds(galoisFieldExtension, index)){
            return -1;
        }
        return inverseOf(galoisFieldExtension.additionMatrix, index, 0);
    }

    static int inverseOfMultiplication(GaloisFieldExtension galoisFieldExtension, int index){
        if(!isInBounds(galoisFieldExtension, index)){
            return -1;
        }
        return inverseOf(galoisFieldExtension.multiplicationMatrix, index, 1);
    }

    static Polynomial normalize(GaloisFieldExtension galoisFieldExtension, Polynomial polynomial){
        if(checkNullable(galoisFieldExtension, polynomial)){
            return null;
        }
        int[] coefficients = Arrays.stream(polynomial.getCoefficients())
                .map(x -> x % galoisFieldExtension.getCharacteristic())
                .toArray();
        return new Polynomial(coefficients);
    }

    private static int inverseOf(int[][] operationMatrix, int index, int neutralElement){
        OptionalInt inverse = IntStream.range(0, operationMatrix.length)
                .filter(i -> operationMatrix[index][i] == neutralElement)
                .findFirst();
        if(inverse.isEmpty()){
            return -1;
        }
        return inverse.getAsInt();
    }

    static boolean isInBounds(GaloisFieldExtension galoisFieldExtension, int number){
        return number >= 0 && number < galoisFieldExtension.getCharacteristic();
    }

    static boolean isNormalized(GaloisFieldExtension galoisFieldExtension, Polynomial polynomial){
        if(checkNullable(galoisFieldExtension, polynomial)){
            return false;
        }
        return Arrays.stream(polynomial.getCoefficients()).allMatch(x ->
                x >= 0 && x < galoisFieldExtension.getCharacteristic());
    }

    static boolean isPrimitive(GaloisFieldExtension galoisFieldExtension, int element){
        if(Objects.isNull(galoisFieldExtension)){
            return false;
        }
        HashSet<Integer> generatingElements = new HashSet<>(){{add(0);}};
        for(int i = 1; i <= galoisFieldExtension.getCharacteristic(); i++){
            generatingElements.add(powMod(galoisFieldExtension, element, i));
        }
        return generatingElements.size() == galoisFieldExtension.getCharacteristic();
    }

    static boolean isPrimitive(GaloisFieldExtension galoisFieldExtension, Polynomial polynomial){
        if(checkNullable(galoisFieldExtension, polynomial)){
            return false;
        }
        if(!galoisFieldExtension.isInField(polynomial)){
            return false;
        }
        int polynomialI = galoisFieldExtension.indexOf(polynomial);
        return isPrimitive(galoisFieldExtension, polynomialI);
    }

    private static boolean checkNullable(Object ... objects){
        return Arrays.stream(objects).anyMatch(Objects::isNull);
    }

}
