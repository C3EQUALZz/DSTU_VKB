namespace WinFormsAppForLaboratories.Laboratories.FirstLaboratory.SecondQuestion;

/// <summary>
/// Создайте приложение с двумя формами и установите вторую форму 
/// как стартовую.Сделайте так, чтобы при запуске стартовая форма разворачивалась
/// до максимальных размеров и содержала функциональность, дающую
/// возможность пользователю открыть первую форму, отображающуюся в виде
/// ромба зеленого цвета с кнопкой (в центре ромба) закрытия формы с надписью
/// GREENPEACE.Первая форма должна в тайтле выводить ФИО студента и группу
/// обучения.
/// </summary>
public partial class TaskForm : Form
{
    public TaskForm()
    {
        InitializeComponent();
    }

    private void SwapToSecondForm_Click(object sender, EventArgs e)
    {
        new SecondForm().Show();
        Hide();
    }
}


