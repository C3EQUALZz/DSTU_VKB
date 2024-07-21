using Microsoft.UI.Xaml.Controls;
using Shield.App.Controls;
using Shield.DataAccess.DTOs;
using Microsoft.UI.Xaml;
using System.Net.Http.Json;

namespace Shield.App.Helpers;
public static class AuthHelper
{
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
            await ApiHelper.Login(content.Login, content.Password);
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

            await ApiHelper.Login(content.Login, content.Password);
        }

        return null;
    }
}
