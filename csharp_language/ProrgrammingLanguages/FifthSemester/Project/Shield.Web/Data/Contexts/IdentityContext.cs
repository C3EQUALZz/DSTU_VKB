using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;

using Shield.Web.Data.Models;

namespace Shield.Web.Data.Contexts;

public class IdentityContext : IdentityDbContext<User>
{
    public string DbPath { get; }

    public IdentityContext()
    {
        DbPath = "Data/Databases/Identity.db";
    }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder) => optionsBuilder.UseSqlite($"Data Source={DbPath}");
}
