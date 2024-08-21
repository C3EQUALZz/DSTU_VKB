using System.Windows.Forms;

namespace ThirdLaboratory.core.interfaces
{
    internal interface IFormFactory
    {
        Form Create(string formName);
    }
}
