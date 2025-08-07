"""Dashboard for displaying real-time progress."""

import sys
import time
from typing import Optional

from ..models import Progress


class Dashboard:
    """Simple dashboard for displaying progress."""
    
    def __init__(self):
        self.last_update = time.time()
        self.last_stage = ""
        
    def update(self, progress: Progress):
        """Update the dashboard with new progress information."""
        # Clear previous line
        sys.stdout.write('\r' + ' ' * 80 + '\r')
        
        # Format progress bar
        bar_length = 40
        filled = int(bar_length * progress.percentage / 100)
        bar = '█' * filled + '░' * (bar_length - filled)
        
        # Format status line
        status = f"[{bar}] {progress.percentage:3.0f}% | {progress.stage.upper()}: {progress.message}"
        
        # Add agent info if in research stage
        if progress.stage == "research" and progress.active_agents > 0:
            status += f" ({progress.completed_agents}/{progress.active_agents} agents)"
        
        # Add cost info if available
        if progress.tokens_used > 0:
            status += f" | Tokens: {progress.tokens_used:,}"
            if progress.estimated_cost > 0:
                status += f" | Cost: ${progress.estimated_cost:.2f}"
        
        sys.stdout.write(status)
        sys.stdout.flush()
        
        # New line when stage changes or completes
        if progress.stage != self.last_stage or progress.percentage >= 100:
            sys.stdout.write('\n')
            self.last_stage = progress.stage
            
    def close(self):
        """Close the dashboard."""
        sys.stdout.write('\n')
        sys.stdout.flush()