using System.Collections.Generic;
using System.Drawing;
using System.Windows.Forms;
using DoAnPaint.Model;



namespace DoAnPaint.View
{
    interface IViewPaint
    {
        /// <summary>
        /// Для перерисовки всего содержимого
        /// </summary>
        void RefreshDrawing();

        /// <summary>
        /// Установите форму указателя мыши
        /// </summary>
        /// <param name="cursor">Форма</param>
        void SetCursor(Cursor cursor);

        /// <summary>
        /// Установить цвет фона
        /// </summary>
        /// <param name="color">Цвет</param>
        void SetColor(Color color);

        /// <summary>
        /// Установить фоновое изображение для кнопки
        /// </summary>
        /// <param name="btn">Кнопка, которой необходимо изменить фон</param>
        /// <param name="color">Цвет</param>
        void SetColor(Button btn, Color color);

        /// <summary>
        /// Метод рисования изображения на графике
        /// </summary>
        /// <param name="shape">Форма, которую нужно нарисовать</param>
        /// <param name="g">графика</param>
        void SetDrawing(Shape shape, Graphics g);

        /// <summary>
        /// Способ нанесения контрольных точек на прямые линии.
        /// </summary>
        void SetDrawingLineSelected(Shape shape, Brush brush,Graphics g);

        /// <summary>
        /// Метод рисования контрольных точек для кривых
        /// </summary>
        void SetDrawingCurveSelected(List<Point> points, Brush brush, Graphics g);

        /// <summary>
        /// Способ рисования контрольных точек для фигур, нарисованных пером.
        /// </summary>
        void SetDrawingRegionRectangle(Pen p, Rectangle rectangle, Graphics g);

        /// <summary>
        /// Метод перемещения фигуры
        /// </summary>
        /// <param name="shape">Изображение нужно переместить</param>
        /// <param name="distance">Расстояние до точки, к которой нужно перенести</param>
        void MovingShape(Shape shape, Point distance);

        /// <summary>
        /// Метод изменения размера изображения в соответствии с контрольными точками
        /// </summary>
        /// <param name="shape">Размер изображения, которое необходимо изменить</param>
        /// <param name="pointCurrent">Точка, куда необходимо изменить местоположение</param>
        /// <param name="previous">Предыдущее место</param>
        /// <param name="indexPoint">Контрольная точка ? </param>
        void MovingControlPoint(Shape shape, Point pointCurrent, Point previous, int indexPoint);
    }
}
