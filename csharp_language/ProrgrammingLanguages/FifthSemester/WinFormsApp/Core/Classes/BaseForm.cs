using System.Runtime.InteropServices;

namespace WinFormsApp.Core.Classes;

public class BaseForm : Form
{
    private readonly int borderSize = 2;
    protected Size formSize;

    public BaseForm()
    {
        Padding = new Padding(borderSize);
        BackColor = Color.FromArgb(39, 39, 58);
    }

    [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    private extern static void ReleaseCapture();


    [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    private extern static void SendMessage(IntPtr hWnd, int wMsg, int wParam, int lParam);

    protected void panelTitleBar_MouseDown(object sender, MouseEventArgs e)
    {
        ReleaseCapture();
        SendMessage(Handle, 0x112, 0xf012, 0);
    }

    protected override void WndProc(ref Message m)
    {
        const int WM_NCCALCSIZE = 0x0083;
        const int WM_SYSCOMMAND = 0x0112;
        const int SC_MINIMIZE = 0xF020;
        const int SC_RESTORE = 0xF120;
        const int WM_NCHITTEST = 0x0084;
        const int resizeAreaSize = 10;

        #region Form Resize
        const int HTCLIENT = 1;
        const int HTLEFT = 10;
        const int HTRIGHT = 11;
        const int HTTOP = 12;
        const int HTTOPLEFT = 13;
        const int HTTOPRIGHT = 14;
        const int HTBOTTOM = 15;
        const int HTBOTTOMLEFT = 16;
        const int HTBOTTOMRIGHT = 17;

        if (m.Msg == WM_NCHITTEST)
        {
            base.WndProc(ref m);
            if (WindowState == FormWindowState.Normal)
            {
                if ((int)m.Result == HTCLIENT)
                {
                    Point screenPoint = new(m.LParam.ToInt32());
                    Point clientPoint = PointToClient(screenPoint);

                    if (clientPoint.Y <= resizeAreaSize)
                    {
                        if (clientPoint.X <= resizeAreaSize)
                            m.Result = (IntPtr)HTTOPLEFT;
                        else if (clientPoint.X < (Size.Width - resizeAreaSize))
                            m.Result = (IntPtr)HTTOP;
                        else
                            m.Result = (IntPtr)HTTOPRIGHT;
                    }
                    else if (clientPoint.Y <= (Size.Height - resizeAreaSize))
                    {
                        if (clientPoint.X <= resizeAreaSize)
                            m.Result = (IntPtr)HTLEFT;
                        else if (clientPoint.X > (Width - resizeAreaSize))
                            m.Result = (IntPtr)HTRIGHT;
                    }
                    else
                    {
                        if (clientPoint.X <= resizeAreaSize)
                            m.Result = (IntPtr)HTBOTTOMLEFT;
                        else if (clientPoint.X < (Size.Width - resizeAreaSize))
                            m.Result = (IntPtr)HTBOTTOM;
                        else
                            m.Result = (IntPtr)HTBOTTOMRIGHT;
                    }
                }
            }
            return;
        }
        #endregion

        if (m.Msg == WM_NCCALCSIZE && m.WParam.ToInt32() == 1)
        {
            return;
        }

        if (m.Msg == WM_SYSCOMMAND)
        {
            int wParam = (m.WParam.ToInt32() & 0xFFF0);

            if (wParam == SC_MINIMIZE)
                formSize = ClientSize;
            if (wParam == SC_RESTORE)
                Size = formSize;
        }
        base.WndProc(ref m);
    }

    protected void FormResizeEvent(object sender, EventArgs e)
    {
        switch (WindowState)
        {
            case FormWindowState.Maximized:
                Padding = new Padding(8, 8, 8, 0);
                break;
            case FormWindowState.Normal:
                if (Padding.Top != borderSize)
                    Padding = new Padding(borderSize);
                formSize = ClientSize;  // Обновление размера формы
                break;
        }
    }



}
