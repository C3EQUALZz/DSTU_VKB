using Microsoft.UI.Xaml.Controls;
using Shield.App.Controls;
using Shield.DataAccess.DTOs;
using Microsoft.UI.Xaml;
using System.Net.Http.Json;
using Windows.Storage;

namespace Shield.App.Helpers;
public class AuthHelper
{
    public delegate void LoginHandler();
    public delegate void RegisterHandler();

    public event LoginHandler Login;
    public event RegisterHandler Register;

    private static AuthHelper _instance;
    public static AuthHelper Instance => _instance ??= new AuthHelper();

    public static async Task<string?> ShowAuthDialogAsync(XamlRoot root)
    {
        var dialog = new ContentDialog();
        var content = new RegisterLoginContent();

        dialog.XamlRoot = root;
        dialog.Style = Application.Current.Resources["DefaultContentDialogStyle"] as Style;
        dialog.Title = "Auth".GetLocalized();
        dialog.PrimaryButtonText = "Apply".GetLocalized();
        dialog.SecondaryButtonText = "Register".GetLocalized();
        dialog.CloseButtonText = "Cancel".GetLocalized();
        dialog.Content = content;
        dialog.DefaultButton = ContentDialogButton.Primary;

        var result = await dialog.ShowAsync();

        if (result == ContentDialogResult.Primary)
        {
            var response = await ApiHelper.Login(content.Login, content.Password);

            if (response == null) return null;

            if (!response.IsSuccessStatusCode)
            {
                System.Diagnostics.Debug.WriteLine(await response.Content.ReadAsStringAsync());

                try
                {
                    return string.Join("\n", (await response.Content.ReadFromJsonAsync<HttpResponseDto>()).Errors.Values.SelectMany(x => x));
                }
                catch
                {
                    return await response.Content.ReadAsStringAsync();
                }
            }

            var dto = await response.Content.ReadFromJsonAsync<LoginResponseDto>();

            if (dto != null)
            {
                ApplicationData.Current.LocalSettings.Values["apiToken"] = dto.Token;
                Instance.Login?.Invoke();
            }
        }
        else if (result == ContentDialogResult.Secondary)
        {
            return await ShowRegisterDialogAsync(root);
        }

        return null;
    }
    public static async Task<string?> ShowRegisterDialogAsync(XamlRoot root)
    {
        var dialog = new ContentDialog();
        var content = new RegisterContent();

        dialog.XamlRoot = root;
        dialog.Style = Application.Current.Resources["DefaultContentDialogStyle"] as Style;
        dialog.Title = "Register".GetLocalized();
        dialog.PrimaryButtonText = "Apply".GetLocalized();
        dialog.CloseButtonText = "Cancel".GetLocalized();
        dialog.Content = content;
        dialog.DefaultButton = ContentDialogButton.Primary;

        var result = await dialog.ShowAsync();

        if (result == ContentDialogResult.Primary)
        {
            var response = await ApiHelper.Register(content.Login, content.Password, content.Email);

            if (response == null) return null;

            if (!response.IsSuccessStatusCode)
            {
                return string.Join("\n", (await response.Content.ReadFromJsonAsync<HttpResponseDto>()).Errors.Values.SelectMany(x => x));
            }

            Instance.Register?.Invoke();
            await ApiHelper.Login(content.Login, content.Password);
        }

        return null;
    }
}
