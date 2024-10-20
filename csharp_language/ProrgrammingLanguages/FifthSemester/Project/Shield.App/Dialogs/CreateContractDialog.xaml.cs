using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Reflection;
using System.Runtime.CompilerServices;
using Microsoft.UI;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Media;
using Shield.App.Controls;
using Shield.App.Helpers;
using Shield.DataAccess.DTOs;
using Windows.Storage;
using Microsoft.Web.WebView2.Core;

namespace Shield.App.Dialogs;
public sealed partial class CreateContractDialog : UserControl, INotifyPropertyChanged
{
    private string _planPath = string.Empty;
    public string PlanPath
    {
        get => _planPath;
        set
        {
            if (value != _planPath)
            {
                _planPath = value;
                NotifyPropertyChanged();
            }
        }
    }

    private string _photoPath = string.Empty;
    public string PhotoPath
    {
        get => _photoPath;
        set
        {
            if (value != _photoPath)
            {
                _photoPath = value;
                NotifyPropertyChanged();
            }
        }
    }

    public string Bailee => BaileeTB.Text;
    public string Address => AddressTB.Text;
    public string Comment => CommentTB.Text;
    public string Organization => OrganizationTB.Text;
    public bool IsLegalEntity => LegalEntityCB.IsChecked.Value;
    public List<string> Owners => OwnersControls.Select(x => x.Value).Where(o => !string.IsNullOrWhiteSpace(o)).ToList();
    public StorageFile Plan;
    public StorageFile Picture;

    public bool IsEdited = false;

    private ObservableCollection<RemovableTextBox> OwnersControls { get; set; } = new();
    private CoreWebView2DevToolsProtocolEventReceiver jsLogReciever;

    public delegate void EditedHandler(object sender);

    public event EditedHandler Edited;
    public event PropertyChangedEventHandler PropertyChanged;

    public CreateContractDialog()
    {
        Edited += (s) => IsEdited = true;

        this.InitializeComponent();

        InitializeWV();
    }

    public CreateContractDialog(ContractDto contract)
    {
        Edited += (s) => IsEdited = true;

        this.InitializeComponent();

        BaileeTB.Text = contract.Bailee;
        AddressTB.Text = contract.Address;
        CommentTB.Text = contract.Comment;
        OrganizationTB.Text = contract.Organization;
        LegalEntityCB.IsChecked = contract.IsLegalEntity;

        if (contract.Owners != null)
        {
            foreach (var ownerName in contract.Owners.Split(';'))
            {
                AddOwner(ownerName);
            }
        }

        InitializeWV();
    }

    private async Task InitializeWV()
    {
        await WV.EnsureCoreWebView2Async();

        var htmlpath = Path.Combine(Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location), "Misc", "html");
        WV.CoreWebView2.SetVirtualHostNameToFolderMapping("app", @$"{htmlpath}", Microsoft.Web.WebView2.Core.CoreWebView2HostResourceAccessKind.Allow);
        
        WV.CoreWebView2.WebMessageReceived += CoreWebView2_WebMessageReceived;

        await this.WV.CoreWebView2.CallDevToolsProtocolMethodAsync("Log.enable", "{}");
        jsLogReciever = WV.CoreWebView2.GetDevToolsProtocolEventReceiver("Log.entryAdded");
        jsLogReciever.DevToolsProtocolEventReceived += (s, e) =>
        {
            //System.Diagnostics.Debug.WriteLine(e.ParameterObjectAsJson);
        };

        WV.CoreWebView2.Navigate("https://app/map/index.html");
    }

    private void CoreWebView2_WebMessageReceived(CoreWebView2 sender, CoreWebView2WebMessageReceivedEventArgs args)
    {
        AddressTB.Text = args.WebMessageAsJson[1..^1];
    }

    private void AddOwner(string? name = null)
    {
        var rtb = new RemovableTextBox();
        if (name != null) rtb.Value = name;

        rtb.TextChanged += (s, tbs, e) => Edited?.Invoke(s);
        rtb.RemoveRequested += (sender) =>
        {
            OwnersControls.Remove(rtb);
            Edited?.Invoke(rtb);
        };

        OwnersControls.Add(rtb);
    }

    private void NotifyPropertyChanged([CallerMemberName] string propertyName = "")
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }

    private void AddOwnerButtonClick(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        AddOwner();
    }

    private async void LoadPhotoButtonClick(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {        
        var file = await FilePickerHelper.PickSingleFile();

        if (file != null)
        {
            PhotoPath = file.Name;
            PhotoPathTB.Foreground = new SolidColorBrush(Colors.White);
            Picture = file;
            Edited?.Invoke(sender);
        }
        else
        {
            PhotoPath = "ошибка";
            PhotoPathTB.Foreground = new SolidColorBrush(Colors.IndianRed);
        }
    }

    private async void LoadPlanButtonClick(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        var file = await FilePickerHelper.PickSingleFile("rvt");

        if (file != null)
        {
            PlanPath = file.Name;
            PlanPathTB.Foreground = new SolidColorBrush(Colors.White);
            Plan = file;
            Edited?.Invoke(sender);
        }
        else
        {
            PlanPath = "ошибка";
            PlanPathTB.Foreground = new SolidColorBrush(Colors.IndianRed);
        }
    }

    private void BaileeTB_TextChanged(object sender, TextChangedEventArgs e)
    {
        Edited?.Invoke(sender);
    }

    private void AddressTB_TextChanged(object sender, TextChangedEventArgs e)
    {
        Edited?.Invoke(sender);
    }

    private void CommentTB_TextChanged(object sender, TextChangedEventArgs e)
    {
        Edited?.Invoke(sender);
    }

    private void OrganizationTB_TextChanged(object sender, TextChangedEventArgs e)
    {
        Edited?.Invoke(sender);
    }

    private void LegalEntityCB_Checked(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        Edited?.Invoke(sender);
    }

    private void LegalEntityCB_Unchecked(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        Edited?.Invoke(sender);
    }
}
