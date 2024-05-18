namespace Library.Core.Interfaces;

public interface IDataComposition<T>
{
    T Parse(string input);
}