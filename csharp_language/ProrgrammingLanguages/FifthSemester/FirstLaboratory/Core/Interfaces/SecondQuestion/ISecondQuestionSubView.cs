namespace FirstLaboratory.Core.Interfaces.SecondQuestion
{
    internal interface ISecondQuestionSubView
    {
        int Width { get; }
        int Height { get; }
        Color BackgroundColor { set; }
        void ExitButton_Click(object sender, EventArgs e);
        void SecondForm_Load(object sender, EventArgs e);
        void SetRegion(Region region);
    }
}
