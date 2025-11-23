package dstu.csae.comparison.first_degree;

import dstu.csae.mathutils.MathUtils;

public interface Case {

    static boolean checkSolvability(int a, int b, int m){
        int gcd = MathUtils.getGCD(a, m);
        return b % gcd == 0;
    }

}
