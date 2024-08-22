namespace FirstLaboratory.Core.Interfaces.ThirdQuestion
{
    internal interface IThirdQuestionSubView
    {
        void ToggleMenuItem_Click(object sender, EventArgs e);
        Color ChildTextBoxForeColor { get; set; }
        bool ToggleMenuItemChecked { get; set; }
    }
}
