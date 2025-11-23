package dstu.csae.comparison.second_degree;

import dstu.csae.comparison.Comparison;
import dstu.csae.exceptions.ExceptionMessageConstants;
import dstu.csae.exceptions.NoSolutionException;
import dstu.csae.mathutils.MathUtils;

import java.util.ArrayList;
import java.util.HashMap;

public class GeneralCase implements Case, ExceptionMessageConstants {

    public static ArrayList<Comparison> solve(Comparison comparison){
        if(!Case.matches(comparison)){
            throw new NoSolutionException(
                    String.format(NO_SOLUTION_MESSAGE, "Сравнение")
            );
        }
        int remains = comparison.getRemains();
        int field = comparison.getField();
        int N = 2;
        while (Symbol.getLegendreSymbol(new Comparison(N, field)) != -1){
            N ++;
        }
        HashMap<Integer, Integer> kAndH = MathUtils.getMultipliersMap(field - 1);
        int k = kAndH.get(2);
        int h = (field - 1) / (int) Math.pow(2, k);
        int a1 = MathUtils.powMod(remains, (h + 1) / 2, field);
        int a2 = MathUtils.findInverseElem(remains, field);
        int N1 = MathUtils.powMod(N, h, field);
        int N2 = 1;
        int j = 0;
        for (int i = 0; i <= k - 2; i ++){
            int b = (a1 * N2) % field;
            int c = (a2 * MathUtils.powMod(b, 2, field)) % field;
            int d = MathUtils.powMod(c, (int)Math.pow(2, k - 2 - i), field);
            j = d == 1 ? 0 : 1;
            N2 = (N2 * MathUtils.powMod(N1, (int)(Math.pow(2, i)) * j, field)) % field;
        }
        return getSolvedComparisons(a1, N2, field);
    }

    private static ArrayList<Comparison> getSolvedComparisons(int a, int N, int field){
        return new ArrayList<>(){{
            add(new Comparison((a*N) % field, field));
            add(new Comparison(-(a * N) % field, field));
        }};
    }
}
