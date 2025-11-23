package dstu.csae.curve;

import dstu.csae.galois.Field;
import dstu.csae.polynomial.Polynomial;
import lombok.Getter;
import lombok.NonNull;
import lombok.Setter;

import java.awt.*;
import java.math.BigInteger;
import java.util.*;
import java.util.stream.IntStream;

@Setter
public class EllipticalCurve {

    private static final String ILLEGAL_EQUATION_DEGREE = "Степень уравнения задана неверно";

    public static final CurvePoint O = new CurvePoint(0, 0);
    @Getter private Field field;
    private Map.Entry<Polynomial, Polynomial> equation;
    public EllipticalCurve(@NonNull  Map.Entry<Polynomial, Polynomial> equation,
                           @NonNull Field field)
            throws IllegalArgumentException{
        if(!(equation.getValue().getDegree() == 3 &&
                equation.getKey().getDegree() == 2)){
            throw new IllegalArgumentException(ILLEGAL_EQUATION_DEGREE);
        }
        this.field = field;
        this.equation = equation;
    }

    public Polynomial getLeft(){
        return equation.getKey().clone();
    }

    public Polynomial getRight(){
        return equation.getValue().clone();
    }

    public Set<CurvePoint> getCurvePointSet(){
        TreeSet<CurvePoint> pointSet = new TreeSet<>(new Comparator<Point>() {
            @Override
            public int compare(Point o1, Point o2) {
                if(o1.x == o2.x){
                    return Integer.compare(o1.y, o2.y);
                }
                return Integer.compare(o1.x, o2.x);
            }
        });
        Polynomial left = equation.getKey();
        Polynomial right = equation.getValue();
        int[] x = IntStream.of(field.getElements())
                        .map(element -> field.bringToField(
                                right.evaluate(element)
                                .orElse(BigInteger.ONE))).toArray();
        int[] y = IntStream.of(field.getElements())
                .map(element -> field.bringToField(
                        left.evaluate(element)
                                .orElse(BigInteger.ONE))).toArray();
        for(int i = 0; i < x.length; i ++){
            for(int j = 0; j < y.length; j ++){
                if(x[i] != y[j]){
                    continue;
                }
                pointSet.add(new CurvePoint(i, j));
            }
        }
        pointSet.add(O);
        return pointSet;
    }

    public CurvePoint getInverse(@NonNull CurvePoint P){
        return new CurvePoint(P.x, field.inverseOfAddition(P.y));
    }

    public CurvePoint add(@NonNull CurvePoint P,
                     @NonNull CurvePoint Q){
        return CurveOperations.addition(this, P, Q);
    }

    public CurvePoint multiply(@NonNull CurvePoint P,
                               int c){
        return CurveOperations.multiply(this, P, c);
    }

    public CurvePoint doublePoint(@NonNull CurvePoint P){
        return add(P, P);
    }


    /**
     * @param P - a point on an elliptical curve
     * @return the smallest natural number k such that k * P = O.
     * k = -1 if the point P does not belong to the elliptic curve
     */
    public int getPointOrder(@NonNull CurvePoint P){
        if(!isOnCurve(P)){
            return -1;
        }
        CurvePoint result;
        int iteration = 0;
        do{
            iteration ++;
            result = multiply(P, iteration);
        }while (!result.equals(EllipticalCurve.O));
        return iteration;
    }

    /**
     *
     * @param P - - a point on an elliptical curve
     * @return true if the point belongs to an elliptical curve, and false otherwise.
     */
    public boolean isOnCurve(@NonNull CurvePoint P){
        BigInteger right = getRight().evaluate(P.x)
                .orElse(BigInteger.ONE)
                .mod(BigInteger.valueOf(field.getCharacteristic()));
        BigInteger left = getLeft().evaluate(P.y)
                .orElse(BigInteger.ONE)
                .mod(BigInteger.valueOf(field.getCharacteristic()));
        return right.equals(left);
    }

    @Override
    public String toString() {
        String lineSeparator = System.lineSeparator();
        ArrayList<String> out = new ArrayList<>();
        out.add("Эллиптическая кривая");
        out.add("Поле: " + field.toString());
        out.add(equation.getKey().toString('y') + " = " +
                equation.getValue().toString('x'));
        return String.join(lineSeparator, out);
    }
}
