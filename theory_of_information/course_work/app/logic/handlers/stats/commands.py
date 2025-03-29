from app.logic.commands.stats import GetFileFullStatsCommand
from app.logic.handlers.stats.base import FileStatsCommandHandler


class GetFileFullStatsCommandHandler(FileStatsCommandHandler[GetFileFullStatsCommand]):
    def __call__(self, command: GetFileFullStatsCommand) -> None:
        stat = path.stat()
        console = Console()

        table = Table(title="📁 File Statistics", show_header=True, header_style="bold magenta")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Name", path.name)
        table.add_row("Size", f"{stat.st_size / 1024:.2f} KB")
        table.add_row("Type", "📂 Directory" if path.is_dir() else "📄 File")
        table.add_row("Modified", datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"))
        table.add_row("Created", datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S"))
        table.add_row("Permissions", oct(stat.st_mode)[-3:])

        console.print(table)
