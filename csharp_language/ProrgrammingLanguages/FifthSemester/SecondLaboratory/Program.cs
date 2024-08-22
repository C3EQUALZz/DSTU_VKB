namespace WinFormsAppForLaboratories
{
    internal static class Program
    {
        [STAThread]
        static void Main()
        {
            ApplicationConfiguration.Initialize();
            Application.Run(new Laboratories.SecondLaboratory.Views.CalculatorView());
        }
    }
}