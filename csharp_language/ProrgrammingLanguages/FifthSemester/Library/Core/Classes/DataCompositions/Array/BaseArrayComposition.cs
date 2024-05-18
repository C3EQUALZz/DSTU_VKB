using Library.Core.Interfaces;

namespace Library.Core.Classes.DataCompositions.Array;

public abstract class BaseArrayComposition : IDataComposition<string[]>
{
    public string[] Parse(string input)
    {
        input = input.Trim('[', ']');
        return input.Split(',');
    }   
}