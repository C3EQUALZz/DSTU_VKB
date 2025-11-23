package dstu.csae.polynomial;

import dstu.csae.exceptions.EmptyCoefficientsException;
import dstu.csae.exceptions.ExceptionMessageConstants;
import dstu.csae.index.Index;
import lombok.NonNull;

import java.math.BigInteger;
import java.util.Arrays;
import java.util.Objects;
import java.util.Optional;
import java.util.stream.IntStream;

public class Polynomial implements Comparable<Polynomial>, Cloneable{
    public static final Polynomial ZERO = new Polynomial(new int[]{0});
    public static final Polynomial ONE = new Polynomial(new int[]{1});

    protected int[] coefficients;

    public Polynomial() throws EmptyCoefficientsException{
        this(1);
    }

    public Polynomial(int degree) throws EmptyCoefficientsException{
        this(new int[degree + 1]);
    }

    public Polynomial(int[] coefficients) throws EmptyCoefficientsException{
        this.coefficients = setCoefficients(coefficients);
    }

    protected int[] setCoefficients(int[] coefficients) throws EmptyCoefficientsException{
        if(coefficients == null || coefficients.length == 0){
            throw new EmptyCoefficientsException(ExceptionMessageConstants.EMPTY_COEFFICIENTS);
        }
        return coefficients;
    }

    public int getDegree(){
        return removeLastZero(this).length - 1;
    }

    public int get(int degree) throws IndexOutOfBoundsException{
        if(!isInBounds(degree)){
            throw new IndexOutOfBoundsException(String.format(
                    ExceptionMessageConstants.POLYNOMIAL_INDEX_OUT_OF_BOUNDS,
                    this,
                    degree
            ));
        };
        return coefficients[degree];
    }

    public int[] getCoefficients(){
        return Arrays.copyOf(coefficients, coefficients.length);
    }

    public int evaluate(int x){
        return evaluate(BigInteger.valueOf(x)).intValue();
    }

    public BigInteger evaluate(@NonNull BigInteger x){
        BigInteger result = BigInteger.ZERO;
        for(int deg = 0; deg < coefficients.length; deg++){
            result = x.pow(deg)
                    .multiply(BigInteger.valueOf(coefficients[deg]))
                    .add(result);
        }
        return result;
    }

    public double evaluate(double x){
        return IntStream.range(0, coefficients.length)
                .mapToDouble(degree -> (Math.pow(x, degree) * coefficients[degree])).sum();
    }

    public void set(int degree, int coefficient){
        isInBounds(degree);
        coefficients[degree] = coefficient;
    }

    public Polynomial add(Polynomial p){
        return PolynomialOperations.addition(this, p);
    }

    public Polynomial subtract(Polynomial p){
        return PolynomialOperations.subtraction(this, p);
    }

    public Polynomial multiply(Polynomial p){
        return PolynomialOperations.multiplication(this, p);
    }

    public Polynomial divide(Polynomial p){
        return PolynomialOperations.division(this, p);
    }

    public Polynomial mod(Polynomial p){
        return PolynomialOperations.mod(this, p);
    }

    public boolean isInBounds(int degree) throws IndexOutOfBoundsException{
        return degree >= 0 && degree < coefficients.length;
    }

    public void removeLastZero(){
        this.coefficients = removeLastZero(this);
    }

    static int[] removeLastZero(Polynomial p){
        int lastIndex = p.coefficients.length - 1;
        if(Arrays.stream(p.coefficients).allMatch(i -> i == 0)){
            return new int[]{0};
        }
        for(int i = lastIndex; i >= 1; i --){
            if (p.coefficients[i] != 0){
                break;
            }
            lastIndex --;
        }
        return Arrays.copyOf(p.coefficients,lastIndex + 1);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Polynomial that = (Polynomial) o;
        if(that.getDegree() != ((Polynomial) o).getDegree()) return false;
        int[] thisC = removeLastZero(this);
        int[] thatC = removeLastZero(that);
        if(thisC.length != thatC.length) return false;
        return IntStream.range(0, thisC.length)
                .allMatch(i -> thisC[i] == thatC[i]);
    }

    @Override
    public int hashCode() {
        return Arrays.hashCode(removeLastZero(this));
    }

    public String toString(char symbol){
        int start = 0;
        while(coefficients[start] == 0){
            start ++;
            if(start == coefficients.length){
                start = 0;
                break;
            }
        }

        StringBuilder out = new StringBuilder(String.valueOf(coefficients[start]));
        String monomial;
        if(start != 0){
            monomial = String.valueOf(symbol) + Index.toSuperscript(String.valueOf(start));
            out.append(monomial);
        }
        for(int index = start + 1; index < coefficients.length; index ++){
            int elem = coefficients[index];
            if (elem == 0){
                continue;
            }
            monomial = elem > 0 ? "+" : "";
            monomial += elem + String.valueOf(symbol) + Index.toSuperscript(String.valueOf(index));
            out.append(monomial);
        }
        return out.toString();
    }

    @Override
    public String toString(){
        return toString('x');
    }

    @Override
    public Polynomial clone() {
        try {
            Polynomial clone = (Polynomial) super.clone();
            clone.coefficients = getCoefficients();
            return clone;
        } catch (CloneNotSupportedException e) {
            throw new AssertionError();
        }
    }

    @Override
    public int compareTo(Polynomial o) {
        if (o == null) return 1;

        int thisDeg = this.getDegree();
        int oDeg = o.getDegree();
        if (thisDeg != oDeg) {
            return Integer.compare(thisDeg, oDeg);
        }

        for (int i = thisDeg; i >= 0; i--) {
            int cmp = Integer.compare(this.get(i), o.get(i));
            if (cmp != 0) {
                return cmp;
            }
        }

        return 0;
    }


}
