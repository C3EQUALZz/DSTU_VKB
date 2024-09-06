> [!NOTE]
> Условие данной лабораторной описано в файле PDF <br>

Здесь реализованы не все 20 заданий по графикам, а только до 10. 
Если нет вашего варианта, то проделайте следующий алгоритм:

- В папке `Graphs/Models` создайте директорию с вашими будущими моделями
- Создайте 3 класса `FirstModel`, `SecondModel`, `ThirdModel` (NOTE: в задании просится по 3 функции придумать)
- Классы обязательно должны имплементировать `IModel` из папки `Graphs/Core/Interfaces`
- После этого откройте код в `Form<номер_вашего_задания>Question` (не Designer!!!) 
- Впишите код, как в примере ниже

Например, код View (Form) будет выглядеть следующим образом для 17 задания:

```csharp
using DoAnPaint.Graphs.Core.Abstract;
using DoAnPaint.Graphs.Core.Interfaces;
using System.Collections.Generic;
using DoAnPaint.Graphs.Models.SeventeenthQuestion;

namespace DoAnPaint.Graphs.Views
{
    public partial class FormFifthQuestion : BaseForm
    {
        public FormSeventeenthQuestion()
        {
            InitializeComponent();
            InitializeModels(new List<IModel> { new FirstModel(), new SecondModel(), new ThirdModel() });
        }
    }
}
```

---

Каждый новый View (Form) в Designer нужно оформлять также, как у меня в прошлых заданиях. 
Обязательно должны быть такие же имена (Name у элементов Form), в ином случае все автоматически не добавится для работы. 

Имена, которые обязательно должны быть присвоены: 

- cartesianChart (график сам)
- graphStartTextBox (TextBox, а не Label ес чо)
- graphEndTextBox (TextBox опять-таки)
- graphStepTextBox (TextBox)
- animationCheckBox
- firstChartCheckBox
- secondChartCheckBox
- thirdChartCheckBox

Все они представлены на риснуке ниже

![Пример задания](https://github.com/user-attachments/assets/444527b4-8837-4cd4-9463-dac0427ffda2)

---

Paint я украл и адаптировал, переделав там немногое. Простите за говнокод там

---

Здесь я прилагаю фото, как я все реализовал

![Paint](https://github.com/user-attachments/assets/91b86eb1-dae0-494a-a5f6-320978436715)

![Graphics](https://github.com/user-attachments/assets/7a2970aa-3a1b-4f0a-bc4f-4d3311259eff)


