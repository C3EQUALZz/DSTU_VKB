using System.Linq;
using System;
using System.Windows.Forms;
using ThirdLaboratory.core.interfaces;

namespace ThirdLaboratory.core
{
    internal class FormFactory : IFormFactory
    {
        private readonly Form _mainForm;

        /// <summary>
        /// Класс, который создает форму с заданием, используя паттерн "Простая фабрика"
        /// В конструктор нужно передать Tag формы, а точнее строку оттуда.  
        /// </summary>
        /// <param name="mainForm">ссылка на родительскую форму, в которую мы будем вставлять наши формы с задаением</param>
        public FormFactory(Form mainForm)
        {
            _mainForm = mainForm;
        }

        /// <summary>
        /// Создает через отражение (рефлексия) сам объект формы 
        /// </summary>
        /// <param name="question">номер вопроса, который нужно создать. </param>
        /// <returns>возвращает саму форму для дальнейшей вставки</returns>
        public Form Create(string formName)
        {
            // Используем рефлексию для создания формы на основе имени
            var formType = GetType().Assembly.GetTypes().FirstOrDefault(t => t.Name == formName);
            if (formType != null && formType.IsSubclassOf(typeof(Form)))
            {
                // Используем существующий метод фабрики для инициализации формы
                // Можно сказать, что у нас относительно абстрактная фабрика, но тут же не совсем расширяемый код, как я видел в книгах. 
                var formInstance = (Form)Activator.CreateInstance(formType);
                formInstance.MdiParent = _mainForm;
                formInstance.Dock = DockStyle.Fill;
                formInstance.ControlBox = false;

                formInstance.FormClosed += (sender, e) => formInstance = null;

                return formInstance;
            }

            throw new ArgumentException($"Неизвестное имя формы: {formName}");
        }
    }
}
