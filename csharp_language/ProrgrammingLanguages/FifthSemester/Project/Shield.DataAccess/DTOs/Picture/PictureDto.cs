namespace Shield.DataAccess.DTOs;
public class PictureDto
{
    public int? PictureId
    {
        get; set;
    }
    public string Title
    {
        get; set;
    }
    public string Type
    {
        get; set;
    }
    public byte[] Data
    {
        get; set;
    }
}
