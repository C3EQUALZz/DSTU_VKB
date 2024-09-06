using System.Drawing;
using System.Windows.Forms;


namespace DoAnPaint.Presenter
{
    /// <summary>
    /// Интерфейс обрабатывает запросы пользователей на манипулирование данными.
    /// </summary>
    internal interface IPresenterDraw
    {
        /// <summary>
        /// Phương thức vẽ một hình lên graphic g
        /// </summary>
        /// <param name="g"></param>
        void GetDrawing(Graphics g);

        /// <summary>
        /// Phương thức xử lý hạ chuột từ người dùng
        /// </summary>
        /// <param name="p"></param>
        void OnClickMouseDown(Point p);

        /// <summary>
        /// Phương thức xử di chuyển chuột từ người dùng
        /// </summary>
        /// <param name="p"></param>
        void OnClickMouseMove(Point p);

        /// <summary>
        /// Phương thức xử thả chuột từ người dùng
        /// </summary>
        void OnClickMouseUp();

        /// <summary>
        /// Вызов метода для рисования линии
        /// </summary>
        void OnClickDrawLine();

        /// <summary>
        /// Метод, который рисует прямоугольник
        /// </summary>
        void OnClickDrawRectangle();

        /// <summary>
        /// Метод, который рисует эллипс
        /// </summary>
        void OnClickDrawEllipse();

        /// <summary>
        /// Метод, который рисует кривую
        /// </summary>
        void OnClickDrawBezier();

        /// <summary>
        /// Метод, который рисует многоугольника
        /// </summary>
        void OnClickDrawPolygon();

        /// <summary>
        /// Метод, который рисует пером
        /// </summary>
        void OnClickDrawPen();

        /// <summary>
        /// Метод, который может стирать нарисованное (ластик)
        /// </summary>
        void OnClickDrawEraser();

        /// <summary>
        /// Метод обработки щелчка правой кнопкой мыши пользователя
        /// </summary>
        void OnClickStopDrawing(MouseButtons mouse);

    }
}
