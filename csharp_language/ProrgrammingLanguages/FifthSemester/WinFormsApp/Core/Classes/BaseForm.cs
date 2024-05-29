using WinFormsApp.Core.Classes.Utils;
using WinFormsApp.Core.Enums.Form;
using WinFormsApp.Core.Interfaces;

namespace WinFormsApp.Core.Classes;

enum BorderConstants
{
    BorderSize = 2,
    ResizeAreaSize = 10
}

public class BaseForm : Form
{
    protected Size formSizeBeforeMinimize;

    public BaseForm()
    {
        Padding = new Padding((int)BorderConstants.BorderSize);
        BackColor = Color.FromArgb(39, 39, 58);
        Resize += FormResizeEvent;
    }

    protected void PanelTitleBar_MouseDown(object sender, MouseEventArgs e)
    {
        NativeMethods.ReleaseCapture();
        NativeMethods.SendMessage(Handle, 0x112, 0xf012, 0);
    }

    protected override void WndProc(ref Message m)
    {
        switch (m.Msg)
        {
            case (int)MessageConstants.WM_NCCALCSIZE:
                if (m.WParam.ToInt32() == 1)
                    return;
                break;

            case (int)MessageConstants.WM_SYSCOMMAND:
                HandleSysCommand(m);
                break;

            case (int)MessageConstants.WM_NCHITTEST:
                HandleNCHitTest(ref m, (int)BorderConstants.ResizeAreaSize);
                break;
        }

        base.WndProc(ref m);
    }

    protected void FormResizeEvent(object? sender, EventArgs e)
    {
        switch (WindowState)
        {
            case FormWindowState.Maximized:
                Padding = new Padding(8, 8, 8, 0);
                break;
            case FormWindowState.Normal:
                if (Padding.Top != (int)BorderConstants.BorderSize)
                    Padding = new Padding((int)BorderConstants.BorderSize);
                formSizeBeforeMinimize = ClientSize;
                break;
        }
    }

    private void HandleSysCommand(Message m)
    {
        var wParam = (m.WParam.ToInt32() & 0xFFF0);
        if (wParam == (int)SysCommandConstants.SC_MINIMIZE)
        {
            formSizeBeforeMinimize = ClientSize;
        }
        else if (wParam == (int)SysCommandConstants.SC_RESTORE)
        {
            ClientSize = formSizeBeforeMinimize;
        }
    }

    private void HandleNCHitTest(ref Message m, int resizeAreaSize)
    {
        base.WndProc(ref m);

        if (WindowState == FormWindowState.Normal && (int)m.Result == (int)HitTestConstants.HTCLIENT)
        {
            Point screenPoint = new(m.LParam.ToInt32());
            Point clientPoint = PointToClient(screenPoint);

            m.Result = GetHitTestResult(clientPoint, resizeAreaSize);
        }
    }

    private IntPtr GetHitTestResult(Point clientPoint, int resizeAreaSize)
    {
        foreach (HitTestConstants hitTestConstant in Enum.GetValues(typeof(HitTestConstants)))
        {

            IHitTestStrategy strategy = HitTestStrategyFactory.GetStrategy(hitTestConstant);

            IntPtr result = strategy.GetHitTestResult(clientPoint, Size, resizeAreaSize);

            if (result != IntPtr.Zero)
            {
                return result;
            }
        }

        return (IntPtr)HitTestConstants.HTCLIENT;
    }

}
