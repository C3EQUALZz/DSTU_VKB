package dstu.csae.comparison.first_degree;

import dstu.csae.comparison.Comparison;
import dstu.csae.diophantine_equation.TwoVariableCase;
import dstu.csae.exceptions.ExceptionMessageConstants;
import lombok.Getter;
import dstu.csae.mathutils.MathUtils;
import dstu.csae.utils.Constants;

import java.util.ArrayList;

@Getter
public class DiophantineCase implements  Case, ExceptionMessageConstants {

    private final int coefficient;
    private final int remains;
    private final int field;

    public DiophantineCase (int coefficient, int remains, int field){
        this.coefficient = coefficient;
        this.remains = remains;
        this.field = field;
    }

    public static ArrayList<Comparison> solve(DiophantineCase diophantine)
        throws ArithmeticException{
        int a = diophantine.getCoefficient();
        int b = diophantine.getRemains();
        int m = diophantine.getField();
        if (!Case.checkSolvability(a, b, m)){
            throw new ArithmeticException(String.format(COMPARISON_IS_NOT_SOLVABLE, diophantine, a, m, b));
        }
        int gcd = MathUtils.getGCD(a, m);
        a /= gcd;
        b /= gcd;
        int m1 = m / gcd;
        int solution = TwoVariableCase.getSolve(new TwoVariableCase(a, m1, b)).get(0) % m1;
        ArrayList<Comparison> solutionList = new ArrayList<>();
        for (int i = 0; i < gcd; i ++){
            solutionList.add(new Comparison(solution + i * m1, m));
        }
        return solutionList;
    }

    @Override
    public String toString(){
        String pattern = "%dx " + Constants.COMPARISON_SYMBOL + " %d(mod %d)";
        return String.format(pattern, coefficient, remains, field);
    }

}
