package dstu.csae;

import dstu.csae.nist.BitFTest;
import dstu.csae.nist.BlockFTest;
import dstu.csae.nist.RunsTest;
import dstu.csae.nist.Test;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.List;
import java.util.Scanner;

public class Main {

    public static final double ALPHA = 0.01;
    public static final List<String> SEQUENCE_FILE_NAMES = List.of(
            "LinearCongruent",
            "SquareCongruent",
            "Fibonacci",
            "Geffen"
    );

    public static void main(String[] args){
        SEQUENCE_FILE_NAMES.forEach(x ->
        {
            String sequence = getSequence(x);
            System.out.println("\nГенератор: " + x);
            System.out.println("Последовательность (" + sequence.length() + " бит): " + sequence);
            int n;
            int m;
            int minM;
            do{
                m = getNumber("m");
                n = sequence.length() / m;
                minM = (int)Math.max(20, 0.01 * n);
                if(m < minM){
                    System.out.println("m должно быть >= " + minM);
                }
                if(m <= 0.01 * n){
                    System.out.println("m должно быть > 0.01 * n");
                }
                if(n >= 100){
                    System.out.println("n должно быть < 100");
                }
            }while (m < minM || m <= 0.01 * n || n >= 100);
            test(sequence, m);
        });
    }

    public static int getNumber(String varName){
        String query = "Введите значение параметра " + varName + ": ";
        String retry = "Повторите попытку";
        Scanner scanner = new Scanner(System.in);
        int val = -1;
        while (val < 0){
            System.out.print(query);
            try{
                val = Integer.parseInt(scanner.nextLine());
            }catch (NumberFormatException ex){
                System.out.println("Ошибка: " + ex.getMessage());
                System.out.println(retry);
            }
        }
        return val;
    }

    public static void test(String sequence, int m){
        final List<Test<String>> tests = List.of(
                new BitFTest(),
                new BlockFTest(m),
                new RunsTest());
        tests.forEach(t -> {
            System.out.println("\n" + t);
            try {
                double a = t.test(sequence);
                System.out.println("PValue = " + a);
                System.out.println("test result: " + (t.isSuccessful(a, ALPHA) ? "success" : "failure"));
            }catch (IllegalArgumentException ex){
                System.out.println("Ошибка: " + ex.getMessage());
            }
        });
    }

    public static String getSequence(String fileName){
        final String DIR_PATH = String.join(File.separator,
                List.of(System.getProperty("user.dir"), "src", "main", "resources")) + File.separator;
        final String FILE_EXTENSION = ".txt";
        String sequence;
        try(Scanner reader = new Scanner(new File(DIR_PATH + fileName + FILE_EXTENSION))){
            sequence = reader.nextLine();
        } catch (FileNotFoundException e) {
            throw new RuntimeException(e);
        }
        return sequence;
    }

}
