package dstu.csae.generator.congruent;

import dstu.csae.curve.CurvePoint;
import dstu.csae.curve.EllipticalCurve;
import dstu.csae.index.Index;
import lombok.NonNull;

import java.util.ArrayList;
import java.util.List;

public class InvertedGenerator extends AbstractCongruentGenerator{

    public InvertedGenerator(EllipticalCurve curve, CurvePoint X0, CurvePoint P, int c) {
        super(curve, X0, P, c);
    }

    public CurvePoint next(@NonNull CurvePoint last){
        return super.next(getCurve().getInverse(last));
    }

    @Override
    public String toString() {
        List<String> out = new ArrayList<>();
        out.add("Инверсионный линейный конгруэнтный генератор");
        out.add("X" + Index.toSubscript("i+1") + " = " + c +
                "X" + Index.toSubscript("i") +
                Index.toSuperscript("-1") + " + P" + P);
        out.add("X" + Index.toSubscript("0") + X0);
        out.add("Период равен " + super.getPeriod());
        return String.join("\n", out);
    }
}
