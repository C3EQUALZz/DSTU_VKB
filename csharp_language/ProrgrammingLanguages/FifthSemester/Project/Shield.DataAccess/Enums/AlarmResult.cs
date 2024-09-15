using Shield.DataAccess.Attributes;

namespace Shield.DataAccess.Enums;
public enum AlarmResult
{
    [LocalizationTag("Ложная тревога")]
    False,

    [LocalizationTag("Кража")]
    Robbery
}
