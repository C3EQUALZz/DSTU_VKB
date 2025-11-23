package dstu.csae.mathutils;

import dstu.csae.diophantine_equation.TwoVariableCase;
import dstu.csae.exceptions.ExceptionMessageConstants;
import dstu.csae.exceptions.NoSolutionException;
import dstu.csae.exceptions.WrongArgumentsException;

import java.util.*;
import java.util.stream.IntStream;


public class MathUtils implements ExceptionMessageConstants {

    public static int getLCM(int ... numbers)
            throws RuntimeException{
        if(numbers == null || numbers.length == 0){
            return -1;
        }
        if(numbers.length == 1){
            return numbers[0];
        }
        if(Arrays.stream(numbers).anyMatch(x -> x == 0)){
            throw new RuntimeException(INVALID_ARGUMENTS_MESSAGE);
        }
        int lcm = numbers[0];
        for(int i = 1; i < numbers.length; i ++){
            lcm = getLCM(lcm, numbers[i]);
        }
        return lcm;
    }

    public static int getLCM(int a, int b)
            throws RuntimeException{
        if(a <= 0 || b <= 0){
            throw new RuntimeException(INVALID_ARGUMENTS_MESSAGE);
        }
        if(a == 1){
            return b;
        }
        if(b == 1){
            return a;
        }
        if(isPrime(a) && isPrime(b)){
            return a * b;
        }
        return a * b / getGCD(a, b);
    }

    public static int getGCD(int ... numbers){
        if(numbers == null || numbers.length == 0){
            return -1;
        }
        if(numbers.length == 1){
            return numbers[0];
        }
        if(Arrays.stream(numbers).allMatch(x -> x == 0)){
            throw new RuntimeException(INVALID_ARGUMENTS_MESSAGE);
        }
        int gcd = numbers[0];
        for(int i = 1; i < numbers.length; i ++){
            gcd = getGCD(gcd, numbers[i]);
        }
        return gcd;
    }

    public static int getGCD(int a, int b)throws WrongArgumentsException {
        int d = 1;
        if(a == 0 && b == 0){
            throw new WrongArgumentsException(INVALID_ARGUMENTS_MESSAGE);
        }
        if(a == 0 || b == 0){
            return Math.max(Math.abs(a), Math.abs(b));
        }
        ArrayList<Integer> aMultipliers = getMultipliersList(Math.abs(a));
        ArrayList<Integer> bMultipliers = getMultipliersList(Math.abs(b));
        aMultipliers.retainAll(bMultipliers);
        ArrayList<Integer> common = new ArrayList<>();
        Iterator<Integer> it = aMultipliers.iterator();
        while(it.hasNext()){
            Integer elem = it.next();
            if (bMultipliers.contains(elem)){
                common.add(elem);
                bMultipliers.remove(elem);
                it.remove();
            }
        }
        for(Integer multiplier : common){
           d *= multiplier;
        }
        return d;
    }

    public static ArrayList<Integer> getMultipliersList(int a){
        if(a == 0){
            return new ArrayList<>(List.of(a));
        }
        ArrayList<Integer> mulipliers = new ArrayList<>();
        mulipliers.add(1);
        int divider = 2;
        while(a != 1){
            if(!(a % divider == 0)){
                divider++;
                continue;
            }
            a /= divider;
            mulipliers.add(divider);
        }
        return mulipliers;
    }

    public static HashMap<Integer, Integer> getMultipliersMap(int a){
        HashMap<Integer, Integer> multipliersMap = new HashMap<>();
        getMultipliersList(a).forEach(n -> {
            if (multipliersMap.containsKey(n)) {
                multipliersMap.put(n, multipliersMap.get(n) + 1);
            } else {
                multipliersMap.put(n, 1);
            }
        });
        return multipliersMap;
    }

    public static int getEulerFunction(int number){
        if(number == 1){
            return 1;
        }
        if(MathUtils.isPrime(number)){
            return number - 1;
        }
        HashMap<Integer, Integer> multipliers = MathUtils.getMultipliersMap(number);
        int result = 1;
        for(Map.Entry<Integer, Integer> multiplier : multipliers.entrySet()){
            int deg = multiplier.getValue();
            int num = multiplier.getKey();
            if(deg == 1){
                result *= getEulerFunction(num);
                continue;
            }
            result *= (int) (Math.pow(num, deg - 1) * (num - 1));
        }
        return result;
    }

    public static boolean isPrime(int number){
        return number > 1
                && IntStream.rangeClosed(2, (int) Math.sqrt(number))
                .noneMatch(n -> (number % n == 0));
    }

    public static int powMod(int number, int deg, int mod){
        if (deg == 0){
            return 1;
        }
        int result = 1;
        number %= mod;
        if (deg == 1){
            return number;
        }
        while(deg > 1){
            if(deg % 2 == 0){
                number = (int)(Math.pow(number, 2) % mod);
                deg /= 2;
                continue;
            }
            result *= number;
            deg --;
        }
        return (number * result) % mod;
    }

    public static int findInverseElem(int number, int mod)throws NoSolutionException{
        if (getGCD(number, mod) != 1){
            throw new NoSolutionException(String.format(NO_INVERSE_ELEM, number, mod));
        }
        TwoVariableCase x = new TwoVariableCase(number, mod, 1);
        int solve = x.getSolve().get(0);
        return solve < 0 ? solve + mod : solve;
    }
}
