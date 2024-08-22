namespace FirstLaboratory.Core.Interfaces.ThirdQuestion
{
    internal interface IThirdQuestionView
    {
        MdiLayout MdiLayoutType { get; set; }
        void ExitMenuItem_Click(object sender, EventArgs e);
        void WindowCascadeMenuItem_Click(object sender, EventArgs e);
        void WindowTileMenuItem_Click(object sender, EventArgs e);
        void NewMenuItem_Click(object sender, EventArgs e);
    }
}
