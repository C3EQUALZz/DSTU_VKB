using System.Reflection.Emit;
using Microsoft.EntityFrameworkCore;
using Shield.DataAccess.Models;

namespace Shield.Web.Data.Contexts;

public class DataContext : DbContext
{
    public DbSet<Contract> Contracts { get; set; }
    public DbSet<Picture> Pictures { get; set; }
    public DbSet<Plan> Plans { get; set; }

    public string DbPath { get; }

    public DataContext()
    {
        DbPath = "Data/Databases/Data.db";
    }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder) => optionsBuilder.UseSqlite($"Data Source={DbPath}");
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        
    }
}
