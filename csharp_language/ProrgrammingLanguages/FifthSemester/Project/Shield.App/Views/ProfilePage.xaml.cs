using System.ComponentModel;
using System.Runtime.CompilerServices;
using Microsoft.UI.Xaml.Controls;
using Shield.App.Helpers;
using Windows.Storage;
using Shield.DataAccess.DTOs;
using System.Net.Http.Json;

namespace Shield.App.Views;
public sealed partial class ProfilePage : Page, INotifyPropertyChanged
{
    private bool isLoggedIn = false;
    public bool IsLoggedIn
    {
        get => isLoggedIn;
        set
        {
            if (value != isLoggedIn)
            {
                isLoggedIn = value;
                NotifyPropertyChanged();
                NotifyPropertyChanged(nameof(IsNotLoggedIn));
                NotifyPropertyChanged(nameof(Profile));
            }
        }
    }
    public bool IsNotLoggedIn => !isLoggedIn;
    public ProfileInfoDto Profile { get; set; }

    public event PropertyChangedEventHandler PropertyChanged;

    public ProfilePage()
    {
        this.InitializeComponent();
    }

    private void NotifyPropertyChanged([CallerMemberName] string propertyName = "")
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }

    private async Task VerifyLoginStatus()
    {
        var response = await ApiHelper.CheckConnection();

        if (response == null || !response.IsSuccessStatusCode)
        {
            IsLoggedIn = false;
        }
        else
        {
            // TODO: Get profile data
            var resp = await ApiHelper.Me();
            var profile = await resp.Content.ReadFromJsonAsync<ProfileInfoDto>();
            Profile = profile;

            IsLoggedIn = true;
        }
    }

    private async void LoginButton_Click(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        await AuthHelper.ShowAuthDialogAsync(this.XamlRoot);
        await VerifyLoginStatus();
    }

    private async void Page_Loaded(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        await VerifyLoginStatus();
    }

    private void LogoutButton_Click(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        if (ApplicationData.Current.LocalSettings.Values.ContainsKey("apiToken"))
        {
            ApplicationData.Current.LocalSettings.Values.Remove("apiToken");
            IsLoggedIn = false;
        }
    }
}
