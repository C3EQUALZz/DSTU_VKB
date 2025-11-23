package dstu.csae.galois;

public abstract class Operations {

    protected static  int[] addition(int[] first, int[] second){
        int minLength = Math.min(first.length, second.length);
        int maxLength = Math.max(first.length, second.length);
        int[] addition = new int[maxLength];
        for(int i = 0; i < minLength; i ++){
            addition[i] += first[i];
            addition[i] += second[i];
        }
        for(int i = minLength; i < maxLength; i ++){
            if(i < first.length - 1){
                addition[i] += first[i];
            }
            if(i < second.length - 1){
                addition[i] += second[i];
            }
        }
        return addition;
    }

    protected static int[] subtraction(int[] reduced, int[] subtracted){
        int minLength = Math.min(reduced.length, subtracted.length);
        int maxLength = Math.max(reduced.length, subtracted.length);
        int[] subtraction = new int[maxLength];
        for(int i = 0; i < minLength; i ++){
            subtraction[i] += reduced[i];
            subtraction[i] -= subtracted[i];
        }
        for(int i = minLength; i < maxLength; i ++){
            if(i < reduced.length - 1){
                subtraction[i] += reduced[i];
            }
            if(i < subtracted.length - 1){
                subtraction[i] -= subtracted[i];
            }
        }
        return subtraction;
    }

    protected static int[] multiplication(int[] first, int[] second){
        int[] multiplication = new int[first.length + second.length - 1];
        for(int i = 0; i < first.length; i ++){
            for(int j = 0; j < second.length; j ++){
                multiplication[i + j] += first[i] * second[j];
            }
        }
        return multiplication;
    }

    protected static int[] division(int[] divisible,int[] divisor){
        int[] division = new int[divisible.length - divisor.length + 1];
        int[] current;
        int divisibleDegree = divisible.length - 1;
        int divisorDegree = divisor.length - 1;
        while(divisibleDegree >= divisorDegree){
            current = new int[divisibleDegree];
            division[divisibleDegree - divisorDegree] = divisible[divisibleDegree] / divisor[divisorDegree];
            current[divisibleDegree - divisorDegree] = division[divisibleDegree - divisorDegree];
            divisible = subtraction(divisible, multiplication(current, divisor));
            divisibleDegree--;
        }
        return division;
    }

}
