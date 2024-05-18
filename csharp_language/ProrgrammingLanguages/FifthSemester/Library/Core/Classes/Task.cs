namespace Library.Core.Classes;

using Interfaces;

public class Task(ILabTask strategy)
{
    public string Execute()
    {
        return strategy.Execute();
    }
}