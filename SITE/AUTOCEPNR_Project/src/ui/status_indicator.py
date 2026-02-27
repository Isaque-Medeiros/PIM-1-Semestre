"""
StatusIndicator Module
Handles status indicators and notifications for the Latam Auto-Filler
"""

import threading
import time
from typing import Optional, Callable, Dict, Any, List
import logging
from enum import Enum


class StatusLevel(Enum):
    """Status levels for notifications"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"
    PROCESSING = "processing"


class StatusIndicator:
    """Status indicator for Latam Auto-Filler operations"""
    
    def __init__(self):
        """Initialize status indicator"""
        self.logger = logging.getLogger(__name__)
        
        # Status tracking
        self.current_status = StatusLevel.INFO
        self.status_message = "Pronto"
        self.is_processing = False
        self.progress = 0
        
        # Callbacks
        self.status_callback = None
        self.progress_callback = None
        self.notification_callback = None
        
        # Status history
        self.status_history: List[Dict[str, Any]] = []
        self.max_history = 100
        
    def set_status(self, status: StatusLevel, message: str, progress: int = None):
        """
        Set current status
        
        Args:
            status: Status level
            message: Status message
            progress: Progress percentage (0-100)
        """
        self.current_status = status
        self.status_message = message
        
        if progress is not None:
            self.progress = max(0, min(100, progress))
        
        # Add to history
        self._add_to_history(status, message, progress)
        
        # Call callbacks
        if self.status_callback:
            self.status_callback(status, message)
        
        if self.progress_callback and progress is not None:
            self.progress_callback(progress)
        
        # Log status
        self._log_status(status, message)
    
    def _add_to_history(self, status: StatusLevel, message: str, progress: int = None):
        """Add status to history"""
        entry = {
            'timestamp': time.time(),
            'status': status.value,
            'message': message,
            'progress': progress
        }
        
        self.status_history.append(entry)
        
        # Keep history size manageable
        if len(self.status_history) > self.max_history:
            self.status_history.pop(0)
    
    def _log_status(self, status: StatusLevel, message: str):
        """Log status message"""
        log_level = {
            StatusLevel.INFO: self.logger.info,
            StatusLevel.WARNING: self.logger.warning,
            StatusLevel.ERROR: self.logger.error,
            StatusLevel.SUCCESS: self.logger.info,
            StatusLevel.PROCESSING: self.logger.info
        }.get(status, self.logger.info)
        
        log_level(f"[{status.value.upper()}] {message}")
    
    def start_processing(self, message: str = "Processando..."):
        """Start processing state"""
        self.is_processing = True
        self.set_status(StatusLevel.PROCESSING, message, 0)
    
    def stop_processing(self, success: bool = True, message: str = None):
        """Stop processing state"""
        self.is_processing = False
        
        if success:
            final_message = message or "Processamento concluído com sucesso"
            self.set_status(StatusLevel.SUCCESS, final_message, 100)
        else:
            final_message = message or "Processamento falhou"
            self.set_status(StatusLevel.ERROR, final_message, 0)
    
    def update_progress(self, progress: int, message: str = None):
        """
        Update progress
        
        Args:
            progress: Progress percentage (0-100)
            message: Optional status message
        """
        progress = max(0, min(100, progress))
        self.progress = progress
        
        if message:
            self.set_status(self.current_status, message, progress)
        elif self.progress_callback:
            self.progress_callback(progress)
    
    def show_notification(self, message: str, level: StatusLevel = StatusLevel.INFO):
        """
        Show notification
        
        Args:
            message: Notification message
            level: Notification level
        """
        if self.notification_callback:
            self.notification_callback(message, level)
        
        # Also log the notification
        self.set_status(level, message)
    
    def get_status_info(self) -> Dict[str, Any]:
        """Get current status information"""
        return {
            'status': self.current_status.value,
            'message': self.status_message,
            'is_processing': self.is_processing,
            'progress': self.progress,
            'timestamp': time.time()
        }
    
    def get_status_history(self, limit: int = None) -> List[Dict[str, Any]]:
        """
        Get status history
        
        Args:
            limit: Maximum number of entries to return
        """
        if limit:
            return self.status_history[-limit:]
        return self.status_history.copy()
    
    def clear_history(self):
        """Clear status history"""
        self.status_history.clear()
    
    def set_status_callback(self, callback: Callable[[StatusLevel, str], None]):
        """
        Set status change callback
        
        Args:
            callback: Function to call on status change
        """
        self.status_callback = callback
    
    def set_progress_callback(self, callback: Callable[[int], None]):
        """
        Set progress change callback
        
        Args:
            callback: Function to call on progress change
        """
        self.progress_callback = callback
    
    def set_notification_callback(self, callback: Callable[[str, StatusLevel], None]):
        """
        Set notification callback
        
        Args:
            callback: Function to call on notification
        """
        self.notification_callback = callback
    
    def reset(self):
        """Reset status indicator"""
        self.current_status = StatusLevel.INFO
        self.status_message = "Pronto"
        self.is_processing = False
        self.progress = 0
        self.clear_history()
    
    def get_processing_time_estimate(self, current_step: int, total_steps: int) -> Dict[str, Any]:
        """
        Get estimated processing time
        
        Args:
            current_step: Current step number
            total_steps: Total number of steps
            
        Returns:
            Dictionary with time estimates
        """
        if current_step <= 0 or total_steps <= 0:
            return {"error": "Invalid step numbers"}
        
        # Estimate based on typical processing times
        step_times = {
            1: 5,   # OCR processing
            2: 2,   # Field parsing
            3: 3,   # Validation
            4: 1,   # Browser focusing
            5: 10,  # Form filling (with delays)
            6: 3    # Submission
        }
        
        current_step_time = step_times.get(current_step, 5)
        remaining_steps = total_steps - current_step
        remaining_time = sum(step_times.get(i, 5) for i in range(current_step + 1, total_steps + 1))
        
        return {
            "current_step": current_step,
            "total_steps": total_steps,
            "current_step_time": current_step_time,
            "remaining_steps": remaining_steps,
            "remaining_time": remaining_time,
            "total_time": current_step_time + remaining_time,
            "completion_percentage": (current_step / total_steps) * 100
        }
    
    def validate_status_consistency(self) -> List[str]:
        """
        Validate status consistency and return any issues found
        
        Returns:
            List of consistency issues
        """
        issues = []
        
        # Check if processing state is consistent with progress
        if self.is_processing and self.progress >= 100:
            issues.append("Processing state active but progress is 100%")
        
        if not self.is_processing and self.progress > 0 and self.progress < 100:
            issues.append("Progress indicates processing but processing state is inactive")
        
        # Check status message consistency
        if self.current_status == StatusLevel.PROCESSING and not self.is_processing:
            issues.append("Status indicates processing but processing state is inactive")
        
        if self.current_status in [StatusLevel.SUCCESS, StatusLevel.ERROR] and self.is_processing:
            issues.append("Status indicates completion but processing state is active")
        
        return issues
    
    def export_status_report(self) -> Dict[str, Any]:
        """Export complete status report"""
        return {
            "current_status": self.get_status_info(),
            "status_history": self.get_status_history(),
            "consistency_issues": self.validate_status_consistency(),
            "summary": {
                "total_history_entries": len(self.status_history),
                "processing_active": self.is_processing,
                "progress_percentage": self.progress,
                "status_level": self.current_status.value
            }
        }