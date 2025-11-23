package dstu.csae.curve;

import dstu.csae.galois.Field;
import dstu.csae.polynomial.Polynomial;
import lombok.NonNull;

import java.util.AbstractMap;
import java.util.Map;

public class CurveOperations {

    static CurvePoint addition(@NonNull EllipticalCurve curve,
                               @NonNull CurvePoint P,
                               @NonNull CurvePoint Q) {
        if(P.equals(EllipticalCurve.O)){
            return Q;
        }
        if(Q.equals(EllipticalCurve.O)){
            return P;
        }
        Field field = curve.getField();
        if (P.equals(Q)) {
            return doubling(curve, P);
        }
        CurvePoint addition = new CurvePoint();
        int x1 = P.x;
        int y1 = P.y;
        int x2 = Q.x;
        int y2 = Q.y;
        int lambda = field.subtract(y2, y1);
        if(x2 == x1){
            return EllipticalCurve.O;
        }
        lambda = field.divide(lambda, field.subtract(x2, x1));
        int x = field.powMod(lambda, 2);
        x = field.subtract(x, x1);
        x = field.subtract(x, x2);
        int y = field.multiply(lambda, field.subtract(x1, x));
        y = field.subtract(y, y1);
        addition.move(x, y);
        return addition;
    }
    static CurvePoint doubling(@NonNull EllipticalCurve curve,
                          @NonNull CurvePoint P){
        if(P.equals(EllipticalCurve.O)){
            return P;
        }
        final int A_INDEX = 1;
        Field field = curve.getField();
        CurvePoint doubling = new CurvePoint();
        int x1 = P.x;
        int y1 = P.y;
        int lambda = field.powMod(x1, 2);
        lambda = field.multiply(3, lambda);
        lambda = field.add(lambda, curve.getRight().get(A_INDEX));
        if(y1 == 0){
            return EllipticalCurve.O;
        }
        lambda = field.divide(lambda, field.multiply(2, y1));
        int x = field.powMod(lambda, 2);
        x = field.subtract(x, field.multiply(2, x1));
        int y = field.multiply(lambda, field.subtract(x1, x));
        y = field.subtract(y, y1);
        doubling.move(x, y);
        return doubling;
    }

    static CurvePoint multiply(@NonNull EllipticalCurve curve,
                               @NonNull CurvePoint P,
                               @NonNull int c){
        if(c < 0){
            return multiply(curve, curve.getInverse(P), -c);
        }
        if(c == 0){
            return EllipticalCurve.O;
        }
        CurvePoint Q = P.clone();
        if(c == 1){
            return Q;
        }
        c --;
        while(c > 1){
            if(c % 2 != 0){
                Q = addition(curve, P, Q);
                c --;
            }
            P = doubling(curve, P);
            c /= 2;
        }
        return addition(curve, P, Q);
    }



}

