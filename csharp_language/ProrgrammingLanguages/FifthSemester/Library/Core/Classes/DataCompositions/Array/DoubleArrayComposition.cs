using Library.Core.Interfaces;

namespace Library.Core.Classes.DataCompositions.Array;

public class DoubleArrayComposition : BaseArrayComposition, IDataComposition<double[]>
{
    public new double[] Parse(string input)
    {
        return base.Parse(input).Select(s => double.Parse(s.Trim())).ToArray();
    }
}