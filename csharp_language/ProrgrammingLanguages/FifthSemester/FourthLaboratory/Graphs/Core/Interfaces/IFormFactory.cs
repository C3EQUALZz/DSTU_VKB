using System.Windows.Forms;

namespace DoAnPaint.Graphs.Core.Interfaces
{
    internal interface IFormFactory
    {
        Form Create(string formName);
    }
}
