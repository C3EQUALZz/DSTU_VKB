using Library.Core.Interfaces;

namespace Library.Core.Classes.DataCompositions.Array;

public class StringArrayComposition : BaseArrayComposition, IDataComposition<string[]>
{
    public new string[] Parse(string input)
    {
        return base.Parse(input).Select(s => s.Trim()).ToArray();
    }
}