using System.Drawing;
using System.Windows.Forms;


namespace DoAnPaint.Presenter.Updates
{
    /// <summary>
    /// Интерфейс обрабатывает запросы пользователя на обновление данных
    /// </summary>
    internal interface IPresenterUpdate
    {
        /// <summary>
        /// Метод обработки, когда пользователь выбирает режим "выбор"
        /// </summary>
        void OnClickSelectMode();

        /// <summary>
        /// Метод обработки, когда пользователь решает изменить цвет
        /// </summary>
        /// <param name="color">Цвет, на который необходимо изменить</param>
        /// <param name="g">Применить к графику g</param>
        void OnClickSelectColor(Color color,Graphics g);

        /// <summary>
        /// Метод обработки, когда пользователь решает удвоить размер линии рисования.
        /// </summary>
        void OnClickSelectSize(int size);

        /// <summary>
        /// Метод обработки, когда пользователь выбирает режим заполнения. 
        /// </summary>
        void OnClickSelectFill(Button btn, Graphics g);


    }
}
