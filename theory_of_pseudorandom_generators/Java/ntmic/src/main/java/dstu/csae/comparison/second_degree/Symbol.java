package dstu.csae.comparison.second_degree;

import dstu.csae.comparison.Comparison;
import dstu.csae.exceptions.ExceptionMessageConstants;
import dstu.csae.exceptions.WrongArgumentsException;
import dstu.csae.mathutils.MathUtils;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class Symbol implements ExceptionMessageConstants {
    public static int getLegendreSymbol(Comparison comparison)throws WrongArgumentsException {
        int remains = comparison.getRemains();
        int field = comparison.getField();
        if(!MathUtils.isPrime(comparison.getField())){
            throw new WrongArgumentsException(INVALID_ARGUMENTS_MESSAGE);
        }
        if(remains % field == 0){
            return 0;
        }
        if(remains == 1){
            return 1;
        }
        if(remains / field > 0){
            return getLegendreSymbol(new Comparison(remains % field, field));
        }
        if(MathUtils.isPrime(remains) && remains != 2 && field != 2){
            int deg = ((field - 1) / 2) * ((field - 1) / 2);
            if(deg % 2 == 0){
                return getLegendreSymbol(new Comparison(field, remains));
            }
            return -getLegendreSymbol(new Comparison(field, remains));
        }
        ArrayList<Integer> multipliers = MathUtils.getMultipliersList(remains);
        multipliers.remove((Integer) 1);
        multipliers.remove((Integer) remains);
        Map<Integer, Integer> countMap = new HashMap<>();
        multipliers.forEach(n -> {
            if (countMap.containsKey(n)) {
                countMap.put(n, countMap.get(n) + 1);
            } else {
                countMap.put(n, 1);
            }
        });
        countMap.keySet().forEach(k -> {
            if(countMap.get(k) > 1) {
                multipliers.remove(k);
                multipliers.remove(k);
            }
        });
        int leg = 1;
        for(int num : multipliers){
            leg *= getLegendreSymbol(new Comparison(num, field));
        }
        if(remains % 2 == 0){
            int deg = (int)((Math.pow(field, 2) - 1) / 8);
            if(deg % 2 == 0){
                return getLegendreSymbol(new Comparison(remains / 2, field));
            }
            return -getLegendreSymbol(new Comparison(remains / 2, field));
        }

        return leg;
    }

    public static int getJacobiSymbol(Comparison comparison) throws WrongArgumentsException{
        int remains = comparison.getRemains();
        int field = comparison.getField();
        if(MathUtils.isPrime(field)){
            throw new WrongArgumentsException(INVALID_ARGUMENTS_MESSAGE);
        }
        ArrayList<Integer> multipliers = MathUtils.getMultipliersList(field);
        multipliers.remove(0);
        int jac = 1;
        for(int num : multipliers){
            jac *= getLegendreSymbol(new Comparison(remains, num));
        }
        return jac;
    }
}
