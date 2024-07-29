using Microsoft.UI.Xaml.Media.Imaging;
using Windows.Storage.Streams;

namespace Shield.App.Helpers;
public class BitmapHelper
{
    public static BitmapImage BytesToBitmap(byte[] bytes)
    {
        using InMemoryRandomAccessStream ms = new InMemoryRandomAccessStream();
        using DataWriter writer = new DataWriter(ms.GetOutputStreamAt(0));
        writer.WriteBytes(bytes);
        writer.StoreAsync().GetResults();

        BitmapImage image = new BitmapImage();
        ms.Seek(0);
        image.SetSource(ms);

        return image;
    }
}
