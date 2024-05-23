using System.Runtime.InteropServices;

namespace WinFormsApp.Core.Classes.Utils;

public static class NativeMethods
{
    [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    public static extern void ReleaseCapture();

    [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    public static extern void SendMessage(nint hWnd, int msg, int wParam, int lParam);
}

