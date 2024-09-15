namespace Shield.DataAccess.Attributes;

[AttributeUsage(AttributeTargets.Field, Inherited = false, AllowMultiple = false)]
public class LocalizationTagAttribute : Attribute
{
    public string Tag
    {
        get;
    }

    public LocalizationTagAttribute(string tag)
    {
        Tag = tag;
    }
}
