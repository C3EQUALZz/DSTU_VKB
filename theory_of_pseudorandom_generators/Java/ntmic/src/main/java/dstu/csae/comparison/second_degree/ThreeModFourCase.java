package dstu.csae.comparison.second_degree;

import dstu.csae.comparison.Comparison;
import dstu.csae.exceptions.ExceptionMessageConstants;
import dstu.csae.exceptions.NoSolutionException;
import dstu.csae.mathutils.MathUtils;

import java.util.ArrayList;

public class ThreeModFourCase implements Case, ExceptionMessageConstants {

    public static boolean matches(Comparison comparison) {
        if (!Case.matches(comparison)){
            return false;
        }
        if (comparison.getField() % 4 != 3){
            return false;
        }
        return true;
    }


    public static ArrayList<Comparison> solve(Comparison squareComparison){
        int remains = squareComparison.getRemains();
        int field = squareComparison.getField();
        if(!matches(squareComparison)){
            throw new NoSolutionException(
                    String.format(NO_SOLUTION_MESSAGE, "Сравнение " + squareComparison)
            );
        }
        int m = (field - 3) / 4;
        int solution = MathUtils.powMod(remains, m + 1, field);
        return new ArrayList<>(){{
            add(new Comparison(solution, field));
            add(new Comparison(-solution, field));
        }};
    }
}
