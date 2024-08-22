namespace FirstLaboratory.Core.Interfaces.FirstQuestion
{
    internal interface IFirstQuestionView
    {
        int Width { get; }
        int Height { get; }
        Region Region { set; }

        Color BackgroundColor { set; }
        void DrawEllipse(Graphics g, Pen borderPen, int width, int height);
        void ResizeEvent(object sender, EventArgs e);
        void PaintEvent(object sender, EventArgs e);
        void ExitButton_Click(object sender, EventArgs e);
        Graphics CreateGraphics();
    }
}
