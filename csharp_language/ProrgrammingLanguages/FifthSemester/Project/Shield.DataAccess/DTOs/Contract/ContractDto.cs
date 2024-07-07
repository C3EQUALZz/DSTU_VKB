using Shield.DataAccess.Models;
namespace Shield.DataAccess.DTOs;
public class ContractDto
{
    public string Address { get; set; }
    public List<string> Owners { get; set; }
    public string Bailee { get; set; }
    public Plan Plan { get; set; }
    public List<Picture> Pictures { get; set; }
}
