package dstu.csae.comparison;

import dstu.csae.exceptions.ExceptionMessageConstants;
import lombok.Getter;
import dstu.csae.utils.Constants;

@Getter
public class Comparison {

    private final int field;
    private final int remains;

    private static final String COMPARISON_FORMAT = "x " + Constants.COMPARISON_SYMBOL + " %d (mod %d)";

    public Comparison(int remains, int field)
            throws IllegalArgumentException{
        if (field < 2){
            throw new IllegalArgumentException(ExceptionMessageConstants.INVALID_ARGUMENTS_MESSAGE);
        }
        this.field = field;
        this.remains = bringToField(remains, this.getField());
    }

    public static int bringToField(int number, int field){
        number %= field;
        if (number < 0){
            number += field;
        }
        return number;
    }

    @Override
    public String toString(){
        return String.format(COMPARISON_FORMAT, remains, field);
    }

}
