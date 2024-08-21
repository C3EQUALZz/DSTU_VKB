using FirstLaboratory.Core.Interfaces.FirstQuestion;

namespace FirstLaboratory.Models
{
    /// <summary>
    /// Модель в паттерне MVP, здесь устанавливаются базовые параметры для отображения в View
    /// Грубо говоря, добавил настройки здесь, хотя можно и в View
    /// </summary>
    internal class FirstQuestionModel : IFirstQuestionModel
    {
        public Color BackgroundColor { get; set; } = Color.Red;
        public Pen BorderPen { get; set; } = new Pen(Color.Black, 3);
        public int Width { get; set; }
        public int Height { get; set; }
    }
}
