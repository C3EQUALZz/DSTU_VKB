package dstu.csae.matocip.utils;

import lombok.NonNull;

import java.math.BigInteger;
import java.util.ArrayList;

public class EuclidAlgorithms {

    public static DiaphanousEquation gcdEx(@NonNull BigInteger a,
                                   @NonNull BigInteger b){
        ArrayList<BigInteger> q = new ArrayList<>(){{
            add(null);
            add(null);
        }};
        ArrayList<BigInteger> r = new ArrayList<>(){{
            add(a);
            add(b);
        }};
        ArrayList<BigInteger> s = new ArrayList<>(){{
            add(BigInteger.ONE);
            add(BigInteger.ZERO);
        }};
        ArrayList<BigInteger> t = new ArrayList<>(){{
            add(BigInteger.ZERO);
            add(BigInteger.ONE);
        }};
        int i = 1;
        do{
            i ++;
            q.add(r.get(i - 2).divide(r.get(i - 1)));
            r.add(r.get(i - 2).remainder(r.get(i - 1)));
            s.add(s.get(i - 2).subtract(q.get(i).multiply(s.get(i - 1))));
            t.add(t.get(i - 2).subtract(q.get(i).multiply(t.get(i - 1))));
        }while (!r.get(i).equals(BigInteger.ZERO));
        return new DiaphanousEquation(s.get(i - 1), t.get(i - 1), r.get(i - 1));
    }

}
