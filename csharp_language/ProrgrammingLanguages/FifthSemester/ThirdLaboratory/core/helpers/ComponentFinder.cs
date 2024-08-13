using System;
using System.Linq;
using System.Reflection;
using System.Windows.Forms;

namespace ThirdLaboratory.core.helpers
{
    /// <summary>
    /// Реализован паттерн стратегия для замены Control, где дальше будет производится поиск. 
    /// Данный класс позволяет искать на форме, да вообще где угодно элемент с определенным Tag
    /// </summary>
    internal class ComponentFinder
    {

        private Control _control;

        public ComponentFinder(Control control)
        {
            _control = control;
        }

        /// <summary>
        /// Свойство, которое как раз и позволяет делать замену в Runtime для реализации паттерна стратегия
        /// </summary>
        public Control Control
        {
            set { _control = value; }
            get { return _control; }
        }


        /// <summary>
        /// Поиск элемента по тегу 
        /// </summary>
        /// <param name="panelTag">тэг панели, которую мы хотим найти</param>
        /// <returns>возвращает сам объект панели</returns>
        public Panel FindPanelByTag(string panelTag)
        {
            var panel = Control
                .Controls
                .Find(panelTag, true)
                .OfType<Panel>()
                .FirstOrDefault(p => p.Tag?.ToString() == panelTag);

            if (panel is null)
            {
                throw new ArgumentNullException("Панель с указанным тегом не найдена.");
            }

            return panel;
        }

        /// <summary>
        /// Поиск таймера по тегу
        /// </summary>
        /// <param name="panelTag">тэг таймера, который должен быть у него</param>
        /// <returns>возвращает сам объект таймера из формы</returns>
        /// <exception cref="ArgumentNullException">возвращается в случае того, если не нашел</exception>
        public Timer FindTimerByTag(string panelTag)
        {
            var componentsField = Control.GetType().GetField("components", BindingFlags.NonPublic | BindingFlags.Instance);

            if (componentsField is null)
            {
                throw new ArgumentNullException("Не были найдены компоненты (часы и т.п), проверьте Designer");
            }
                
            var components = componentsField.GetValue(Control) as System.ComponentModel.Container;

            var timer = components?.Components.OfType<Timer>().FirstOrDefault(t => t.Tag?.ToString() == panelTag);

            if (timer is null)
            {
                throw new ArgumentNullException("Не был найден таймер, проверьте Designer");
            }
                
            return timer;
        }
    }
}
