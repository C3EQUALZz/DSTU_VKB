using System.Drawing.Drawing2D;

namespace WinFormsAppForLaboratories.Laboratories.SecondLaboratory.Core.Classes;

/// <summary>
/// https://youtu.be/vxc5GopCOMQ?si=lIf4HjTm0DQOK1kU
/// </summary>
public class CustomButton : Button
{
    private int borderSize = 0;
    private int borderRadius = 50;
    private Color borderColor = Color.Transparent;

    public int BorderSize
    {
        get => borderSize;
        set { borderSize = value; Invalidate();  }
    }

    public int BorderRadius
    {
        get => borderRadius;
        set { borderRadius = (value <= Height) ? value : Height; Invalidate(); }
    }

    public Color BackGroundColor
    {
        get => BackColor;
        set { BackColor = value; }
    }

    public Color TextColor
    {
        get => ForeColor;
        set { ForeColor = value; }
    }

    public CustomButton()
    {
        Size = new Size(200, 100);
        FlatAppearance.BorderSize = 0;
        FlatStyle = FlatStyle.Flat;
        BackColor = Color.DodgerBlue;
        ForeColor = Color.White;
        Resize += (sender, e) => borderRadius = borderRadius > Height ? Height : borderRadius;
    }


    private static GraphicsPath GetFigurePath(RectangleF rectangle, float radius)
    {
        var graphicsPath = new GraphicsPath();
        graphicsPath.StartFigure();

        // Массив координат и углов
        PointF[] points = [
        new(rectangle.X, rectangle.Y),
        new(rectangle.Right - radius, rectangle.Y),
        new(rectangle.Right - radius, rectangle.Bottom - radius),
        new(rectangle.X, rectangle.Bottom - radius)
        ];

        float[] startAngles = [ 180, 270, 0, 90 ];

        // Добавляем дуги
        for (int i = 0; i < points.Length; i++)
        {
            graphicsPath.AddArc(points[i].X, points[i].Y, radius, radius, startAngles[i], 90);
        }

        graphicsPath.CloseFigure();

        return graphicsPath;
    }

    protected override void OnPaint(PaintEventArgs e)
    {
        base.OnPaint(e);
        e.Graphics.SmoothingMode = SmoothingMode.AntiAlias;

        var rectangleSurface = new RectangleF(0, 0, Width, Height);
        var rectangleBorder = new RectangleF(1, 1, Width - 0.5F, Height - 1);

        if (borderRadius > 1 && Parent != null)
        {
            using var graphicsPathSurface = GetFigurePath(rectangleSurface, borderRadius);
            using var graphicsPathBorder = GetFigurePath(rectangleBorder, borderRadius - 1F);
            using var penSurface = new Pen(Parent.BackColor, 2);
            using var penBorder = new Pen(borderColor, borderSize);
            penBorder.Alignment = PenAlignment.Inset;
            Region = new Region(graphicsPathSurface);
            e.Graphics.DrawPath(penBorder, graphicsPathSurface);

            if (borderSize >= 1)
            {
                e.Graphics.DrawPath(penBorder, graphicsPathBorder);
            }
        }

        else
        {
            Region = new Region(rectangleSurface);

            if (borderSize >= 1)
            {
                using var penBorder = new Pen(borderColor, borderSize);
                penBorder.Alignment = PenAlignment.Inset;
                e.Graphics.DrawRectangle(penBorder, 0, 0, Width - 1, Height - 1);
            }

        }
    }

    protected override void OnHandleCreated(EventArgs e)
    {
        base.OnHandleCreated(e);

        if (Parent != null)
        {
            Parent.BackColorChanged += (sender, args) =>
            {
                if (DesignMode) Invalidate();
            };
        }
    }

}
