using Windows.Storage;
using Windows.Storage.Pickers;

namespace Shield.App.Helpers;

class FilePickerHelper
{
    /// <summary>
    /// Accepts file types in format "jpg|jpeg|png"
    /// </summary>
    /// <param name="fileTypes"></param>
    public static async Task<StorageFile?> PickSingleFile(string fileTypes = "jpg|jpeg|png", PickerLocationId suggestedStartLocation = PickerLocationId.Desktop, PickerViewMode viewMode = PickerViewMode.Thumbnail)
    {
        var openPicker = new FileOpenPicker();
        
        openPicker.ViewMode = viewMode;
        openPicker.SuggestedStartLocation = suggestedStartLocation;
        
        fileTypes.Split('|').ToList().ForEach(type => openPicker.FileTypeFilter.Add($".{type}"));
        
        return await openPicker.PickSingleFileAsync();
    }
}
