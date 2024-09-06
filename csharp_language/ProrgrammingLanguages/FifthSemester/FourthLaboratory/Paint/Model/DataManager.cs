using DoAnPaint.Utils;
using System.Collections.Generic;
using System.Drawing;


namespace DoAnPaint.Model
{
    /// <summary>
    /// Класс управляет вспомогательными объектами для рисования фигур.
    /// </summary>
    public class DataManager
    {
        public static DataManager instance;

        public List<Shape> ShapeList { get; set; }

        public Shape ShapeToMove { get; set; }

        public Rectangle rectangleRegion;

        public bool IsMouseDown { get; set; }

        public bool IsMovingShape { get; set; }

        public bool IsMovingMouse { get; set; }

        public bool IsDrawingCurve { get; set; }

        public bool IsDrawingPolygon { get; set; }

        public bool IsDrawingPen { get; set; }

        public bool IsDrawingEraser { get; set; }

        public bool IsFill { get; set; }

        public bool IsSave{ get; set; }

        public bool IsNotNone{ get; set; }


        public int PointToResize { get; set; }

        public CurrentShapeStatus CurrentShape { get; set; }

        public Point CursorCurrent { get; set; }

        public Color ColorCurrent { get; set; }

        public int LineSize { get; set; }

        private DataManager()
        {
            ShapeList = new List<Shape>();
            PointToResize = -1;
        }

        public static DataManager getInstance()
        {
            if (instance == null) instance = new DataManager();
            return instance;
        }

        /// <summary>
        /// Метод обновления конечной точки чертежа
        /// </summary>
        /// <param name="p">конечная точка обновления</param>
        public void UpdatePointTail(Point p)
        {
            ShapeList[ShapeList.Count - 1].pointTail = p;
        }

        /// <summary>
        /// =Добавьте объект в список (для дальнейшего выделения)
        /// </summary>
        /// <param name="line">Сущность (форма), которую мы хотим добавить в набор объектов</param>
        public void AddEntity(Shape shape)
        {
            ShapeList.Add(shape);
        }

        /// <summary>
        /// Метод устанавливает для выбранного состояния всех фигур значение false
        /// </summary>
        public void OffAllShapeSelected()
        {
            ShapeList.ForEach(shape => shape.isSelected = false);
        }

        /// <summary>
        /// Метод расчета расстояния между точками y и x
        /// </summary>
        /// <param name="x">кооррдианты точки x</param>
        /// <param name="y">координаты точки y</param>
        /// <returns></returns>
        public Point DistanceXY(Point x, Point y)
        {
            return new Point(y.X - x.X, y.Y - x.Y);
        }

        /// <summary>
        /// Метод обновляет область, представляющую собой прямоугольник, окружающий рисунок
        /// в режиме выбора изображения
        /// </summary>
        public void UpdateRectangleRegion(Point p)
        {         
            rectangleRegion.Width = p.X - rectangleRegion.X;
            rectangleRegion.Height = p.Y - rectangleRegion.Y;
        }
    }
}
