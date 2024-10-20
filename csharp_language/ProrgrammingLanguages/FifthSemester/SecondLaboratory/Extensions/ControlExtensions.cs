using System.Drawing;
using System.Windows.Forms;

namespace SecondLaboratory.Extensions;
public static class ControlExtensions
{
    public static void SetRoundedShape(this Control control, int radius)
    {
        System.Drawing.Drawing2D.GraphicsPath path = new System.Drawing.Drawing2D.GraphicsPath();
        path.AddLine(radius, 0, control.Width - radius, 0);
        path.AddArc(control.Width - radius, 0, radius, radius, 270, 90);
        path.AddLine(control.Width, radius, control.Width, control.Height - radius);
        path.AddArc(control.Width - radius, control.Height - radius, radius, radius, 0, 90);
        path.AddLine(control.Width - radius, control.Height, radius, control.Height);
        path.AddArc(0, control.Height - radius, radius, radius, 90, 90);
        path.AddLine(0, control.Height - radius, 0, radius);
        path.AddArc(0, 0, radius, radius, 180, 90);
        control.Region = new Region(path);
    }

    public static void SetRoundedShape(this Control control, int r1, int r2, int r3, int r4)
    {
        System.Drawing.Drawing2D.GraphicsPath path = new System.Drawing.Drawing2D.GraphicsPath();
        path.AddLine(r1, 0, control.Width - r1, 0);
        path.AddArc(control.Width - r1, 0, r1, r1, 270, 90);
        path.AddLine(control.Width, r2, control.Width, control.Height - r2);
        path.AddArc(control.Width - r2, control.Height - r2, r2, r2, 0, 90);
        path.AddLine(control.Width - r3, control.Height, r3, control.Height);
        path.AddArc(0, control.Height - r3, r3, r3, 90, 90);
        path.AddLine(0, control.Height - r4, 0, r4);
        path.AddArc(0, 0, r4, r4, 180, 90);
        control.Region = new Region(path);
    }

    public static void SetRoundedShape(this Panel panel, int radius)
    {
        System.Drawing.Drawing2D.GraphicsPath path = new System.Drawing.Drawing2D.GraphicsPath();
        path.AddLine(radius, 0, panel.Width - radius, 0);
        path.AddArc(panel.Width - radius, 0, radius, radius, 270, 90);
        path.AddLine(panel.Width, radius, panel.Width, panel.Height - radius);
        path.AddArc(panel.Width - radius, panel.Height - radius, radius, radius, 0, 90);
        path.AddLine(panel.Width - radius, panel.Height, radius, panel.Height);
        path.AddArc(0, panel.Height - radius, radius, radius, 90, 90);
        path.AddLine(0, panel.Height - radius, 0, radius);
        path.AddArc(0, 0, radius, radius, 180, 90);
        panel.Region = new Region(path);
    }

    public static void SetRoundedShape(this Panel panel, int r1, int r2, int r3, int r4)
    {
        System.Drawing.Drawing2D.GraphicsPath path = new System.Drawing.Drawing2D.GraphicsPath();
        path.AddLine(r1, 0, panel.Width - r1, 0);
        path.AddArc(panel.Width - r1, 0, r1, r1, 270, 90);
        path.AddLine(panel.Width, r2, panel.Width, panel.Height - r2);
        path.AddArc(panel.Width - r2, panel.Height - r2, r2, r2, 0, 90);
        path.AddLine(panel.Width - r3, panel.Height, r3, panel.Height);
        path.AddArc(0, panel.Height - r3, r3, r3, 90, 90);
        path.AddLine(0, panel.Height - r4, 0, r4);
        path.AddArc(0, 0, r4, r4, 180, 90);
        panel.Region = new Region(path);
    }
}
