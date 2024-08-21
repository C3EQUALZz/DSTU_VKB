using FirstLaboratory.Core.Interfaces.FirstQuestion;

namespace FirstLaboratory.Models
{
    internal class FirstQuestionModel : IFirstQuestionModel
    {
        public Color BackgroundColor { get; set; } = Color.Red;
        public Pen BorderPen { get; set; } = new Pen(Color.Black, 3);
        public int Width { get; set; }
        public int Height { get; set; }
    }
}
