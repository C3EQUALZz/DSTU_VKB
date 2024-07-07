namespace Shield.DataAccess.Models;
public class Picture
{
    public int PictureId { get; set; }
    public string Title { get; set; }
    public string Type { get; set; }
    public byte[] Data { get; set; }
    //public Contract Contract { get; set; }
}
