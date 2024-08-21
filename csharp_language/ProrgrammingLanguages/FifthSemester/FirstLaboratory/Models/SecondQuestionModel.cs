using System.Drawing.Drawing2D;

namespace FirstLaboratory.Models
{
    internal class SecondQuestionModel
    {
        public static GraphicsPath CreateDiamondPath(int width, int height)
        {
            var path = new GraphicsPath();
            path.AddLines(new[]
            {
            new Point(0, height / 2),
            new Point(width / 2, 0),
            new Point(width, height / 2),
            new Point(width / 2, height)
        });
            path.CloseFigure();

            return path;
        }
    }
}
