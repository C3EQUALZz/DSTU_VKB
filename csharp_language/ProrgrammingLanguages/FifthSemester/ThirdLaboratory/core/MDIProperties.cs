using System;
using System.Runtime.InteropServices;
using System.Windows.Forms;

namespace ThirdLaboratory.core
{   
    /// <summary>
    /// ВЗЯТО ПОЛНОСТЬЮ С ОБЗОРА, Я ВООБЩЕ ХЗ
    /// </summary>
    public static class MDIProperties
    {
        [DllImport("user32.dll")]
        private static extern int GetWindowLong(IntPtr hWnd, int nIndex);

        [DllImport("user32.dll")]
        private static extern int SetWindowLong(IntPtr hWnd, int nIndex, int dwNewLong);

        [DllImport("user32.dll")]
        private static extern int SetWindowPos(
            IntPtr hWnd,
            IntPtr hWndInsertAfter,
            int X,
            int Y,
            int cx,
            int cy,
            uint uFlags
        );

        
        // Я сам не понимаю что за цифры в 16СС, если что. 
        private const int GWL_EXSTYLE = -20;
        private const int WS_EX_CLIENTEDGE = 0x200;
        private const uint SWP_NOSIZE = 0x0001;
        private const uint SWP_NOMOVE = 0x0002;
        private const uint SWP_NOZORDER = 0x0004;
        private const uint SWO_NOACTIVATE = 0x0010;
        private const uint SWP_FRAMECHANGED = 0x0020;
        private const uint SWO_NOOWNERZORDER = 0x0200;

        public static bool SetBevel(this Form form, bool show)
        {
            foreach(Control control  in form.Controls)
            {
                var client = control as MdiClient;

                if (client != null)
                {
                    var windowLong = GetWindowLong(control.Handle, GWL_EXSTYLE);

                    if (show)
                    {
                        windowLong |= WS_EX_CLIENTEDGE;
                    }

                    else
                    {
                        windowLong &= WS_EX_CLIENTEDGE;
                    }
                    SetWindowLong(control.Handle, GWL_EXSTYLE, windowLong);
                    SetWindowPos(client.Handle, IntPtr.Zero, 0, 0, 0, 0,
                        SWO_NOACTIVATE | SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | 
                        SWO_NOOWNERZORDER | SWP_FRAMECHANGED
                    );
                    return true;
                }
                     
            }

            return false;
        }
    }
}
