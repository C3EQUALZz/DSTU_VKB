package dstu.csae.topg.generator;

import dstu.csae.index.Index;
import dstu.csae.mathutils.MathUtils;
import lombok.Getter;

import java.math.BigInteger;
import java.util.ArrayList;
import java.util.function.UnaryOperator;


public class SquareCongruentGenerator implements Generator, Periodic{

    @Getter private int a2;
    @Getter private int a1;
    @Getter private int b;
    @Getter private int m;
    @Getter private final BigInteger x0;
    private final UnaryOperator<BigInteger> generator = x -> x
            .pow(2)
            .multiply(BigInteger.valueOf(a2))
            .add(x.multiply(BigInteger.valueOf(a1)))
            .add(BigInteger.valueOf(b))
            .mod(BigInteger.valueOf(m));

    public SquareCongruentGenerator(int a2, int a1, int b, long x0, int m)
        throws IllegalArgumentException{

        setMod(m);
        this.a2 = a2;
        this.a1 = a1;
        this.b = b;
        this.x0 = BigInteger.valueOf(x0);
    }

    private void setMod(int m) throws IllegalArgumentException{
        if(m <= 0){
            throw new IllegalArgumentException(ExceptionConstants.WRONG_MODULO_VALUE);
        }
        this.m = m;
    }

    public ArrayList<BigInteger> getRandomSequence(int count){
        ArrayList<BigInteger> sequence = new ArrayList<>();
        sequence.add(x0);
        BigInteger current = x0;
        for(int i = 0; i < count; i ++){
            current = generate(current);
            sequence.add(current);
        }
        return sequence;
    }

    public BigInteger generate(BigInteger seed){
        return generator.apply(seed);
    }

    public long getPeriod(){
        if(isMaximizedPeriod()){
            return m;
        }
        BigInteger turtle = generate(x0);
        BigInteger hare = generate(generate(x0));
        while(turtle.compareTo(hare) != 0){
            turtle = generate(turtle);
            hare = generate(generate(hare));
        }
        turtle = x0;
        while(turtle.compareTo(hare) != 0){
            turtle = generate(turtle);
            hare = generate(hare);
        }
        hare = generate(turtle);
        long period = 1;
        while(turtle.compareTo(hare) != 0){
            hare = generate(hare);
            period ++;
        }
        return period;
    }

    public int getStartPeriodIndex(){
        if(isMaximizedPeriod()){
            return 0;
        }
        BigInteger turtle = generate(x0);
        BigInteger hare = generate(generate(x0));
        while(turtle.compareTo(hare) != 0){
            turtle = generate(turtle);
            hare = generate(generate(hare));
        }
        turtle = x0;
        int start = 0;
        while(turtle.compareTo(hare) != 0){
            turtle = generate(turtle);
            hare = generate(hare);
            start++;
        }
        return start;
    }

    public boolean isMaximizedPeriod(){
        if(BigInteger.valueOf(b)
                .gcd(BigInteger.valueOf(m))
                .compareTo(BigInteger.ONE) != 0){
            return false;
        }
        if(!MathUtils.getMultipliersList(m)
                .stream()
                .filter(MathUtils::isPrime)
                .allMatch(x -> (a1 - 1) % x == 0 && a2 % x == 0)){
            return false;
        }
        if(m % 4 == 0 && (a1 - 1) % 4 != a2){
            return false;
        }
        return m % 2 == 0 && (a1 - 1) % 2 == a2;
    }

    @Override
    public String toString(){
        ArrayList<String> out = new ArrayList<>(){{
            add("Квадратичный конгруэнтный генератор");
            add("a" + Index.toSubscript("2") + "= " + a2);
            add("a" + Index.toSubscript("1") + "= " + a1);
            add("b= " + b);
            add("m= " + m);
            add("x" + Index.toSubscript("0") + "= " + x0);
            add("Общий вид: ");
            add("x" + Index.toSubscript("n+1") + "≡"
                + a2 + "x" + Index.toSuperscript("2")
                + "+" + a1 + "x" + Index.toSuperscript("1")
                + "+" + b + "(mod " + m + ")");
        }};
        String lineSeparator = System.lineSeparator();
        return String.join(lineSeparator, out);
    }

}
