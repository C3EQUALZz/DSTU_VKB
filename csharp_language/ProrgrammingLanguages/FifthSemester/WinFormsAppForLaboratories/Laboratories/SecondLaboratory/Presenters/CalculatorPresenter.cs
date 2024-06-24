using WinFormsAppForLaboratories.Laboratories.SecondLaboratory.Core.Interfaces;
using WinFormsAppForLaboratories.Laboratories.SecondLaboratory.Models;

namespace WinFormsAppForLaboratories.Laboratories.SecondLaboratory.Presenters;

public class CalculatorPresenter(ICalculatorView _view, CalculatorModel _model)
{
    public void OnNumberButtonClick(object sender, EventArgs e)
    {
        _view.EnterValue = false;
        var button = (Button)sender;

        if (_view.Display1Text == "0" || _view.EnterValue)
        {
            _view.Display1Text = string.Empty;
        }

        if ((button.Text == "." && !_view.Display1Text.Contains('.')) || button.Text != ".")
        {
            _view.Display1Text += button.Text;
        }
    }

    public void OnMathOperationButtonClick(object sender, EventArgs e)
    {
        if (_view.Result != 0)
        {
            OnEqualsButtonClick(sender, e);
        }
        else
        {
            _view.Result = double.Parse(_view.Display1Text);
        }

        var button = (Button) sender;
        _view.Operation = button.Text;
        _view.EnterValue = true;
        if (_view.Display1Text != "0")
        {
            _view.Display2Text = _view.FirstNumber = $"{_view.Result} {_view.Operation}";
            _view.Display1Text = string.Empty;
        }
    }

    public void OnEqualsButtonClick(object sender, EventArgs e)
    {
        _view.SecondNumber = _view.Display1Text;
        _view.Display2Text = $"{_view.Display2Text} {_view.Display1Text} = ";

        if (_view.Display1Text != string.Empty)
        {
            if (_view.Display1Text == "0")
                _view.Display2Text = string.Empty;

            double firstNumber = _view.Result;
            double secondNumber = double.Parse(_view.Display1Text);

            try
            {
                double result = _model.Evaluate(firstNumber, secondNumber, _view.Operation);
                _view.Display1Text = result.ToString();
                _view.AppendHistory($"{_view.FirstNumber} {_view.SecondNumber} = {result}\n");
                _view.Result = result;
            }

            catch (Exception)
            {
                _view.Display1Text = "Ошибка";
            }

            _view.Operation = string.Empty;
        }
    }

    public void OnHistoryButtonClick(object sender, EventArgs e)
    {
        _view.ToggleHistoryPanel();
    }

    public void OnClearHistoryButtonClick(object sender, EventArgs e)
    {
        _view.ClearHistory();
        _view.AppendHistory("История операций пуста");
    }

    public void OnBackSpaceButtonClick(object sender, EventArgs e)
    {
        if (_view.Display1Text.Length > 0)
        {
            _view.Display1Text = _view.Display1Text.Remove(_view.Display1Text.Length - 1, 1);
        }

        if (_view.Display1Text == string.Empty)
        {
            _view.Display1Text = "0";
        }
    }

    public void OnClearButtonClick(object sender, EventArgs e)
    {
        _view.Display1Text = "0";
        _view.Display2Text = string.Empty;
        _view.Result = 0;
    }

    public void OnClearEntryButtonClick(object sender, EventArgs e)
    {
        _view.Display1Text = "0";
    }

    public void OnOperationButtonClick(object sender, EventArgs e)
    {
        var button = (Button) sender;
        _view.Operation = button.Text;
        double number = double.Parse(_view.Display1Text);

        try
        {
            _view.Display1Text = _model.Evaluate(number, _view.Operation).ToString();
            _view.Display2Text = $"{_view.Operation}({_view.Display1Text})";
            _view.AppendHistory($"{_view.Display2Text} = {_view.Display1Text}\n");
        }
        catch (Exception)
        {
            _view.Display1Text = "Error";
        }
    }

    public void OnExitButtonClick(object sender, EventArgs e)
    {
        Application.Exit();
    }
}
