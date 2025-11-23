package dstu.csae.topg.register;

import lombok.NonNull;

import java.util.Arrays;
import java.util.stream.Collectors;

public class MatrixOperations {

    public static int[][] multiply(@NonNull int[][] A,
                                   @NonNull int[][] B){
        assert A[0].length == B.length;
        int[][] multiplication = new int[A.length][B[0].length];
        for(int i = 0; i < multiplication.length; i ++){
            for (int j = 0; j < multiplication[0].length; j ++){
                for(int k = 0; k < A[0].length; k ++){
                    multiplication[i][j] += A[i][k] * B[k][j];
                    multiplication[i][j] %= 2;
                }
            }
        }
        return multiplication;
    }

    public static String toString(int[][] matrix){
        return Arrays.stream(matrix)
                .map(Arrays::toString)
                .collect(Collectors.joining("\n"));
    }

}
