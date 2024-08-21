using System.Drawing;
using System.Windows.Forms;

namespace ThirdLaboratory.core.classes
{
    public class RoundedPanel : Panel
    {
        protected override void OnPaint(PaintEventArgs e)
        {
            base.OnPaint(e);
            using (var path = new System.Drawing.Drawing2D.GraphicsPath())
            {
                int radius = 20; // Adjust the radius as needed
                path.AddArc(0, 0, radius, radius, 180, 90);
                path.AddArc(Width - radius, 0, radius, radius, 270, 90);
                path.AddArc(Width - radius, Height - radius, radius, radius, 0, 90);
                path.AddArc(0, Height - radius, radius, radius, 90, 90);
                path.CloseFigure();

                e.Graphics.SmoothingMode = System.Drawing.Drawing2D.SmoothingMode.AntiAlias;
                Region = new Region(path);

                // Fill the path with the background color
                e.Graphics.FillPath(new SolidBrush(BackColor), path);

                // Draw the border
                using (var pen = new Pen(Color.Black, 3)) // Adjust the width of the pen as needed
                {
                    e.Graphics.DrawPath(pen, path);
                }
            }
        }
    }
}
