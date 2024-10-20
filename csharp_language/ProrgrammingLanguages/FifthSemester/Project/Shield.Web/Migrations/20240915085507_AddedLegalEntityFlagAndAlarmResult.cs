using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Shield.Web.Migrations
{
    /// <inheritdoc />
    public partial class AddedLegalEntityFlagAndAlarmResult : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<bool>(
                name: "IsLegalEntity",
                table: "Contracts",
                type: "INTEGER",
                nullable: false,
                defaultValue: false);

            migrationBuilder.AddColumn<int>(
                name: "Result",
                table: "Alarms",
                type: "INTEGER",
                nullable: false,
                defaultValue: 0);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "IsLegalEntity",
                table: "Contracts");

            migrationBuilder.DropColumn(
                name: "Result",
                table: "Alarms");
        }
    }
}
