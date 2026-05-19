package org.cequalz;

public class Quadrilateral {

    public static final int MIN_SIDE = 0;
    public static final int MAX_SIDE = 100;

    /**
     * This method finds the area of a regular quadrilateral.
     *
     * @param side1 the length of one side
     * @param side2 the length of the second side
     * @return area of the shape
     *
     * @pre 0 &lt;= side1 &lt;= 100
     * @pre 0 &lt;= side2 &lt;= 100
     */
    public static int area(int side1, int side2) {
        if (side1 < MIN_SIDE || side1 > MAX_SIDE
                || side2 < MIN_SIDE || side2 > MAX_SIDE) {
            throw new IllegalArgumentException(
                    "Стороны должны лежать в диапазоне [" + MIN_SIDE + ", " + MAX_SIDE + "]"
            );
        }
        return side1 * side2;
    }
}
