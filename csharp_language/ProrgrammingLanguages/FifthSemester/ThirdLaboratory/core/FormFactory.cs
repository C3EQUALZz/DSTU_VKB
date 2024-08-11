using System.Windows.Forms;

namespace ThirdLaboratory.core
{
    internal class FormFactory
    {
        private readonly Form _mainForm;

        /// <summary>
        /// Класс, который создает форму с заданием, используя паттерн "Простая фабрика"
        /// В конструктор нужно передать ссылку на форму, чтобы была вставка в приложение. 
        /// </summary>
        /// <param name="mainForm">ссылка на родительскую форму, в которую мы будем вставлять наши формы с задаением</param>
        public FormFactory(Form mainForm)
        {
            _mainForm = mainForm;
        }

        /// <summary>
        /// Создает через небольшие хитрости сам объект формы, который используется для создания формы. 
        /// </summary>
        /// <param name="question">номер вопроса, который нужно создать. </param>
        /// <returns>возвращает саму форму для дальнейшей вставки</returns>
        public T Create<T>() where T : Form, new()
        {
            var form = new T
            {
                MdiParent = _mainForm,
                Dock = DockStyle.Fill,
                ControlBox = false
            };

            form.FormClosed += (sender, e) => form = null;

            return form;
        }
    }
}
