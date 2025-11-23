package dstu.csae.topg.generator;

import dstu.csae.mathutils.MathUtils;
import dstu.csae.topg.register.Register;
import lombok.Getter;
import lombok.NonNull;

import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

@Getter
public class GeffenGenerator implements Generator, Periodic{

    public static final String PERIODS_ARE_NOT_PRIME = "Значения периодов регистров не взаимно простые";

    private final int[] startPosition;
    private final Register[] registers;
    private final int period;

    public GeffenGenerator(
            @NonNull Register first,
            @NonNull Register second,
            @NonNull Register third){
        if(MathUtils.getGCD(first.getS(), second.getS(), third.getS()) != 1){
            throw new IllegalArgumentException(PERIODS_ARE_NOT_PRIME);
        }
        registers = new Register[3];
        registers[0] = first;
        registers[1] = second;
        registers[2] = third;
        period = setPeriod();
        startPosition = setStartPosition();
    }

    @Override
    public long getPeriod(){
        return period;
    }

    private int setPeriod(){
        int[] sArr = Arrays.stream(registers)
                .mapToInt(Register::getS)
                .toArray();
        return MathUtils.getLCM(sArr);
    }

    private int[] setStartPosition(){
        int[] startState = new int[registers.length];
        IntStream.range(0, registers.length)
                .forEach(index -> {
                    startState[index] = registers[index].next();
                    registers[index].clear();
                });
        return startState;
    }

    public void clear(){
        Arrays.stream(registers)
                .forEach(Register::clear);
    }
    public int nextInt(){
        return Integer.parseInt(IntStream.of(nextArray())
                .mapToObj(String::valueOf)
                .collect(Collectors.joining("")), 2);
    }
    public int nextBit(){
        int[] values = nextArray();
        int result  = ((values[0] & values[1]) + (values[1] & values[2])) % 2;
        return (result + values[2]) % 2;
    }

    public String getSequence(){
        return IntStream.range(0, (int)getPeriod())
                .map(x -> nextBit())
                .mapToObj(String::valueOf)
                .collect(Collectors.joining(""));
    }

    public int[] nextArray(){
        return IntStream.range(0, 3)
                .map(i -> registers[i].next())
                .toArray();
    }

    @Override
    public String toString() {
        List<String> out = new ArrayList<>();
        out.add("Генератор Геффе");
        out.add("Период генератора: " + getPeriod());
        IntStream.range(0, registers.length)
                .forEach(index -> out.add((index + 1) + ". " + registers[index].toString()));
        return String.join("\n", out);
    }
}
