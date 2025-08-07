"""Dashboard UI for displaying research progress."""

import threading
import time
from typing import Optional
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.table import Table


class Dashboard:
    """Real-time dashboard for research progress."""
    
    def __init__(self):
        self.console = Console()
        self.live = None
        self.layout = Layout()
        self.running = False
        self.thread = None
        
        # Progress tracking
        self.stage = "initializing"
        self.percentage = 0.0
        self.active_agents = 0
        self.completed_agents = 0
        self.tokens_used = 0
        self.estimated_cost = 0.0
        self.message = "Starting research..."
        
        self._setup_layout()
    
    def _setup_layout(self):
        """Set up the dashboard layout."""
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=3)
        )
        
        self.layout["body"].split_row(
            Layout(name="progress", ratio=2),
            Layout(name="stats", ratio=1)
        )
    
    def start(self):
        """Start the dashboard in a separate thread."""
        self.running = True
        self.thread = threading.Thread(target=self._run)
        self.thread.start()
    
    def close(self):
        """Stop the dashboard."""
        self.running = False
        if self.thread:
            self.thread.join()
        if self.live:
            self.live.stop()
    
    def _run(self):
        """Run the dashboard update loop."""
        with Live(self.layout, refresh_per_second=4, console=self.console) as live:
            self.live = live
            while self.running:
                self._update_display()
                time.sleep(0.25)
    
    def _update_display(self):
        """Update the dashboard display."""
        # Header
        self.layout["header"].update(
            Panel(
                "[bold cyan]EssayForge Research Dashboard[/bold cyan]",
                style="cyan"
            )
        )
        
        # Progress
        progress_panel = self._create_progress_panel()
        self.layout["progress"].update(progress_panel)
        
        # Stats
        stats_panel = self._create_stats_panel()
        self.layout["stats"].update(stats_panel)
        
        # Footer
        self.layout["footer"].update(
            Panel(
                f"[dim]{self.message}[/dim]",
                style="dim"
            )
        )
    
    def _create_progress_panel(self) -> Panel:
        """Create the progress panel."""
        progress = Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            expand=True
        )
        
        # Add progress bars
        overall_task = progress.add_task(
            f"[cyan]Overall Progress - {self.stage.title()}",
            total=100,
            completed=self.percentage
        )
        
        if self.active_agents > 0 or self.completed_agents > 0:
            agents_task = progress.add_task(
                f"[green]Agents Progress",
                total=self.active_agents + self.completed_agents,
                completed=self.completed_agents
            )
        
        return Panel(
            progress,
            title="Progress",
            border_style="green"
        )
    
    def _create_stats_panel(self) -> Panel:
        """Create the statistics panel."""
        table = Table(show_header=False, box=None)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="white")
        
        table.add_row("Stage", self.stage.title())
        table.add_row("Active Agents", str(self.active_agents))
        table.add_row("Completed Agents", str(self.completed_agents))
        table.add_row("Tokens Used", f"{self.tokens_used:,}")
        table.add_row("Estimated Cost", f"${self.estimated_cost:.2f}")
        
        return Panel(
            table,
            title="Statistics",
            border_style="blue"
        )
    
    def update_progress(
        self,
        stage: Optional[str] = None,
        percentage: Optional[float] = None,
        active_agents: Optional[int] = None,
        completed_agents: Optional[int] = None,
        tokens_used: Optional[int] = None,
        estimated_cost: Optional[float] = None,
        message: Optional[str] = None
    ):
        """Update the dashboard progress."""
        if stage is not None:
            self.stage = stage
        if percentage is not None:
            self.percentage = percentage
        if active_agents is not None:
            self.active_agents = active_agents
        if completed_agents is not None:
            self.completed_agents = completed_agents
        if tokens_used is not None:
            self.tokens_used = tokens_used
        if estimated_cost is not None:
            self.estimated_cost = estimated_cost
        if message is not None:
            self.message = message