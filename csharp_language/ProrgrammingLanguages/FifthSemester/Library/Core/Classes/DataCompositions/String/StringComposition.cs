using Library.Core.Interfaces;

namespace Library.Core.Classes.DataCompositions.String;

public class StringComposition : IDataComposition<string>
{
    public string Parse(string input)
    {
        return input.Trim();
    }
    
}