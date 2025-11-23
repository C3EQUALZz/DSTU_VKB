package dstu.csae.continuous_fraction;

import dstu.csae.exceptions.ExceptionMessageConstants;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.stream.Collectors;

public class ContinuousFraction implements ExceptionMessageConstants {

    private Fraction[] coefficients;
    private Fraction[] suitableFractions;

    private ContinuousFraction() {}

    public ContinuousFraction(Fraction[] coefficients){
        setCoefficients(coefficients);
    }

    public ContinuousFraction(Fraction fraction){
        this(getContinuousFraction(fraction));
    }

    public ContinuousFraction(ContinuousFraction fraction){
        this(fraction.getCoefficients());
    }

    public Fraction[] getCoefficients(){
        return Arrays.copyOf(coefficients, coefficients.length);
    }

    public static ContinuousFraction getContinuousFraction(Fraction fraction)
            throws IllegalArgumentException{
        if(fraction.getDenominator() == 0){
            throw new IllegalArgumentException(ATTEMPT_DIVIDE_BY_ZERO);
        }
        int numerator = Math.abs(fraction.getNumerator());
        int denominator = Math.abs(fraction.getDenominator());
        ArrayList<Fraction> coefficients = new ArrayList<>();
        int iteration = 1;
        int b = 1;
        int a = numerator / denominator;
        coefficients.add(new Fraction(b, a));
        while (numerator > 0 && iteration < 1000000){
            a = denominator / numerator;
            int temp = denominator % numerator;
            denominator = numerator;
            numerator = temp;
            coefficients.add(new Fraction(b, a));
            iteration ++;
        }
        return new ContinuousFraction(coefficients.toArray(new Fraction[0]));
    }

    public void setCoefficients(Fraction[] coefficients)
            throws IllegalArgumentException{
        int lastIndex = coefficients.length - 1;
        if(coefficients[lastIndex].getDenominator() == 0){
            throw new IllegalArgumentException(LAST_FRACTION_DENOMINATOR_IS_ZERO);
        }
        this.coefficients = Arrays.copyOf(coefficients, coefficients.length);
        int[] Q = new int[coefficients.length + 1];
        int[] P = new int[coefficients.length + 1];
        suitableFractions = new Fraction[P.length];
        P[0] = 1;
        Q[0] = 0;
        Q[1] = 1;
        P[1] = getCoefficient(0).getDenominator();
        for(int index = 2; index < P.length; index ++){
            int numerator = coefficients[index - 1].getNumerator();
            int denominator = coefficients[index - 1].getDenominator();
            P[index] = denominator * P[index - 1] + numerator * P[index - 2];
            Q[index] = denominator * Q[index - 1] + numerator * Q[index - 2];
        }
        for(int index = 0; index < P.length; index ++) {
            suitableFractions[index] = new Fraction(P[index], Q[index]);
        }
    }

    public int getK(){
        return coefficients.length - 1;
    }

    public Fraction getSuitableFraction(int index)
        throws IndexOutOfBoundsException{
        if (index < -1 && index > getK()){
            throw new IndexOutOfBoundsException();
        }
        return new Fraction(suitableFractions[index + 1]);
    }

    public Fraction getCoefficient(int index)
        throws IndexOutOfBoundsException{
        if (index < 0 || index > coefficients.length){
            throw new IndexOutOfBoundsException(INDEX_OUT_OF_BOUNDS);
        }
        return new Fraction(coefficients[index]);
    }

    @Override
    public String toString(){
        return "[" + Arrays.stream(coefficients)
                .map(String :: valueOf)
                .collect(Collectors.joining(", ")) + "]";
    }
}
