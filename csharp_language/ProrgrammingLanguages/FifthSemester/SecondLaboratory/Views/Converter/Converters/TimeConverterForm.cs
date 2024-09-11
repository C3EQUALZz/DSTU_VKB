using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace SecondLaboratory.Views.Converter.Converters
{
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
}
