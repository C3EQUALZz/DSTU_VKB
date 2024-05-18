using Library.Core.Classes.DataCompositions;
using Library.Core.Interfaces;

namespace Library.FirstLaboratory;

public class FirstTask : ILabTask
{
    private readonly string _parsedData;
    
    public FirstTask(string input) => _parsedData = CompositionFactory.Create<string>().Parse(input);
    public string Execute()
    {
        return $"Результат задания {_parsedData}";
    }
    
}