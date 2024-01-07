package programmingLanguagesJava.laboratories.firstdotfirstLaboratory;

import java.awt.*;

public class Triangle {
    private final Point point1;
    private final Point point2;
    private final Point point3;

    public Triangle(Point point1, Point point2, Point point3) {
        this.point1 = point1;
        this.point2 = point2;
        this.point3 = point3;
    }

    public double getPerimeter() {
        return calculatePerimeter();
    }

    public Point getX() {
        return point1;
    }

    public Point getY() {
        return point2;
    }

    public Point getZ() {
        return point3;
    }

    private double calculatePerimeter() {
        return distance(point1, point2) + distance(point2, point3) + distance(point3, point1);
    }

    private double distance(Point p1, Point p2) {
        return Math.sqrt(Math.pow(p2.getX() - p1.getX(), 2) + Math.pow(p2.getY() - p1.getY(), 2));
    }
}
