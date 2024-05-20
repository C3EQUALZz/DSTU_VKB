using Library.Core.Classes.DataCompositions;
using Library.Core.Interfaces;

namespace Library.Laboratories.FirstLaboratory.FirstTask;

public class Main : ILabTask
{
    private readonly string _parsedData;
    
    public Main(string input) => _parsedData = CompositionFactory.Create<string>().Parse(input);
    public string Execute()
    {
        return $"Результат задания {_parsedData}";
    }
    
}