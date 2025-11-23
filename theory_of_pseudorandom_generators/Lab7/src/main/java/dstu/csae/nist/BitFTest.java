package dstu.csae.nist;

import java.util.Arrays;
import org.apache.commons.numbers.gamma.Erfc;

public class BitFTest implements Test<String>{

    public double test(String sequence) {
        int[] seq = Arrays.stream(sequence.split(""))
                .mapToInt(x -> Byte.parseByte(x, 2))
                .toArray();
        int sum = Arrays.stream(seq)
                .map(x -> 2 * x - 1)
                .sum();
        int n = seq.length;
        double sObs = Math.abs(sum) / Math.sqrt(n);
        sObs /= Math.sqrt(2);
        return Erfc.value(sObs);
    }

    @Override
    public boolean isSuccessful(double actual, double required) {
        return actual >= required;
    }


    @Override
    public String toString() {
        return "Частотно-побитовый тест";
    }
}
