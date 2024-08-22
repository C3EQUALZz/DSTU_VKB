using System.Drawing.Drawing2D;
using FirstLaboratory.Core.Interfaces.SecondQuestion;

namespace FirstLaboratory.Models
{
    /// <summary>
    /// Модель, которая рисует нам окно в форме ромба
    /// </summary>
    internal class SecondQuestionModel : ISecondQuestionModel
    {
        /// <summary>
        /// Здесь создается путь отображения с помощью 4 точек, нагло украл код с stackoverflow. 
        /// </summary>
        public GraphicsPath CreateDiamondPath(int width, int height)
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
