package dstu.csae.topg;

import com.github.sh0nk.matplotlib4j.Plot;
import com.github.sh0nk.matplotlib4j.PythonExecutionException;
import dstu.csae.mathutils.MathUtils;
import dstu.csae.topg.data.Sequence;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class App {
    public static final String FILE_DIR = String.join(
            File.separator,
            List.of(System.getProperty("user.dir"),
                    "src", "main", "resources")
    ) + File.separator;

    public static void main(String[] args) throws PythonExecutionException, IOException {
        Sequence linear = getSequence(
                FILE_DIR + "LinearCongruent.txt",
                "Линейный генератор");
        Sequence square = getSequence(FILE_DIR + "SquareCongruent.txt",
                "Квадратичный генератор");
        Sequence fibonacci = getSequence(FILE_DIR + "Fibonacci.txt",
                "Генератор Фибоначчи");
        Sequence geffen = getSequence(FILE_DIR + "geffen.txt",
                "Генератор Геффе");
        show(linear, square, fibonacci, geffen);
    }

    public static void show(Sequence ... sequences) throws PythonExecutionException, IOException {
        int with = MathUtils.getMultipliersList(sequences.length)
                .stream()
                .max(Integer :: compareTo)
                .orElse(1);
        int height = sequences.length / with;
        Plot plt = Plot.create();
        for(int i = 0; i < with; i ++){
            for(int j = 0 ; j < height; j ++){
                plt.subplot(with, height, (i * height + j) + 1);
                Sequence s = sequences[i * height + j];
                ArrayList<Integer> x = IntStream.range(0, s.size() - 1)
                        .mapToObj(s :: get)
                        .collect(Collectors.toCollection(ArrayList::new));
                ArrayList<Integer> y = IntStream.range(1, s.size())
                        .mapToObj(s :: get)
                        .collect(Collectors.toCollection(ArrayList::new));
                plt.plot().add(x, y, ".");
                plt.title(s.getTitle());
            }
        }
        plt.show();
    }

    public static Sequence getSequence(String fileName, String title)
            throws RuntimeException{
        ArrayList<Integer> out;
        try(Scanner scanner = new Scanner(new File(fileName))) {
            out = Arrays.stream(scanner.nextLine().split("\t"))
                    .map(Integer::parseInt)
                    .collect(Collectors.toCollection(ArrayList::new));
        } catch (FileNotFoundException e) {
            throw new RuntimeException(e);
        }
        return new Sequence(out, title);
    }

}
