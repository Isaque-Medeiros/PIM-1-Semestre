"""
OverlayWindow Module
Handles transparent overlay window for user feedback and status display
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from typing import Optional, Callable, Dict, Any
import logging
from PIL import Image, ImageTk
import numpy as np


class OverlayWindow:
    """Transparent overlay window for Latam Auto-Filler feedback"""
    
    def __init__(self, title: str = "Latam Auto-Filler"):
        """
        Initialize transparent overlay window
        
        Args:
            title: Window title
        """
        self.title = title
        self.root = None
        self.is_visible = False
        self.update_callback = None
        self.logger = logging.getLogger(__name__)
        
        # Window configuration
        self.window_width = 400
        self.window_height = 300
        self.opacity = 0.9
        self.position = (100, 100)  # Default position
        
        # UI Components
        self.status_label = None
        self.progress_bar = None
        self.status_text = None
        self.button_frame = None
        
        # Status tracking
        self.current_status = "Pronto"
        self.progress_value = 0
        self.is_processing = False
        
    def create_window(self):
        """Create the transparent overlay window"""
        try:
            # Create main window
            self.root = tk.Tk()
            self.root.title(self.title)
            self.root.geometry(f"{self.window_width}x{self.window_height}+{self.position[0]}+{self.position[1]}")
            
            # Make window transparent and always on top
            self.root.attributes('-alpha', self.opacity)
            self.root.attributes('-topmost', True)
            self.root.overrideredirect(True)  # Remove window borders
            
            # Set transparency color (make background transparent)
            self.root.configure(bg='black')
            self.root.attributes('-transparentcolor', 'black')
            
            # Create UI elements
            self._create_ui()
            
            # Bind events
            self.root.bind('<Button-1>', self._on_drag_start)
            self.root.bind('<B1-Motion>', self._on_drag_motion)
            self.root.bind('<Double-Button-1>', self._toggle_visibility)
            
            self.is_visible = True
            self.logger.info("Overlay window created successfully")
            
        except Exception as e:
            self.logger.error(f"Error creating overlay window: {e}")
            raise
    
    def _create_ui(self):
        """Create UI elements"""
        # Main frame with rounded corners simulation
        main_frame = tk.Frame(
            self.root, 
            bg='white', 
            relief='raised', 
            bd=2,
            width=self.window_width-20,
            height=self.window_height-20
        )
        main_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Title bar
        title_frame = tk.Frame(main_frame, bg='#2c3e50', height=30)
        title_frame.pack(fill='x', padx=2, pady=2)
        
        title_label = tk.Label(
            title_frame, 
            text=self.title, 
            fg='white', 
            bg='#2c3e50',
            font=('Arial', 10, 'bold')
        )
        title_label.pack(side='left', padx=10, pady=5)
        
        # Status area
        status_frame = tk.Frame(main_frame, bg='white')
        status_frame.pack(fill='x', padx=10, pady=5)
        
        self.status_label = tk.Label(
            status_frame,
            text="Status: Pronto",
            font=('Arial', 10),
            fg='#2c3e50',
            bg='white'
        )
        self.status_label.pack(anchor='w')
        
        # Progress bar
        progress_frame = tk.Frame(main_frame, bg='white')
        progress_frame.pack(fill='x', padx=10, pady=5)
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            orient='horizontal',
            length=300,
            mode='determinate'
        )
        self.progress_bar.pack(fill='x')
        
        # Status text area
        text_frame = tk.Frame(main_frame, bg='white')
        text_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.status_text = tk.Text(
            text_frame,
            height=6,
            width=40,
            bg='#f8f9fa',
            fg='#2c3e50',
            font=('Arial', 9),
            wrap='word'
        )
        self.status_text.pack(fill='both', expand=True)
        
        # Scrollbar for text area
        scrollbar = tk.Scrollbar(self.status_text)
        scrollbar.pack(side='right', fill='y')
        self.status_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.status_text.yview)
        
        # Button frame
        self.button_frame = tk.Frame(main_frame, bg='white')
        self.button_frame.pack(fill='x', padx=10, pady=5)
        
        # Control buttons
        self._create_buttons()
    
    def _create_buttons(self):
        """Create control buttons"""
        # Start button
        start_btn = tk.Button(
            self.button_frame,
            text="Iniciar",
            bg='#27ae60',
            fg='white',
            font=('Arial', 9, 'bold'),
            command=self._on_start
        )
        start_btn.pack(side='left', padx=5)
        
        # Stop button
        stop_btn = tk.Button(
            self.button_frame,
            text="Parar",
            bg='#e74c3c',
            fg='white',
            font=('Arial', 9, 'bold'),
            command=self._on_stop
        )
        stop_btn.pack(side='left', padx=5)
        
        # Clear button
        clear_btn = tk.Button(
            self.button_frame,
            text="Limpar",
            bg='#95a5a6',
            fg='white',
            font=('Arial', 9, 'bold'),
            command=self._on_clear
        )
        clear_btn.pack(side='left', padx=5)
        
        # Minimize button
        minimize_btn = tk.Button(
            self.button_frame,
            text="_",
            bg='#3498db',
            fg='white',
            font=('Arial', 9, 'bold'),
            width=3,
            command=self._toggle_visibility
        )
        minimize_btn.pack(side='right', padx=5)
    
    def _on_start(self):
        """Handle start button click"""
        if self.update_callback:
            self.update_callback('start')
    
    def _on_stop(self):
        """Handle stop button click"""
        if self.update_callback:
            self.update_callback('stop')
    
    def _on_clear(self):
        """Handle clear button click"""
        self.clear_status()
        if self.update_callback:
            self.update_callback('clear')
    
    def _toggle_visibility(self, event=None):
        """Toggle window visibility"""
        if self.is_visible:
            self.hide()
        else:
            self.show()
    
    def _on_drag_start(self, event):
        """Handle drag start"""
        self._drag_start_x = event.x
        self._drag_start_y = event.y
    
    def _on_drag_motion(self, event):
        """Handle drag motion"""
        try:
            x = self.root.winfo_x() + (event.x - self._drag_start_x)
            y = self.root.winfo_y() + (event.y - self._drag_start_y)
            self.root.geometry(f"+{x}+{y}")
        except:
            pass
    
    def show(self):
        """Show the overlay window"""
        if self.root:
            self.root.deiconify()
            self.is_visible = True
    
    def hide(self):
        """Hide the overlay window"""
        if self.root:
            self.root.withdraw()
            self.is_visible = False
    
    def destroy(self):
        """Destroy the overlay window"""
        if self.root:
            self.root.destroy()
            self.root = None
            self.is_visible = False
    
    def update_status(self, status: str, progress: int = None):
        """
        Update status display
        
        Args:
            status: Status message
            progress: Progress percentage (0-100)
        """
        self.current_status = status
        
        if self.root and self.root.winfo_exists():
            # Update status label
            if self.status_label:
                self.status_label.config(text=f"Status: {status}")
            
            # Update progress bar
            if progress is not None and self.progress_bar:
                self.progress_bar['value'] = progress
            
            # Update status text with timestamp
            timestamp = time.strftime("%H:%M:%S")
            self.status_text.insert('end', f"[{timestamp}] {status}\n")
            self.status_text.see('end')
    
    def clear_status(self):
        """Clear status text"""
        if self.status_text:
            self.status_text.delete('1.0', 'end')
    
    def set_update_callback(self, callback: Callable):
        """
        Set callback function for button events
        
        Args:
            callback: Function to call with event type
        """
        self.update_callback = callback
    
    def show_message(self, message: str, message_type: str = "info"):
        """
        Show a message dialog
        
        Args:
            message: Message text
            message_type: Type of message (info, warning, error)
        """
        if message_type == "error":
            messagebox.showerror("Erro", message)
        elif message_type == "warning":
            messagebox.showwarning("Aviso", message)
        else:
            messagebox.showinfo("Informação", message)
    
    def update_progress(self, value: int):
        """
        Update progress bar
        
        Args:
            value: Progress value (0-100)
        """
        if self.progress_bar and self.root and self.root.winfo_exists():
            self.progress_bar['value'] = value
    
    def set_processing(self, is_processing: bool):
        """
        Set processing state
        
        Args:
            is_processing: True if processing, False otherwise
        """
        self.is_processing = is_processing
        status_text = "Processando..." if is_processing else "Pronto"
        self.update_status(status_text)
    
    def add_log_entry(self, message: str, level: str = "info"):
        """
        Add a log entry to the status text
        
        Args:
            message: Log message
            level: Log level (info, warning, error)
        """
        timestamp = time.strftime("%H:%M:%S")
        color_tag = {
            "info": "black",
            "warning": "orange", 
            "error": "red"
        }.get(level, "black")
        
        # For now, just add text (coloring would require more complex text widget setup)
        self.status_text.insert('end', f"[{timestamp}] [{level.upper()}] {message}\n")
        self.status_text.see('end')
    
    def get_position(self) -> tuple:
        """Get current window position"""
        if self.root:
            return (self.root.winfo_x(), self.root.winfo_y())
        return self.position
    
    def set_position(self, x: int, y: int):
        """
        Set window position
        
        Args:
            x: X coordinate
            y: Y coordinate
        """
        self.position = (x, y)
        if self.root:
            self.root.geometry(f"+{x}+{y}")
    
    def set_opacity(self, opacity: float):
        """
        Set window opacity
        
        Args:
            opacity: Opacity value (0.0 to 1.0)
        """
        self.opacity = max(0.1, min(1.0, opacity))  # Clamp between 0.1 and 1.0
        if self.root:
            self.root.attributes('-alpha', self.opacity)
    
    def run(self):
        """Run the overlay window main loop"""
        if self.root:
            try:
                self.root.mainloop()
            except Exception as e:
                self.logger.error(f"Error in overlay window main loop: {e}")
    
    def quit(self):
        """Quit the overlay window"""
        if self.root:
            self.root.quit()
    
    def is_running(self) -> bool:
        """Check if window is running"""
        return self.root is not None and self.is_visible