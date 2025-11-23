package dstu.csae.curve;

import java.awt.*;

public class CurvePoint extends Point implements Cloneable{

    public CurvePoint() {
        super();
    }

    public CurvePoint(int x, int y) {
        super(x, y);
    }

    @Override
        public String toString(){
            if(!this.equals(EllipticalCurve.O)){
                return "(" + x + ", " + y + ")";
            }
            return "O";
        }

    @Override
    public CurvePoint clone() {
        return (CurvePoint) super.clone();
    }
}
