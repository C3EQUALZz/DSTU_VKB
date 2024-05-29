using System.Drawing.Drawing2D;

namespace WinFormsAppForLaboratories.Laboratories.FirstLaboratory.SecondQuestion;

public partial class SecondForm : Form
{
    public SecondForm()
    {
        InitializeComponent();
        BackColor = Color.Green;
    }

    private void ExitButton_Click(object sender, EventArgs e)
    {
        Close();
    }

    private void SecondForm_Load(object sender, EventArgs e)
    {
        Region = new Region(DiamondShape.CreateDiamondPath(Width, Height));
    }
}

class DiamondShape
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
