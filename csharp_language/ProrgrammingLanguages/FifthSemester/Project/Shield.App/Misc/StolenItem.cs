namespace Shield.App.Misc;
public class StolenItem
{
    public static readonly List<StolenItem> Items = [
            new("Арбуз", "Вроде спелый", 999999),
    ];

    public string Name;
    public string Meta;
    public double Price;

    private StolenItem(string name, string meta, double price)
    {
        Name = name;
        Meta = meta;
        Price = price;
    }
}
