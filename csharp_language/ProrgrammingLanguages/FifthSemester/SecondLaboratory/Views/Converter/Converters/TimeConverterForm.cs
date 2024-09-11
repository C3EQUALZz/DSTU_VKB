namespace SecondLaboratory.Views.Converter.Converters;
public partial class TimeConverterForm : SecondLaboratory.Views.Converter.ConverterBaseForm
{
    private int minsInYear = 525_600;

    public TimeConverterForm()
    {
        InitializeComponent();

        LTitle = "Год";
        RTitle = "Минута";

        LeftConverter = x => x * minsInYear;
        RightConverter = x => x / minsInYear;
    }
}
