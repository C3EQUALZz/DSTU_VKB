> [!NOTE] 
> Условие данной лабораторной описано в файле PDF <br>

Для переключения заданий нужно зайти в `Program.cs` и вписать в `Application.Run` одно из следующих:

- `FirstQuestionView`
- `SecondQuestionView`
- `ThirdQuestionView`

Пример вызова 2 задания:
```csharp
internal static class Program
{
    /// <summary>
    ///  The main entry point for the application.
    /// </summary>
    [STAThread]
    static void Main()
    {
        // To customize application configuration such as set high DPI settings or default font,
        // see https://aka.ms/applicationconfiguration.
        ApplicationConfiguration.Initialize();
        Application.Run(new SecondQuestionView());
    }
}
```

Здесь мне лень делать отдельную ещё форму для выбора задания))