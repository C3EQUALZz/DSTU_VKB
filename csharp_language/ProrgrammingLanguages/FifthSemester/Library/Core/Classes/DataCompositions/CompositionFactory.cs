using Library.Core.Classes.DataCompositions.Array;
using Library.Core.Classes.DataCompositions.String;
using Library.Core.Interfaces;

namespace Library.Core.Classes.DataCompositions;

public static class CompositionFactory
{
    public static IDataComposition<T> Create<T>()
    {
        return typeof(T) switch
        {
            var type when type == typeof(int[]) => (IDataComposition<T>) new IntArrayComposition(),
            var type when type == typeof(double[]) => (IDataComposition<T>) new DoubleArrayComposition(),
            var type when type == typeof(string[]) => (IDataComposition<T>) new StringArrayComposition(),
            var type when type == typeof(string) => (IDataComposition<T>) new StringComposition(),
            _ => throw new ArgumentException("Неподдерживаемый тип для обработки с консоли")
        };
    }
}