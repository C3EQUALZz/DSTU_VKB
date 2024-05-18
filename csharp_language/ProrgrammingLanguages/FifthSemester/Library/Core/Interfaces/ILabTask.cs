namespace Library.Core.Interfaces;

/**
 * Реализован паттерн стратегия, так как каждый класс - задание.
 * Каждое задание лабораторных похожи друг на друга по общему признаку, но отличаются по алгоритму.
 */
public interface ILabTask
{
    string Execute();
}