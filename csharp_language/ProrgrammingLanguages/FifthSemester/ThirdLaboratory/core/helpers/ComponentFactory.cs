using System;
using System.Linq;
using System.Reflection;
using System.Windows.Forms;

namespace ThirdLaboratory.core.helpers
{
    internal class ComponentFactory
    {
        public static Panel FindPanelByTag(Control parent, string panelTag)
        {
            var panel = parent
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

        public static Timer FindTimerByTag(Form form, string panelTag)
        {
            var componentsField = form.GetType().GetField("components", BindingFlags.NonPublic | BindingFlags.Instance);

            if (componentsField is null)
            {
                throw new ArgumentNullException("Не были найдены компоненты (часы и т.п), проверьте Designer");
            }
                
            var components = componentsField.GetValue(form) as System.ComponentModel.Container;

            var timer = components?.Components.OfType<Timer>().FirstOrDefault(t => t.Tag?.ToString() == panelTag);

            if (timer is null)
            {
                throw new ArgumentNullException("Не был найден таймер, проверьте Designer");
            }
                
            return timer;
        }
    }
}
