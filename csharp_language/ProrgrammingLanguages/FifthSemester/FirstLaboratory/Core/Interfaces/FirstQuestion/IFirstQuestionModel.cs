namespace FirstLaboratory.Core.Interfaces.FirstQuestion
{
    internal interface IFirstQuestionModel
    {
        Color BackgroundColor { get; set; }
        Pen BorderPen { get; set; }
        int Width { get; set; }
        int Height { get; set; }
    }
}
