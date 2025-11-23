package dstu.csae.nist;

import org.apache.commons.numbers.gamma.Erfc;

import java.util.Arrays;

public class RunsTest implements Test<String>{

    public double test(String sequence) {
        int[] seq = Arrays.stream(sequence.split(""))
                .mapToInt(x -> Byte.parseByte(x, 2))
                .toArray();
        int n = seq.length;
        double oneCount = (double) Arrays.stream(seq).sum() / n;
        if(Math.abs(oneCount - 0.5) >= 2 / Math.sqrt(n)){
            return 0;
        }
        double VnObs = 0;
        for(int i = 0; i < seq.length - 1; i ++){
            if(seq[i] == seq[i + 1]){
                continue;
            }
            VnObs += 1;
        }
        VnObs += 1;
        double pValue = VnObs - 2 * n * oneCount * (1 - oneCount);
        pValue = Math.abs(pValue);
        pValue /= (2 * Math.sqrt(2 * n) * oneCount * (1 - oneCount));
        return Erfc.value(pValue);
    }

    @Override
    public boolean isSuccessful(double actual, double required) {
        return actual >= required;
    }

    @Override
    public String toString() {
        return "Тест на последовательность одинаковых бит";
    }
}
