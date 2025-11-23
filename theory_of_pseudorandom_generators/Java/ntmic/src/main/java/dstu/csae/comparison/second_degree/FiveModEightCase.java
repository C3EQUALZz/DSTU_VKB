package dstu.csae.comparison.second_degree;

import dstu.csae.comparison.Comparison;
import dstu.csae.exceptions.ExceptionMessageConstants;
import dstu.csae.exceptions.NoSolutionException;
import dstu.csae.mathutils.MathUtils;

import java.util.ArrayList;

public class FiveModEightCase implements Case, ExceptionMessageConstants {

    public static boolean matches(Comparison comparison) {
        if (!Case.matches(comparison)){
            return false;
        }
        if (comparison.getField() % 8 != 5){
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
        int m = (field - 5) / 8;
        return  getSolvedComparisons(remains, m, field);
    }

    private static ArrayList<Comparison> getSolvedComparisons(int remains, int m, int field) {
        int specialCase = MathUtils.powMod(remains, 2 * m + 1, field);
        int solution = -1;
        if (specialCase == 1){
            solution = MathUtils.powMod(remains, m + 1, field);
        }else{
            solution = MathUtils.powMod(2, 2 * m + 1, field);
            solution *= MathUtils.powMod(remains, m + 1, field);
            solution %= field;
        }
        ArrayList<Comparison> out =  new ArrayList<>();
        out.add(new Comparison(solution, field));
        out.add(new Comparison(-solution, field));
        return out;
    }
}
