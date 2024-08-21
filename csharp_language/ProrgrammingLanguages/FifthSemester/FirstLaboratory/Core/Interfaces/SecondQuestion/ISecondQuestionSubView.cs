namespace FirstLaboratory.Core.Interfaces.SecondQuestion
{
    internal interface ISecondQuestionSubView
    {
        int Width { get; }
        int Height { get; }
        Region Region { get; set; }
        Color BackgroundColor { set; }
    }
}
