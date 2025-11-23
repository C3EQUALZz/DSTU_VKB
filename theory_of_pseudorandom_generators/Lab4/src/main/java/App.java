import dstu.csae.polynomial.Polynomial;
import dstu.csae.topg.generator.GeffenGenerator;
import dstu.csae.topg.register.Register;
import lombok.NonNull;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import java.util.stream.LongStream;

public class App {

    public static final String FILE_PATH = System.getProperty("user.home") +
            File.separator + "Desktop" + File.separator + "Geffen.txt";

    public static void main(String[] args) {
        /*Register register1 = getRegister(1);
        Register register2 = getRegister(2);
        Register register3 = getRegister(3);*/
        Register register1 = new Register(
                new Polynomial(new int[]{1, 1, 0, 1, 1, 1}),
                new int[]{1, 0, 1, 0, 1},
                4,
                1);
        Register register2 = new Register(
                new Polynomial(new int[]{1, 1, 1}),
                new int[]{1, 0},
                5,
                0);
        Register register3 = new Register(
                new Polynomial(new int[]{1, 0, 1, 1, 0, 1, 1}),
                new int[]{1, 0, 1, 0, 1, 0},
                4,
                2);
        GeffenGenerator generator = new GeffenGenerator(
                register1,
                register2,
                register3
        );
        System.out.println(generator);
        String states = printStates(generator, " -> ");
        System.out.println(states);
        int numberCount = inputCount();
        String sequence = generator.getSequence();
        int maxBitCount = sequence.length() / numberCount;
        String decimalSequence = IntStream.range(0, numberCount)
                .mapToObj(x -> {
                    int startIndex = x * maxBitCount;
                    int endIndex = Math.min(startIndex + maxBitCount, sequence.length());
                    BigInteger num = new BigInteger(sequence.substring(startIndex, endIndex), 2);
                    return num.toString();
                }).collect(Collectors.joining("\t"));
        System.out.println(decimalSequence);
        saveSequence(generator, decimalSequence);
    }

    public static Register getRegister(int index){
        Register reg = null;
        Scanner scanner = new Scanner(System.in);
        while (reg == null){
            String query = "Введите коэффициенты полинома для регистра № " + index + ": ";
            System.out.print(query);
            Polynomial polynomial = new Polynomial();
            try{
                int[] coefficients = Arrays.stream(scanner.nextLine().split("\\s"))
                        .mapToInt(Integer::parseInt)
                        .toArray();
                polynomial = new Polynomial(coefficients);
            }catch (Exception ex){
                System.out.println(ex.getMessage());
                continue;
            }
            query = "Введите значение сдвига для регистра № " + index + ": ";
            System.out.print(query);
            int k;
            try{
                k = Integer.parseInt(scanner.nextLine());
            }catch (Exception ex){
                System.out.println(ex.getMessage());
                continue;
            }
            query = "Введите начальные значения ячеек регистра: ";
            System.out.print(query);
            int[] startState;
            try{
                startState = Arrays.stream(scanner.nextLine().split("\\s"))
                        .mapToInt(Integer::parseInt)
                        .toArray();
            }catch (Exception ex){
                System.out.println(ex.getMessage());
                continue;
            }
            try{
                reg = new Register(polynomial, startState, k, startState.length-1);
            }catch (Exception ex){
                System.out.println(ex.getMessage());
            }
        }
        return reg;
    }

    public static int inputCount(){
        String query = "Введите количество чисел для перевода в 10-ную систему: ";
        Scanner scanner = new Scanner(System.in);
        int count = -1;
        while (count < 1){
            System.out.print(query);
            try {
                count = Integer.parseInt(scanner.nextLine());
            }catch (Exception ex){
                System.out.println(ex.getMessage());
            }
        }
        return count;
    }

    public static String printStates(@NonNull GeffenGenerator generator,
                                     @NonNull String separator){
        List<String> out = new ArrayList<>();
        for(int i = 0; i < generator.getPeriod(); i ++){
            int[] arr = generator.nextArray();
            int result = ((arr[0] & arr[1]) + (arr[1] & arr[2])) % 2;
            result = (result + arr[2]) % 2;
            String state = stateToString(arr);
            out.add(i + ". " + state +
                    separator + result);
        }
        return String.join("\n", out);
    }

    private static String stateToString(int[] state){
        return Arrays.stream(state)
                .mapToObj(String::valueOf)
                .collect(Collectors.joining(""));
    }

    public static void saveSequence(GeffenGenerator generator,
                                    String decimalSequence){
        try(FileWriter writer = new FileWriter(FILE_PATH)){
            writer.write(generator.toString() + "\n");
            writer.write(printStates(generator, " ") + "\n");
            writer.write("Десятичные значения: " + "\n");
            writer.write(decimalSequence);
        } catch (IOException e) {
            System.out.println("Не удалось сохранить данные: " + e.getMessage());
        }
    }

}
