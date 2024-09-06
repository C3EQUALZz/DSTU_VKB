using System.Collections.Generic;
using System.Drawing;
using DoAnPaint.Model;


namespace DoAnPaint.Utils
{
    /// <summary>
    /// Класс, который находит ограничивающую область рисунка
    /// </summary>
    public class FindRegion
    {
        /// <summary>
        /// Метод установки начальной и конечной точек фигуры принадлежит классу GroupShape.
        /// </summary>
        public static void SetPointHeadTail(GroupShape group)
        {
            int minX = int.MaxValue,minY = int.MaxValue;
            int maxX = int.MinValue, maxY = int.MinValue;

            for (int i = 0; i < group.Count; i++)
            {
                Shape shape = group[i];

                if (shape.pointHead.X < minX)
                {
                    minX = shape.pointHead.X;
                }
                if (shape.pointTail.X < minX)
                {
                    minX = shape.pointTail.X;
                }

                if (shape.pointHead.Y < minY)
                {
                    minY = shape.pointHead.Y;
                }
                if (shape.pointTail.Y < minY)
                {
                    minY = shape.pointTail.Y;
                }

                if (shape.pointHead.X > maxX)
                {
                    maxX = shape.pointHead.X;
                }
                if (shape.pointTail.X > maxX)
                {
                    maxX = shape.pointTail.X;
                }

                if (shape.pointHead.Y > maxY)
                {
                    maxY = shape.pointHead.Y;
                }
                if (shape.pointTail.Y > maxY)
                {
                    maxY = shape.pointTail.Y;
                }
            }
            group.pointHead = new Point(minX, minY);
            group.pointTail = new Point(maxX, maxY);
        }

        /// <summary>
        /// Метод установки начальной и конечной точек фигуры принадлежит классу MCurve.
        /// </summary>
        /// <param name="curve"></param>
        public static void SetPointHeadTail(MCurve curve)
        {
            int minX = int.MaxValue, minY = int.MaxValue;
            int maxX = int.MinValue, maxY = int.MinValue;
            curve.points.ForEach(p =>
            {
                if (minX > p.X)
                {
                    minX = p.X;
                }
                if (minY > p.Y)
                {
                    minY = p.Y;
                }
                if (maxX < p.X)
                {
                    maxX = p.X;
                }
                if (maxY < p.Y)
                {
                    maxY = p.Y;
                }
            });
            curve.pointHead = new Point(minX, minY);
            curve.pointTail = new Point(maxX, maxY);
        }

        /// <summary>
        /// Метод установки начальной и конечной точек фигуры принадлежит классу MPolygon.
        /// </summary>
        public static void SetPointHeadTail(MPolygon polygon)
        {
            int minX = int.MaxValue, minY = int.MaxValue;
            int maxX = int.MinValue, maxY = int.MinValue;
            polygon.points.ForEach(p =>
            {
                if (minX > p.X)
                {
                    minX = p.X;
                }
                if (minY > p.Y)
                {
                    minY = p.Y;
                }
                if (maxX < p.X)
                {
                    maxX = p.X;
                }
                if (maxY < p.Y)
                {
                    maxY = p.Y;
                }
            });
            polygon.pointHead = new Point(minX, minY);
            polygon.pointTail = new Point(maxX, maxY);
        }

        /// <summary>
        /// Метод установки начальной и конечной точек изображения принадлежит классу MPen.
        /// </summary>
        public static void SetPointHeadTail(MPen pen)
        {
            int minX = int.MaxValue, minY = int.MaxValue;
            int maxX = int.MinValue, maxY = int.MinValue;
            pen.points.ForEach(p =>
            {
                if (minX > p.X)
                {
                    minX = p.X;
                }
                if (minY > p.Y)
                {
                    minY = p.Y;
                }
                if (maxX < p.X)
                {
                    maxX = p.X;
                }
                if (maxY < p.Y)
                {
                    maxY = p.Y;
                }
            });
            pen.pointHead = new Point(minX, minY);
            pen.pointTail = new Point(maxX, maxY);
        }

        /// <summary>
        /// Метод получения всех контрольных точек фигуры
        /// </summary>
        /// <param name="shape">Изображение должно получить контрольные точки</param>
        /// <returns>Список контрольных точек</returns>
        public static List<Point> GetControlPoints(Shape shape)
        {
            List<Point> points = new List<Point>();
            int xCenter = (shape.pointHead.X + shape.pointTail.X) / 2;
            int yCenter = (shape.pointHead.Y + shape.pointTail.Y) / 2;
            points.Add(new Point(shape.pointHead.X, shape.pointHead.Y));
            points.Add(new Point(xCenter, shape.pointHead.Y));
            points.Add(new Point(shape.pointTail.X, shape.pointHead.Y));
            points.Add(new Point(shape.pointHead.X, yCenter));
            points.Add(new Point(shape.pointTail.X, yCenter));
            points.Add(new Point(shape.pointHead.X, shape.pointTail.Y));
            points.Add(new Point(xCenter, shape.pointTail.Y));
            points.Add(new Point(shape.pointTail.X, shape.pointTail.Y));
            return points;
        }
    }
}
