using WinFormsApp.Core.Enums;

namespace WinFormsApp.Core.Classes
{
    /// <summary>
    /// Класс, в котором хранятся коды HTML для цветовой палитры приложения. 
    /// Используется для смены цветовой темы в приложении. 
    /// </summary>
    public static class ColorMapCodes
    {
        public static Dictionary<ThemeColor, string> ColorCodes { get; } = new Dictionary<ThemeColor, string>
        {
            { ThemeColor.NightInManchester, "#3F51B5" },
            { ThemeColor.ApprovalGreen, "#009688" },
            { ThemeColor.SmashingPumpkins, "#FF5722" },
            { ThemeColor.WhaleShark, "#607D8B" },
            { ThemeColor.VitaminC, "#FF9800" },
            { ThemeColor.PinkSpyro, "#9C27B0" },
            { ThemeColor.KarimunBlue, "#2196F3" },
            { ThemeColor.PorcelainRose, "#EA676C" },
            { ThemeColor.SpanishCrimson, "#E41A4A" },
            { ThemeColor.BlueAndroidBase, "#5978BB" },
            { ThemeColor.OceanSoul, "#018790" },
            { ThemeColor.FirmamentBlue, "#0E3441" },
            { ThemeColor.Fiji, "#00B0AD" },
            { ThemeColor.CaviarCouture, "#721D47" },
            { ThemeColor.Cascara, "#EA4833" },
            { ThemeColor.AnimatedCoral, "#EF937E" },
            { ThemeColor.SunOrange, "#F37521" },
            { ThemeColor.CherriesJubilee, "#A12059" },
            { ThemeColor.BlueSapphire, "#126881" },
            { ThemeColor.HillLands, "#8BC240" },
            { ThemeColor.Odyssey, "#364D5B" },
            { ThemeColor.ChineseGreen, "#C7DC5B" },
            { ThemeColor.BlueDanube, "#0094BC" },
            { ThemeColor.PurpleYearning, "#E4126B" },
            { ThemeColor.MidoriGreen, "#43B76E" },
            { ThemeColor.MiddleBlue, "#7BCFE9" },
            { ThemeColor.Carmoisine, "#B71C46" }
        };
    }
}
