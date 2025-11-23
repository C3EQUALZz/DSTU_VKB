package dstu.csae.generator.congruent;

import dstu.csae.curve.CurvePoint;
import dstu.csae.curve.EllipticalCurve;
import dstu.csae.generator.Generator;
import lombok.Getter;
import lombok.NonNull;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor
public abstract class AbstractCongruentGenerator implements Generator<CurvePoint>, Periodic{

    protected final EllipticalCurve curve;
    protected final CurvePoint X0;
    protected final CurvePoint P;
    protected  final int c;

    @Override
    public CurvePoint next(@NonNull CurvePoint last){
        CurvePoint result = curve.multiply(last, c);
        return curve.add(result, P);
    }

    @Override
    public long getPeriod(){
        CurvePoint turtle = next(X0);
        CurvePoint hare = next(next(X0));
        while (!hare.equals(turtle)){
            turtle = next(turtle);
            hare = next(next(hare));
        }
        turtle = X0;
        while (!turtle.equals(hare)){
            turtle = next(turtle);
            hare = next(hare);
        }
        hare = next(turtle);
        long period = 1;
        while(!hare.equals(turtle)){
            hare = next(hare);
            period ++;
        }
        return period;
    }



}
