package dstu.csae.galois;

import dstu.csae.exceptions.ExceptionMessageConstants;
import dstu.csae.exceptions.ReverseElementEvaluationException;
import dstu.csae.math.ArithmeticFunctions;
import dstu.csae.polynomial.Polynomial;
import lombok.Getter;

import java.math.BigInteger;
import java.security.InvalidParameterException;
import java.util.Arrays;
import java.util.Optional;
import java.util.stream.IntStream;

public class GaloisField implements Field<Integer>, Cloneable{

    @Getter private int characteristic;
    private int[] elements;
    private static final int ZERO = 0;
    private static final int ONE = 1;
    private GaloisField(){}

    public GaloisField(int characteristic){
        if(!ArithmeticFunctions.isPrime(characteristic) || characteristic < 1){
            throw new InvalidParameterException(
                    String.format(ExceptionMessageConstants.NUMBER_IS_NOT_PRIME,
                            characteristic)
            );
        }
        this.characteristic = characteristic;
        generateElements();
    }

    public int[] getElements(){
        return Arrays.copyOf(elements, elements.length);
    }

    public int bringToField(int number){
        return FieldOperations.bringToField(this, number);
    }

    public int bringToField(BigInteger number){
        return FieldOperations.bringToField(this, number);
    }

    public Polynomial bringToField(Polynomial Polynomial){
        return FieldOperations.bringToField(this, Polynomial);
    }

    @Override
    public Integer add(Integer first, Integer second){
        return FieldOperations.addition(this, first, second);
    }

    @Override
    public Integer subtract(Integer reduced, Integer subtracted){
        return FieldOperations.subtraction(this, reduced, subtracted);
    }
    @Override
    public Integer multiply(Integer first, Integer second){
        return FieldOperations.multiplication(this, first, second);
    }

    @Override
    public Integer divide(Integer divisible, Integer divisor)
            throws ArithmeticException{
        return FieldOperations.division(this, divisible, divisor);
    }

    @Override
    public Integer zero() {
        return ZERO;
    }

    @Override
    public Integer one() {
        return ONE;
    }

    public Polynomial add(Polynomial first, Polynomial second){
        return FieldOperations.addition(this, first, second);
    }

    public Polynomial subtract(Polynomial reduced, Polynomial subtracted){
        return FieldOperations.subtraction(this, reduced, subtracted);
    }

    public Polynomial multiply(Polynomial first, Polynomial second){
        return FieldOperations.multiplication(this, first, second);
    }

    public Polynomial divide(Polynomial divisible, Polynomial divisor){
        return FieldOperations.division(this, divisible, divisor);
    }

    public int mod(int divisible, int divisor){
        return FieldOperations.mod(this, divisible, divisor);
    }

    public Polynomial mod(Polynomial divisible, Polynomial divisor){
        return FieldOperations.mod(this, divisible, divisor);
    }

    public int powMod(int number, int degree){
        return FieldOperations.powMod(this, number, degree);
    }

    public int inverseOfAddition(int number){
        return FieldOperations.inverseOfAddition(this, number);
    }

    public int inverseOfMultiplication(int number)
            throws ReverseElementEvaluationException {
        return FieldOperations.inverseOfMultiplication(this, number);
    }

    public boolean isInField(int number){
        return FieldOperations.isInField(this, number);
    }

    public boolean isInField(Polynomial Polynomial){
        return FieldOperations.isInField(this, Polynomial);
    }

    @Override
    public Integer findFirstPrimitive() {
        return Arrays.stream(elements)
                .filter(this::isPrimitive)
                .findFirst()
                .orElse(-1);
    }

    public boolean isPrimitive(int element){
        return FieldOperations.isPrimitive(this, element);
    }

    public boolean isIrreducible(Polynomial polynomial)
            throws IllegalArgumentException{
        Optional.ofNullable(polynomial).orElseThrow(() ->
                new IllegalArgumentException(ExceptionMessageConstants.POLYNOMIAL_IS_NULL));
        return FieldOperations.isIrreducible(this, polynomial);
    }

    public boolean isNormalized(Polynomial polynomial){
        Optional.ofNullable(polynomial).orElseThrow(() ->
                new IllegalArgumentException(ExceptionMessageConstants.POLYNOMIAL_IS_NULL));
        return FieldOperations.isNormalized(this, polynomial);
    }

    private void generateElements(){
        elements = IntStream.range(0, characteristic).toArray();
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        GaloisField galoisField = (GaloisField) o;
        return characteristic == galoisField.characteristic;
    }

    @Override
    public int hashCode() {
        return characteristic;
    }

    @Override
    public String toString() {
        return String.format("GF(%d)",
                characteristic);
    }

    @Override
    public GaloisField clone() {
        try {
            GaloisField clone = (GaloisField) super.clone();
            clone.elements = getElements();
            return clone;
        } catch (CloneNotSupportedException e) {
            throw new AssertionError();
        }
    }
    

}
