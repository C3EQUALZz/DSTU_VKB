import dstu.csae.polynomial.Polynomial;
import dstu.csae.topg.generator.GeffenGenerator;
import dstu.csae.topg.generator.Generator;
import dstu.csae.topg.generator.LinearCongruentGenerator;
import dstu.csae.topg.generator.SquareCongruentGenerator;
import dstu.csae.topg.register.Register;
import org.jfree.chart.JFreeChart;
import org.jfree.data.category.CategoryDataset;
import org.jfree.data.category.SlidingCategoryDataset;

import javax.swing.*;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;
import java.util.stream.Collectors;

public class Main {

    public static final String LINEAR_GEN_PATH = "src/main/resources/LinearCongruent.txt";
    public static final String SQUARE_GEN_PATH = "src/main/resources/SquareCongruent.txt";
    public static final String FIBONACCI_GEN_PATH = "src/main/resources/Fibonacci.txt";
    public static final String GEFFEN_GEN_PATH = "src/main/resources/Geffen.txt";

    public static void main(String[] args) {
        try{
            Map.Entry<LinearCongruentGenerator, ArrayList<Long>> linear = getLinear(getScanner(LINEAR_GEN_PATH));
            Map.Entry<SquareCongruentGenerator, ArrayList<Long>> square = getSquare(getScanner(SQUARE_GEN_PATH));
            Map.Entry<Register, ArrayList<Long>> fibonacci = getFibonacci(getScanner(FIBONACCI_GEN_PATH));
            Map.Entry<GeffenGenerator, ArrayList<Long>> geffen = getGeffen(getScanner(GEFFEN_GEN_PATH));
            printGenerator(
                    linear,
                    square,
                    fibonacci,
                    geffen);
        }catch (FileNotFoundException ex){
            System.out.println(ex.getMessage());
        }
    }

    @SafeVarargs
    public static void printGenerator(Map.Entry<? extends Generator, ArrayList<Long>> ... generators){
        Arrays.stream(generators)
                .forEach(x ->{
                        System.out.println(x.getKey());
                    SlidingCategoryDataset dataset = StatsGenerator.getDataSet(x.getValue());
                    JFreeChart chart = StatsGenerator.getJFreeChart(
                            x.getKey().toString()
                                    .split("\n")[0],
                            "Значение",
                            "Количество",
                            "",
                            dataset);
                    new Statistic(StatsGenerator.getPanel(chart)).setVisible(true);
                });
    }

    public static Map.Entry<GeffenGenerator, ArrayList<Long>> getGeffen(Scanner scanner)
            throws NumberFormatException{
        Register reg1 = getRegister(scanner);
        Register reg2 = getRegister(scanner);
        Register reg3 = getRegister(scanner);
        ArrayList<Long> data = Arrays.stream(scanner.nextLine().split("\t"))
                .map(Long::parseLong)
                .collect(Collectors.toCollection(ArrayList::new));
        GeffenGenerator geffen = new GeffenGenerator(reg1, reg2, reg3);
        scanner.close();
        return new AbstractMap.SimpleEntry<>(geffen, data);
    }


    public static Register getRegister(Scanner scanner)
            throws NumberFormatException{
        int k = Integer.parseInt(scanner.nextLine());
        int[] coefficients = Arrays.stream(scanner.nextLine().split(" "))
                .mapToInt(Integer::parseInt)
                .toArray();
        int[] start = Arrays.stream(scanner.nextLine().split(" "))
                .mapToInt(Integer::parseInt)
                .toArray();
        return new Register(new Polynomial(coefficients), start, k);
    }

    public static Map.Entry<Register, ArrayList<Long>> getFibonacci(Scanner scanner)
            throws NumberFormatException{
        Register register = getRegister(scanner);
        ArrayList<Long> data = Arrays.stream(scanner.nextLine().split("\t"))
                .map(Long::parseLong)
                .collect(Collectors.toCollection(ArrayList::new));
        scanner.close();
        return new AbstractMap.SimpleEntry<>(register, data);
    }

    public static Map.Entry<LinearCongruentGenerator, ArrayList<Long>> getLinear(Scanner scanner)
            throws NumberFormatException{
        int a = Integer.parseInt(scanner.nextLine());
        int b = Integer.parseInt(scanner.nextLine());
        long x0 = Long.parseLong(scanner.nextLine());
        int m = Integer.parseInt(scanner.nextLine());
        ArrayList<Long> data = Arrays.stream(scanner.nextLine().split("\t"))
                .map(Long::parseLong)
                .collect(Collectors.toCollection(ArrayList::new));
        LinearCongruentGenerator linear = new LinearCongruentGenerator(a, b, x0, m);
        scanner.close();
        return new AbstractMap.SimpleEntry<>(linear, data);
    }

    public static Map.Entry<SquareCongruentGenerator, ArrayList<Long>> getSquare(Scanner scanner)
            throws NumberFormatException{
        int a2 = Integer.parseInt(scanner.nextLine());
        int a1 = Integer.parseInt(scanner.nextLine());
        int b = Integer.parseInt(scanner.nextLine());
        int m = Integer.parseInt(scanner.nextLine());
        long x0 = Long.parseLong(scanner.nextLine());
        ArrayList<Long> data = Arrays.stream(scanner.nextLine().split("\t"))
                .map(Long::parseLong)
                .collect(Collectors.toCollection(ArrayList::new));
        SquareCongruentGenerator square = new SquareCongruentGenerator(a2, a1, b, x0, m);
        scanner.close();
        return new AbstractMap.SimpleEntry<>(square, data);
    }

    public static Scanner getScanner(String path) throws FileNotFoundException {
        return new Scanner(new File(path));
    }

}
