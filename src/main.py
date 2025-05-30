import requests
from rich.console import Console
from rich.table import Table


def main():
    url = "https://1.1.1.1/cdn-cgi/trace"
    console = Console()

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        console.print(f"[bold red]Error fetching the trace details:[/bold red] {e}")
        return

    # Parse the response text into key-value pairs
    trace_data = {}
    for line in response.text.strip().splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            trace_data[key] = value

    table = Table()
    table.add_column("Network Trace", style="green", justify="left")
    table.add_column("Value", style="bold magenta", justify="left")
    colors = ["bright_cyan", "bright_yellow"]

    for i, (key, value) in enumerate(trace_data.items()):
        row_style = colors[i % 2]
        table.add_row(key, value, style=row_style)

    console.print(table)


if __name__ == "__main__":
    main()
