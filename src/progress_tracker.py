"""Progress tracking utilities for better user experience."""

import sys
import time
from typing import Optional, TextIO


class ProgressBar:
    """Simple progress bar for console output."""
    
    def __init__(
        self, 
        total: int, 
        description: str = "Processing", 
        width: int = 50,
        file: Optional[TextIO] = None
    ):
        self.total = total
        self.current = 0
        self.description = description
        self.width = width
        self.file = file or sys.stdout
        self.start_time = time.time()
        self._last_update = 0
    
    def update(self, increment: int = 1) -> None:
        """Update progress by increment."""
        self.current = min(self.current + increment, self.total)
        
        # Only update display every 0.1 seconds to avoid flickering
        current_time = time.time()
        if current_time - self._last_update < 0.1 and self.current < self.total:
            return
        
        self._last_update = current_time
        self._display()
    
    def set_progress(self, value: int) -> None:
        """Set absolute progress value."""
        self.current = min(max(value, 0), self.total)
        self._display()
    
    def _display(self) -> None:
        """Display the progress bar."""
        if self.total == 0:
            return
        
        percent = (self.current / self.total) * 100
        filled_width = int(self.width * self.current / self.total)
        
        bar = '█' * filled_width + '░' * (self.width - filled_width)
        
        # Calculate ETA
        elapsed = time.time() - self.start_time
        if self.current > 0:
            eta = (elapsed / self.current) * (self.total - self.current)
            eta_str = f" ETA: {eta:.0f}s" if eta > 1 else ""
        else:
            eta_str = ""
        
        # Format output
        output = f"\r{self.description}: |{bar}| {percent:5.1f}% ({self.current}/{self.total}){eta_str}"
        
        self.file.write(output)
        self.file.flush()
        
        if self.current >= self.total:
            self.file.write("\n")
    
    def finish(self) -> None:
        """Mark progress as complete."""
        self.current = self.total
        self._display()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.current < self.total:
            self.finish()


class StepTracker:
    """Track multi-step processes."""
    
    def __init__(self, steps: list, description: str = "Processing"):
        self.steps = steps
        self.current_step = 0
        self.description = description
        self.start_time = time.time()
    
    def next_step(self, message: Optional[str] = None) -> None:
        """Move to next step."""
        if self.current_step < len(self.steps):
            step_name = self.steps[self.current_step]
            display_message = message or step_name
            
            elapsed = time.time() - self.start_time
            print(f"[{elapsed:6.1f}s] Step {self.current_step + 1}/{len(self.steps)}: {display_message}")
            
            self.current_step += 1
    
    def finish(self) -> None:
        """Mark all steps as complete."""
        total_time = time.time() - self.start_time
        print(f"[{total_time:6.1f}s] {self.description} completed successfully!")


def with_progress(iterable, description: str = "Processing", total: Optional[int] = None):
    """Wrap an iterable with a progress bar."""
    if total is None:
        try:
            total = len(iterable)
        except TypeError:
            # If iterable doesn't have len(), convert to list
            iterable = list(iterable)
            total = len(iterable)
    
    with ProgressBar(total, description) as pbar:
        for item in iterable:
            yield item
            pbar.update(1)