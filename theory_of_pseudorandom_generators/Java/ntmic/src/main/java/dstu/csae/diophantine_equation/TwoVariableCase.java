package dstu.csae.diophantine_equation;

import dstu.csae.continuous_fraction.ContinuousFraction;
import dstu.csae.continuous_fraction.Fraction;
import dstu.csae.exceptions.ExceptionMessageConstants;
import lombok.Getter;
import dstu.csae.mathutils.MathUtils;

import java.util.ArrayList;
import java.util.List;

@Getter
public class TwoVariableCase implements ExceptionMessageConstants {

    private int a;
    private int b;
    private int c;

    public TwoVariableCase(int a, int b, int c){
        this.a = a;
        this.b = b;
        this.c = c;
    }

    public ArrayList<Integer> getSolve(){
        return getSolve(this);
    }

    public static ArrayList<Integer> getSolve(TwoVariableCase equation){
        int a = equation.getA();
        int b = equation.getB();
        int c = equation.getC();
        int gcd = MathUtils.getGCD(a, b);
        if (c % gcd != 0){
            throw new ArithmeticException(String.format(DIOPHANTINE_EQUATION_IS_NOT_SOLVABLE, equation, a, b, c));
        }
        ContinuousFraction fraction = new ContinuousFraction(new Fraction(a, b));
        int k = fraction.getK();
        Fraction suitableFraction = fraction.getSuitableFraction(k - 1);
        int p = suitableFraction.getNumerator();
        int q = suitableFraction.getDenominator();
        int x = (k - 1) % 2 == 0 ? 1 : -1;
        int y = (k - 1) % 2 == 0 ? 1 : -1;
        x *= q * (c / gcd);
        y *= p * (c / gcd);
        return new ArrayList<>(List.of(x, y));
    }

    @Override
    public String toString(){
        return String.format("%dx - %dy = %d", a, b, c);
    }

}
