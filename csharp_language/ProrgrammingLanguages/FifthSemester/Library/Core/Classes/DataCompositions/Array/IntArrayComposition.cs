using Library.Core.Interfaces;

namespace Library.Core.Classes.DataCompositions.Array;

using System.Linq;

public class IntArrayComposition : BaseArrayComposition, IDataComposition<int[]>
{
    public new int[] Parse(string input)
    {
        return base.Parse(input).Select(s => int.Parse(s.Trim())).ToArray();
    }
}