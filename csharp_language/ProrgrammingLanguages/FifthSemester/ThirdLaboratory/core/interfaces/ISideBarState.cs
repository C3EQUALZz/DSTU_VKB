using ThirdLaboratory.core.helpers;

namespace ThirdLaboratory.core.interfaces
{
    /// <summary>
    /// Интерфейс, который нужен для реализация паттерна "Состояние"
    /// </summary>
    internal interface ISideBarState
    {
        /// <summary>
        /// Метод, который будет обрабатывать смену состояния
        /// </summary>
        /// <param name="context">контекст для смены состояния</param>
        void Handle(SideBarContext context);
    }
}
