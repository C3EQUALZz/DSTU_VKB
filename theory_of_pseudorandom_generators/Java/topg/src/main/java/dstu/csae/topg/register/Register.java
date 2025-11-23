package dstu.csae.topg.register;

import dstu.csae.galois.Field;
import dstu.csae.polynomial.Polynomial;
import dstu.csae.topg.generator.Generator;
import dstu.csae.topg.generator.Periodic;
import lombok.Getter;
import lombok.NonNull;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.IntStream;

@Getter
public class Register implements Generator, Periodic {


    private static final String WRONG_DEGREE_OR_SP_LENGTH = "Степень многочлена и длина начальной позиции не равны";
    private static final String WRONG_POLYNOMIAL_AFTER_NORMALIZATION = "Полином после нормализации не подходит";

    private final int[][] register;
    private final int[] startPosition;
    private final int[][] T;
    private final int[][] V;
    private final int S;
    private final int lastIndex;
    private final int shift;
    private final int columnIndex;
    private final Polynomial polynomial;

    public Register(@NonNull Polynomial polynomial,
                    @NonNull int[] startPosition,
                    int shift,
                    int columnIndex){
        if(columnIndex < 0 || columnIndex >= startPosition.length){
            throw new IllegalArgumentException("Индекс выходит за пределы границ регистра");
        }
        if(polynomial.getDegree() != startPosition.length){
            throw new IllegalArgumentException(WRONG_DEGREE_OR_SP_LENGTH);
        }
        Polynomial p = normalize(polynomial, new Field(2));
        if(p.getDegree() < 2){
            throw  new IllegalArgumentException(WRONG_POLYNOMIAL_AFTER_NORMALIZATION);
        }
        this.polynomial = p;
        this.shift = shift;

        this.lastIndex = polynomial.getDegree() - 1;
        T = setT();
        V = setV();
        S = (int)Math.pow(2, polynomial.getDegree()) - 1;
        this.startPosition = startPosition;
        this.register = new int[2][polynomial.getDegree()];
        this.columnIndex = columnIndex;
        clear();
    }

    public void clear(){
        register[0] = startPosition;
        register[1] = new int[register[0].length];
    }

    public int next(){
        return next(startPosition.length)[columnIndex];
    }

    public int[] next(int count){
        int length = register[0].length;
        int[] out = Arrays.copyOfRange(register[0], length - count, length);
        step();
        return out;
    }

    private void step(){
        for(int i = 0; i < V.length; i ++) {
            for(int j = 0; j < V[0].length; j ++){
                if(V[i][j] == 0){
                    continue;
                }
                register[1][i] = (register[0][j] + register[1][i]) % 2;
            }
        }
        register[0] = Arrays.copyOf(register[1], register[1].length);
        register[1] = new int[register[0].length];
    }

    private int[][] setT(){
        int[][] T = new int[polynomial.getDegree()][polynomial.getDegree()];
        T[0] = Arrays.copyOfRange(polynomial.getCoefficients(), 1, polynomial.getDegree() + 1);
        IntStream.rangeClosed(1, lastIndex)
                        .forEach(i -> T[i][i-1] = 1);
        return T;
    }

    private int[][] setV(){
        int[][] V = T;
        for(int i = 1; i < shift; i ++){
            V = MatrixOperations.multiply(V, T);
        }
        return V;
    }

    @Override
    public long getPeriod(){
        clear();
        next();
        int period = 1;
        while (!Arrays.equals(register[0], startPosition)){
            next();
            period ++;
        }
        return period;
    }

    private static Polynomial normalize(@NonNull Polynomial polynomial, Field field){
        return field.bringToField(polynomial).orElse(Polynomial.ONE);
    }

    private boolean isInBounds(int index){
        return 0 <= index && index < startPosition.length;
    }

    @Override
    public String toString() {
        List<String> out = new ArrayList<>();
        out.add("Генератор Фибоначчи:");
        out.add("Примитивный многочлен: " + polynomial);
        out.add("Количество ячеек: " + register[0].length);
        out.add("Матрица состояний T: ");
        out.add(MatrixOperations.toString(T));
        out.add("Матрица переходов V: ");
        out.add(MatrixOperations.toString(V));
        out.add("Значение сдвига k: " + shift);
        out.add("Начальное состояние: " + Arrays.toString(startPosition));
        out.add("Период: " + getS());
        return String.join("\n", out);
    }
}
