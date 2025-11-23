package dstu.csae.math;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.stream.IntStream;

public class ArithmeticFunctions {

    public static int getEulerFunction(int number){
        if(number == 1){
            return 1;
        }
        if(ArithmeticFunctions.isPrime(number)){
            return number - 1;
        }
        HashMap<Integer, Integer> multipliers = ArithmeticFunctions.getMultipliersMap(number);
        return multipliers.keySet()
                .stream()
                .reduce(1, (accumulator, num) ->
                        accumulator * (num == 1 ? getEulerFunction(num) :
                                (int) (Math.pow(num, multipliers.get(num) - 1) * (num - 1)))
                );
    }

    public static ArrayList<Integer> getMultipliersList(int number){
        if(number == 0){
            return new ArrayList<>();
        }
        ArrayList<Integer> multipliers = new ArrayList<>();
        if(number < 0){
            number = -number;
            multipliers.add(-1);
        }
        int multiplier = 2;
        while (number != 1){
            if(number % multiplier != 0){
                multiplier++;
                continue;
            }
            number /= multiplier;
            multipliers.add(multiplier);
        }
        multipliers.sort(Integer::compareTo);
        return multipliers;
    }

    public static HashMap<Integer, Integer> getMultipliersMap(int number){
        HashMap<Integer, Integer> multipliers = new HashMap<>();
        getMultipliersList(number)
                .forEach(x -> multipliers.put(x, multipliers.getOrDefault(x, 0) + 1));
        return multipliers;
    }


    public static boolean isPrime(int number){
        return number > 1
                && IntStream.rangeClosed(2, (int) Math.sqrt(number))
                .noneMatch(n -> (number % n == 0));
    }
}
