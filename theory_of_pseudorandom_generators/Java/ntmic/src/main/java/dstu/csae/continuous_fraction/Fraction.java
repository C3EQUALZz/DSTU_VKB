package dstu.csae.continuous_fraction;

import dstu.csae.exceptions.ExceptionMessageConstants;
import lombok.Getter;
import dstu.csae.mathutils.MathUtils;

import java.util.Objects;

@Getter
public class Fraction implements ExceptionMessageConstants {

    private int numerator;
    private int denominator;

    public Fraction(Fraction fraction){
        this(fraction.getNumerator(), fraction.getDenominator());
    }

    public Fraction(int numerator, int denominator){
        setCoefficients(numerator, denominator);
    }

    public void setCoefficients(int numerator, int denominator)
        throws IllegalArgumentException{
        if (numerator == 0 && denominator == 0){
            throw new IllegalArgumentException(INVALID_ARGUMENTS_MESSAGE);
        }
        this.numerator = numerator;
        this.denominator = denominator;
    }

    public int getDiv(){
        return numerator / denominator;
    }

    public int getMod(){
        return numerator % denominator;
    }

    public double count() throws ArithmeticException{
        if (denominator == 0){
            throw new ArithmeticException(ATTEMPT_DIVIDE_BY_ZERO);
        }
        return (double) numerator / denominator;
    }


    @Override
    public boolean equals(Object o){
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Fraction fraction = (Fraction) o;
        int thisGSD = MathUtils.getGCD(getNumerator(), getDenominator());
        int oGSD = MathUtils.getGCD(fraction.getNumerator(), fraction.getDenominator());
        return numerator / thisGSD == fraction.numerator / oGSD &&
                denominator / thisGSD == fraction.denominator / oGSD;
    }

    @Override
    public int hashCode() {
        return Objects.hash(numerator, denominator);
    }

    @Override
    public String toString(){
        return numerator + "/" + denominator;
    }
}
