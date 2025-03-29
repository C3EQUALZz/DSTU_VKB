from typing import TYPE_CHECKING

from rich.console import Console
from rich.table import Table

from app.infrastructure.services.file_stat import FileStatService
from app.logic.commands.stats import GetFileFullStatsCommand
from app.logic.handlers.stats.base import FileStatsCommandHandler

if TYPE_CHECKING:
    from app.domain.entities.file_objects import FileStatistic


class GetFileFullStatsCommandHandler(FileStatsCommandHandler[GetFileFullStatsCommand]):
    def __call__(self, command: GetFileFullStatsCommand) -> None:
        service: FileStatService = FileStatService()

        statistic: FileStatistic = service.get_file_full_stat(command.file_path)

        console = Console()

        table = Table(title="📁 File Statistics", show_header=True, header_style="bold magenta")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Name", statistic.name)
        table.add_row("Size", statistic.size.as_generic_type())
        table.add_row("Type", statistic.type_of_file.as_generic_type())
        table.add_row("Modified", statistic.updated_at.strftime("%Y-%m-%d %H:%M:%S"))
        table.add_row("Created", statistic.created_at.strftime("%Y-%m-%d %H:%M:%S"))
        table.add_row("Permissions", statistic.permissions.as_generic_type())

        console.print(table)
