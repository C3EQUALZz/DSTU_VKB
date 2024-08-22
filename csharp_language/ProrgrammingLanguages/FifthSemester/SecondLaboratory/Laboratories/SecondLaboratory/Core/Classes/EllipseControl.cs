namespace WinFormsAppForLaboratories.Laboratories.SecondLaboratory.Core.Classes;

using System.ComponentModel;
using System.Runtime.InteropServices;

/// <summary>
/// https://youtu.be/kOEPiuHkJkM?si=V9Z3LsgyN8INsCee
/// </summary>
public class EllipseControl : Component
{
    [DllImport("Gdi32.dll", EntryPoint = "CreateRoundRectRgn")]
    private static extern IntPtr CreateRoundRectRgn(int nL, int nT, int nR, int nB, int nWidthEllipse, int nHeigthEllipse);

    private Control? control;
    private int cornerRadius = 25;
    public Control? TargetControl
    {
        get { return control; }
        set
        {
            control = value;
            if (control != null)
                control.SizeChanged += (sender, eventArgs) => control.Region = Region.FromHrgn(CreateRoundRectRgn(0, 0, control.Width, control.Height, cornerRadius, cornerRadius));
        }
    }

    public int CornerRadius
    { 
        get { return cornerRadius; }
        set
        {
            cornerRadius = value;
            if (control != null)
            {
                control.Region = Region.FromHrgn(CreateRoundRectRgn(0, 0, control.Width, control.Height, cornerRadius, cornerRadius));
            }
        } 
    }

}
