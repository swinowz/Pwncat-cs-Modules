#!/usr/bin/env python3
import os
import time
import zipfile

from rich.progress import (
    Progress,
    BarColumn,
    TextColumn,
    DownloadColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

from pwncat.util import console, copyfileobj, human_readable_size, human_readable_delta
from pwncat.commands import Complete, Parameter, CommandDefinition
from pwncat.platform import PlatformError


class Command(CommandDefinition):
    """
    Upload a tools zip file to the remote host
    """

    PROG = "upload_tools"
    ARGS = {
        "local_zip": Parameter(Complete.LOCAL_FILE, nargs="?", default="/home/sway/Desktop/save_mega/tools/LINUX/tools.zip", help="Local path to the tools zip"),
        "remote_path": Parameter(Complete.REMOTE_FILE, nargs="?", default="/tmp/tools.zip", help="Remote file path"),
    }

    def run(self, manager: "pwncat.manager.Manager", args):

        # Validate the zip file first
        try:
            console.log(f"validating zip file: [cyan]{args.local_zip}[/cyan]")
            with zipfile.ZipFile(args.local_zip, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                console.log(f"zip contains [green]{len(file_list)}[/green] files: {', '.join(file_list[:5])}{'...' if len(file_list) > 5 else ''}")
                
            file_size = os.path.getsize(args.local_zip)
            console.log(f"zip file size: [cyan]{human_readable_size(file_size)}[/cyan]")
            
        except zipfile.BadZipFile:
            console.log(f"[red]Error: {args.local_zip} is not a valid zip file[/red]")
            return
        except Exception as e:
            console.log(f"[red]Error validating zip: {e}[/red]")
            return

        # Create a progress bar for the upload
        progress = Progress(
            TextColumn("[bold cyan]{task.fields[filename]}", justify="right"),
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.1f}%",
            "•",
            DownloadColumn(),
            "•",
            TransferSpeedColumn(),
            "•",
            TimeRemainingColumn(),
        )

        try:
            # Upload the file
            length = os.path.getsize(args.local_zip)
            started = time.time()
            
            with progress:
                task_id = progress.add_task(
                    "upload", filename=args.remote_path, total=length, start=False
                )

                with open(args.local_zip, "rb") as source:
                    with manager.target.platform.open(args.remote_path, "wb") as destination:
                        progress.start_task(task_id)
                        copyfileobj(
                            source,
                            destination,
                            lambda count: progress.update(task_id, advance=count),
                        )

            elapsed = time.time() - started
            console.log(
                f"[bold green]uploaded [cyan]{human_readable_size(length)}[/cyan] "
                f"in [green]{human_readable_delta(elapsed)}[/green] to [cyan]{args.remote_path}[/cyan][/bold green]"
            )
            
        except (
            FileNotFoundError,
            PermissionError,
            IsADirectoryError,
            PlatformError,
        ) as exc:
            self.parser.error(str(exc)) 