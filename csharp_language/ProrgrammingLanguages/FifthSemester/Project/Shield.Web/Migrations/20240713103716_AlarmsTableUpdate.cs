using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Shield.Web.Migrations
{
    /// <inheritdoc />
    public partial class AlarmsTableUpdate : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Alarm_Contracts_ContractId",
                table: "Alarm");

            migrationBuilder.DropPrimaryKey(
                name: "PK_Alarm",
                table: "Alarm");

            migrationBuilder.RenameTable(
                name: "Alarm",
                newName: "Alarms");

            migrationBuilder.RenameIndex(
                name: "IX_Alarm_ContractId",
                table: "Alarms",
                newName: "IX_Alarms_ContractId");

            migrationBuilder.AddPrimaryKey(
                name: "PK_Alarms",
                table: "Alarms",
                column: "AlarmId");

            migrationBuilder.AddForeignKey(
                name: "FK_Alarms_Contracts_ContractId",
                table: "Alarms",
                column: "ContractId",
                principalTable: "Contracts",
                principalColumn: "ContractId",
                onDelete: ReferentialAction.Cascade);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Alarms_Contracts_ContractId",
                table: "Alarms");

            migrationBuilder.DropPrimaryKey(
                name: "PK_Alarms",
                table: "Alarms");

            migrationBuilder.RenameTable(
                name: "Alarms",
                newName: "Alarm");

            migrationBuilder.RenameIndex(
                name: "IX_Alarms_ContractId",
                table: "Alarm",
                newName: "IX_Alarm_ContractId");

            migrationBuilder.AddPrimaryKey(
                name: "PK_Alarm",
                table: "Alarm",
                column: "AlarmId");

            migrationBuilder.AddForeignKey(
                name: "FK_Alarm_Contracts_ContractId",
                table: "Alarm",
                column: "ContractId",
                principalTable: "Contracts",
                principalColumn: "ContractId",
                onDelete: ReferentialAction.Cascade);
        }
    }
}
