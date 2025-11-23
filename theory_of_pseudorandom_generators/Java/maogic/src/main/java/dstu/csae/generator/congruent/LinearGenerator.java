package dstu.csae.generator.congruent;

import dstu.csae.curve.CurvePoint;
import dstu.csae.curve.EllipticalCurve;
import dstu.csae.index.Index;

import java.util.ArrayList;
import java.util.List;

public class LinearGenerator extends AbstractCongruentGenerator{


    public LinearGenerator(EllipticalCurve curve, CurvePoint X0, CurvePoint P, int c) {
        super(curve, X0, P, c);
    }

    @Override
    public String toString() {
        List<String> out = new ArrayList<>();
        out.add("Линейный конгруэнтный генератор");
        out.add("X" + Index.toSubscript("i+1") + " = " + c +
                "X" + Index.toSubscript("i") + " + P" + P);
        out.add("X" + Index.toSubscript("0") + X0);
        out.add("Период равен " + super.getPeriod());
        return String.join("\n", out);
    }

}
