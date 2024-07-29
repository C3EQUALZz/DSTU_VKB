using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;

using Shield.App.Activation;
using Shield.App.Contracts.Services;
using Shield.App.Views;

using Shield.App.Helpers;
using Shield.App.Dialogs;

namespace Shield.App.Services;

public class ActivationService : IActivationService
{
    private readonly ActivationHandler<LaunchActivatedEventArgs> _defaultHandler;
    private readonly IEnumerable<IActivationHandler> _activationHandlers;
    private readonly IThemeSelectorService _themeSelectorService;
    private UIElement? _shell = null;

    public ActivationService(ActivationHandler<LaunchActivatedEventArgs> defaultHandler, IEnumerable<IActivationHandler> activationHandlers, IThemeSelectorService themeSelectorService)
    {
        _defaultHandler = defaultHandler;
        _activationHandlers = activationHandlers;
        _themeSelectorService = themeSelectorService;
    }

    public async Task ActivateAsync(object activationArgs)
    {
        // Execute tasks before activation.
        await InitializeAsync();

        // Set the MainWindow Content.
        if (App.MainWindow.Content == null)
        {
            _shell = App.GetService<ShellPage>();
            App.MainWindow.Content = _shell ?? new Frame();
        }

        // Handle activation via ActivationHandlers.
        await HandleActivationAsync(activationArgs);

        // Activate the MainWindow.
        App.MainWindow.Activate();

        // Execute tasks after activation.
        await StartupAsync();

        var root = App.MainWindow.Content as FrameworkElement;
        if (root != null)
            root.Loaded += async (s, e) =>
            {
                var response = await ApiHelper.CheckConnection();

                if (response == null || !response.IsSuccessStatusCode)
                {
                    await ShowLoginNotification(root.XamlRoot);
                }
            };
    }

    private async Task ShowLoginNotification(XamlRoot root)
    {
        var response = await AuthHelper.ShowAuthDialogAsync(root);

        if (response != null)
        {
            ShellPage.Instance.Notify("Error".GetLocalized(), response);
        }
    }

    private async Task HandleActivationAsync(object activationArgs)
    {
        var activationHandler = _activationHandlers.FirstOrDefault(h => h.CanHandle(activationArgs));

        if (activationHandler != null)
        {
            await activationHandler.HandleAsync(activationArgs);
        }

        if (_defaultHandler.CanHandle(activationArgs))
        {
            await _defaultHandler.HandleAsync(activationArgs);
        }
    }

    private async Task InitializeAsync()
    {
        await _themeSelectorService.InitializeAsync().ConfigureAwait(false);
        await Task.CompletedTask;
    }

    private async Task StartupAsync()
    {
        await _themeSelectorService.SetRequestedThemeAsync();
        await Task.CompletedTask;
    }
}
