package dstu.csae.nist;

import org.apache.mahout.math.jet.stat.Gamma;

import java.util.Arrays;


public class BlockFTest implements Test<String>{

    private final int m;

    public BlockFTest(int m){
        this.m = m;
    }

    public double test(String sequence)
            throws IllegalArgumentException{
        int n = sequence.length() / m;
        if(sequence.length() < m * n){
            throw new IllegalArgumentException("Последовательность не подходит для этого теста");
        }
        int[][] seq = new int[n + 1][m];
        for(int i = 0; i < n * m; i ++){
            int row = i / m;
            int column = i % m;
            seq[row][column] = Byte.parseByte(String.valueOf(sequence.charAt(i)));
        }
        double hiSqr = 4 * m;
        for(int[] block : seq){
            double value = (double) Arrays.stream(block).sum() / block.length;
            value -= 0.5;
            value = Math.pow(value, 2);
            hiSqr += value;
        }
        return Gamma.incompleteGamma((double) n / 2, hiSqr / 2);
    }

    @Override
    public boolean isSuccessful(double actual, double required) {
        return actual >= required;
    }

    @Override
    public String toString() {
        return "Частотно-блочный тест";
    }
}
