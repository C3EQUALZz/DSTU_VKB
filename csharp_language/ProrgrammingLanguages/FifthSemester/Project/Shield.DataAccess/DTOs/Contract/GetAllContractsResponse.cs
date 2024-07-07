using Shield.DataAccess.Models;
namespace Shield.DataAccess.DTOs;
public class GetAllContractsResponse
{
    public List<Contract> Contracts { get; set; }
}
