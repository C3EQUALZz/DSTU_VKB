using System.Reflection;

namespace Shield.DataAccess.Extensions;
public static class EnumExtensions
{
    public static T? GetAttribute<T>(this Enum value) where T : Attribute
    {
        var type = value.GetType();

        var memberInfo = type.GetMember(value.ToString());

        if (memberInfo.Length > 0)
        {
            var attribute = memberInfo[0].GetCustomAttribute<T>();

            if (attribute != null)
            {
                return attribute;
            }
        }

        return null;
    }
}
