using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Shield.Web.Migrations
{
    /// <inheritdoc />
    public partial class SignDate : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<DateOnly>(
                name: "SignDate",
                table: "Contracts",
                type: "TEXT",
                nullable: false,
                defaultValue: new DateOnly(1, 1, 1));
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "SignDate",
                table: "Contracts");
        }
    }
}
