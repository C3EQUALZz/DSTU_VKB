namespace WinFormsAppForLaboratories.Laboratories.SecondLaboratory.Core.Interfaces;

public interface ICalculatorView
{
    string Display1Text { get; set; }
    string Display2Text { get; set; }
    bool EnterValue { get; set; }
    string? Operation { get; set; }
    string? FirstNumber { get; set; }
    string? SecondNumber { get; set; }
    double Result { get; set; }

    void AppendHistory(string text);
    void ClearHistory();
    void ToggleHistoryPanel();
}


