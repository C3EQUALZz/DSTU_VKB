using Shield.Web.Data.Models;

namespace Shield.Web.Interfaces;

public interface ITokenService
{
    public Task<string> CreateToken(User user);
}
