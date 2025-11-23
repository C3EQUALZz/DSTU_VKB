package dstu.csae.topg.generator;

import dstu.csae.index.Index;
import dstu.csae.mathutils.MathUtils;
import lombok.Getter;

import java.math.BigInteger;
import java.util.ArrayList;
import java.util.function.UnaryOperator;

public class LinearCongruentGenerator implements Generator, Periodic{

    @Getter  private int a;
    @Getter  private int b;
    @Getter  private BigInteger x0;
    @Getter  private int m;
    private final UnaryOperator<BigInteger> generator = x -> x
            .multiply(BigInteger.valueOf(a))
            .add(BigInteger.valueOf(b))
            .mod(BigInteger.valueOf(m));

    private LinearCongruentGenerator(){}

    public LinearCongruentGenerator(int a, int b, long x0, int m) throws IllegalArgumentException{
        setM(m);
        setA(a);
        setB(b);
        setX0(x0);
    }

    public void setA(int a) throws IllegalArgumentException{
        if (a < 0 || a > m){
            throw new IllegalArgumentException(ExceptionConstants.WRONG_A_PARAMETER_VALUE);
        }
        this.a = a;
    }

    public void setB(int b) throws IllegalArgumentException{
        if(b < 0 || b > m){
            throw new IllegalArgumentException(ExceptionConstants.WRONG_B_PARAMETER_VALUE);
        }
        this.b = b;
    }

    public void setX0(long x0) throws IllegalArgumentException{
        if(x0 < 0 || x0 > m){
            throw new IllegalArgumentException(ExceptionConstants.WRONG_X_PARAMETER_VALUE);
        }
        this.x0 = BigInteger.valueOf(x0);
    }

    public void setM(int m) throws IllegalArgumentException{
        if(m <= 0){
            throw new IllegalArgumentException(ExceptionConstants.WRONG_MODULO_VALUE);
        }
        this.m = m;
    }

    public ArrayList<BigInteger> getRandomSequence(int count){
        BigInteger current = x0;
        ArrayList<BigInteger> sequence = new ArrayList<>(){{
            add(x0);
        }};
        for(int i = 1; i < count; i ++){
            current = generate(current);
            sequence.add(current);
        }
        return sequence;
    }

    public BigInteger generate(BigInteger seed) {
        return generator.apply(seed);
    }



    public boolean isMaximizedPeriod(){
        if(BigInteger.valueOf(b)
                .gcd(BigInteger.valueOf(m)).compareTo(BigInteger.ONE) != 0){
            return false;
        }
        if(MathUtils.getMultipliersList(m).stream()
                .anyMatch(x -> (a - 1) % x != 0)){
            return false;
        }
        if(m % 4 != 0){
            return false;
        }
        return MathUtils.getMultipliersList(m).stream()
                .allMatch(x -> (x - 1) % 4 == 0);
    }

    @Override
    public long getPeriod() {
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

    @Override
    public String toString() {
        String lineSeparator = System.lineSeparator();
        ArrayList<String> out = new ArrayList<>() {{
            add("Линейный конгруэнтный генератор");
            add("a = " + a);
            add("b = " + b);
            add("X0 = " + x0.intValue());
            add("m = " + m);
            add("Общий вид: ");
            add("x" + Index.toSubscript("n+1") + "≡"
                    + a + "*x" + Index.toSubscript("n") + " + " + b
                    + "(mod " + m + ")");
        }};
        return String.join(lineSeparator, out);
    }
}
