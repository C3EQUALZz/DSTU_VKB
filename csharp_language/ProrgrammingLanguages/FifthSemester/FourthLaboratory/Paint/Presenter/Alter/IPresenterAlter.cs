using System.Windows.Forms;


namespace DoAnPaint.Presenter.Alter
{
    /// <summary>
    /// Интерфейс, который обновляет приложение по запросам пользователей
    /// </summary>
    interface IPresenterAlter
    {
        /// <summary>
        /// Нажатие на одну из кнопок с разделом группировок изображения 
        /// </summary>
        void OnClickDrawGroup();

        /// <summary>
        /// Способ разгруппировать изображение
        /// </summary>
        void OnClickDrawUnGroup();

        /// <summary>
        /// Обработчик на удаление формы
        /// </summary>
        void OnClickDeleteShape();

        /// <summary>
        /// Обработчик событий на удаление всего
        /// </summary>
        void OnClickClearAll(PictureBox picturebox);

        /// <summary>
        /// Способ сохранения изображения
        /// </summary>
        void OnClickSaveImage(PictureBox picturebox);

        /// <summary>
        /// Способ открытия изображения в PictureBox
        /// </summary>
        void OnClickOpenImage(PictureBox picturebox);

        /// <summary>
        /// Метод создания нового рисунка из PictureBox
        /// </summary>
        void OnClickNewImage(PictureBox picturebox);

        /// <summary>
        /// Способ вызова приложения из PictureBox
        /// </summary>
        void OnClickShutdown(PictureBox picturebox);

        /// <summary>
        /// Метод обработки нажатий клавиш в PictureBox
        /// </summary>
        void OnUseKeyStrokes(PictureBox picturebox, Keys key);

    }
}
