using System.Windows.Forms;

namespace ThirdLaboratory.core.helpers.questions
{
    internal static class Handlers
    {
        public static void HandleTextChanged(string text, ref int? value)
        {
            if (string.IsNullOrEmpty(text))
                return;

            if (int.TryParse(text, out var buffer))
            {
                value = buffer;
            }
            else
            {
                MessageBox.Show("Вы ввели не целое число");
            }
        }
    }
}
