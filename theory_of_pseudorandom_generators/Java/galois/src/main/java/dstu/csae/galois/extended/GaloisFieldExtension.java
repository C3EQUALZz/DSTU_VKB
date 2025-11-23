package dstu.csae.galois.extended;

import dstu.csae.exceptions.ExceptionMessageConstants;
import dstu.csae.galois.Field;
import dstu.csae.galois.GaloisField;
import dstu.csae.index.Index;
import dstu.csae.polynomial.Polynomial;
import lombok.Getter;

import java.util.ArrayList;
import java.util.Objects;
import java.util.Optional;
import java.util.stream.IntStream;

public class GaloisFieldExtension implements Field<Polynomial>{

    public final Polynomial ZERO;
    public final Polynomial ONE;
    @Getter
    private final GaloisField galoisField;
    @Getter
    private final int degree;
    @Getter
    private final Polynomial polynomial;
    private final ArrayList<Polynomial> elements;
    final int[][] additionMatrix;
    final  int[][] multiplicationMatrix;


    public GaloisFieldExtension(GaloisField galoisField, Polynomial polynomial)
        throws IllegalArgumentException{
        if(Objects.isNull(galoisField)){
            throw new IllegalArgumentException(ExceptionMessageConstants.FIELD_IS_NULL);
        }
        if(Objects.isNull(polynomial)){
            throw new IllegalArgumentException(ExceptionMessageConstants.POLYNOMIAL_IS_NULL);
        }
        if(!galoisField.isNormalized(polynomial)){
            throw new IllegalArgumentException(
                    String.format(ExceptionMessageConstants.POLYNOMIAL_IS_NOT_NORMALIZED,
                            polynomial, galoisField));
        }
        if(!galoisField.isIrreducible(polynomial)){
            throw new IllegalArgumentException(
                    String.format(ExceptionMessageConstants.POLYNOMIAL_IS_REDUCIBLE,
                            polynomial, galoisField));
        }
        this.galoisField = galoisField;
        this.polynomial = polynomial;
        this.degree = polynomial.getDegree();
        elements = generateElements();
        ZERO = elements.get(0);
        ONE = elements.get(1);
        additionMatrix = generateAdditionMatrix();
        multiplicationMatrix = generateMultiplicationMatrix();
    }


    @Override
    public int getCharacteristic() {
        return elements.size();
    }

    @Override
    public Polynomial findFirstPrimitive() {
        return elements.stream()
                .filter(this::isPrimitive)
                .findFirst()
                .orElse(null);
    }

    public int findFirstIntPrimitive(){
        return indexOf(findFirstPrimitive());
    }

    public Polynomial get(int index){
        if(!isInBounds(index)){
            return null;
        }
        return elements.get(index);
    }

    public int indexOf(Polynomial polynomial){
        if(!isInField(polynomial)){
            return -1;
        }
        return elements.indexOf(polynomial);
    }

    private ArrayList<Polynomial> generateElements(){
        int characteristic = galoisField.getCharacteristic();
        int elementCount = (int)Math.pow(galoisField.getCharacteristic(), degree);
        int[][] coefficients = new int[elementCount][degree];
        int period = 1;
        int currentDegree = 0;
        ArrayList<Polynomial> elements = new ArrayList<>();
        while(currentDegree < degree){
            int currentElementIndex = 0;
            int currentValue = 0;
            while(currentElementIndex < elementCount) {
                for (int i = 0; i < period; i++) {
                    coefficients[currentElementIndex][currentDegree] = currentValue;
                    currentElementIndex++;
                }
                currentValue = (currentValue + 1) % characteristic;
            }
            period *= characteristic;
            currentDegree ++;
        }
        IntStream.range(0, coefficients.length)
                .forEach(index -> elements.add(new Polynomial(coefficients[index])));
        return elements;
    }

    private int[][] generateAdditionMatrix(){
        int[][] additionMatrix = new int[elements.size()][elements.size()];
        for(int i = 0; i < elements.size(); i ++){
            for(int j = 0; j < elements.size(); j ++){
                Polynomial addition = galoisField.add(elements.get(i), elements.get(j));
                addition = galoisField.mod(addition, polynomial);
                additionMatrix[i][j] = elements.indexOf(addition);
            }
        }
        return additionMatrix;
    }

    private int[][] generateMultiplicationMatrix(){
        int[][] multiplicationMatrix = new int[elements.size()][elements.size()];
        for(int i = 0; i < elements.size(); i ++){
            for(int j = 0; j < elements.size(); j ++){
                Polynomial multiplication = galoisField.multiply(elements.get(i), elements.get(j));
                multiplication = galoisField.mod(multiplication, polynomial);
                multiplicationMatrix[i][j] = elements.indexOf(multiplication);
            }
        }
        return multiplicationMatrix;
    }

    @Override
    public Polynomial zero(){
        return ZERO.clone();
    }

    @Override
    public Polynomial one(){
        return ONE.clone();
    }

    @Override
    public Polynomial add(Polynomial first, Polynomial second){
        return ExtendedFieldOperations.addition(this, first, second);
    }

    @Override
    public Polynomial subtract(Polynomial reduced, Polynomial subtracted){
        return ExtendedFieldOperations.subtraction(this, reduced, subtracted);
    }

    @Override
    public Polynomial multiply(Polynomial first, Polynomial second){
        return ExtendedFieldOperations.multiplication(this, first, second);
    }

    @Override
    public Polynomial divide(Polynomial divisible, Polynomial divisor){
        return ExtendedFieldOperations.division(this, divisible, divisor);
    }

    public int add(int first, int second){
        return ExtendedFieldOperations.addition(this, first, second);
    }

    public int subtract(int reduced, int subtracted){
        return ExtendedFieldOperations.subtraction(this, reduced, subtracted);
    }

    public int multiply(int first, int second){
        return ExtendedFieldOperations.multiplication(this, first, second);
    }

    public int divide(int divisible, int divisor){
        return ExtendedFieldOperations.division(this, divisible, divisor);
    }

    public int mod(int divisible, int divisor){
        return ExtendedFieldOperations.mod(this, divisible, divisor);
    }

    public int powMod(int number, int degree){
        return ExtendedFieldOperations.powMod(this, number, degree);
    }

    public Polynomial powMod(Polynomial polynomial, int degree){
        return ExtendedFieldOperations.powMod(this, polynomial, degree);
    }

    public int bringToField(int number){
        return ExtendedFieldOperations.bringToField(this, number);
    }

    public Polynomial bringToField(Polynomial p){
        return Optional.ofNullable(ExtendedFieldOperations.bringToField(this, p))
                .orElse(get(0));
    }

    public int inverseOfAddition(int element){
        return ExtendedFieldOperations.inverseOfAddition(this, element);
    }

    public Polynomial inverseOfAddition(Polynomial polynomial){
        return ExtendedFieldOperations.inverseOfAddition(this, polynomial);
    }

    public int inverseOfMultiplication(int element){
        return ExtendedFieldOperations.inverseOfMultiplication(this, element);
    }

    public Polynomial inverseOfMultiplication(Polynomial polynomial){
        return ExtendedFieldOperations.inverseOfMultiplication(this, polynomial);
    }

    public Polynomial normalize(Polynomial polynomial){
        return ExtendedFieldOperations.normalize(this, polynomial);
    }

    public boolean isInField(Polynomial polynomial){
        if(Objects.isNull(polynomial)){
            return false;
        }
        return elements.contains(polynomial);
    }

    public boolean isInBounds(int index){
        return ExtendedFieldOperations.isInBounds(this, index);
    }

    public boolean isPrimitive(int element){
        return ExtendedFieldOperations.isPrimitive(this, element);
    }

    public boolean isPrimitive(Polynomial polynomial){
        return ExtendedFieldOperations.isPrimitive(this, polynomial);
    }

    public boolean isNormalized(Polynomial polynomial){
        return ExtendedFieldOperations.isNormalized(this, polynomial);
    }

    @Override
    public boolean equals(Object o) {
        if (o == null || getClass() != o.getClass()) return false;
        GaloisFieldExtension that = (GaloisFieldExtension) o;
        return Objects.equals(galoisField, that.galoisField) && Objects.equals(polynomial, that.polynomial);
    }

    @Override
    public int hashCode() {
        return Objects.hash(galoisField, polynomial);
    }

    @Override
    public String toString() {
        return String.format("GF(%s%s)(%s)",
                galoisField.getCharacteristic(),
                Index.toSuperscript(String.valueOf(degree)),
                polynomial);
    }

    public static void main(String[] args) {
        GaloisField field = new GaloisField(2);
        GaloisFieldExtension fieldExtension = new GaloisFieldExtension(field, new Polynomial(new int[]{1, 1, 1}));
        System.out.println(fieldExtension);
    }

}
