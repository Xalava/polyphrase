import tkinter as tk
from tkinter import ttk
import sys
import os
from polyphrase import PolyPhraseGenerator

class ModernFrame(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(padding="20")

class PolyPhraseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PolyPhrase Generator")
        self.root.minsize(500, 400)
        
        # Configure styles
        self.setup_styles()
        
        try:
            self.generator = PolyPhraseGenerator()
            self.setup_gui()
        except Exception as e:
            self.show_error(f"Failed to initialize: {str(e)}")
    
    def setup_styles(self):
        # Configure modern styles
        style = ttk.Style()
        style.configure('Title.TLabel', font=('Helvetica', 16, 'bold'))
        style.configure('Subtitle.TLabel', font=('Helvetica', 10))
        style.configure('Status.TLabel', font=('Helvetica', 9))
        
        # Modern button style
        style.configure('Generate.TButton',
                       font=('Helvetica', 11),
                       padding=10)
        
        # Custom entry style
        style.configure('Custom.TEntry',
                       padding=5,
                       font=('Helvetica', 11))
    
    def setup_gui(self):
        # Main container
        container = ModernFrame(self.root)
        container.grid(row=0, column=0, sticky="nsew")
        
        # Title and description
        title_frame = ModernFrame(container)
        title_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        ttk.Label(title_frame, 
                 text="PolyPhrase Password Generator",
                 style='Title.TLabel').pack(anchor="w")
        
        ttk.Label(title_frame,
                 text="Generate secure, multilingual passwords",
                 style='Subtitle.TLabel').pack(anchor="w")
        
        # Settings frame
        settings_frame = ModernFrame(container)
        settings_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        
        # Language selection
        lang_frame = ttk.Frame(settings_frame)
        lang_frame.pack(fill="x", pady=5)
        
        ttk.Label(lang_frame, text="Language:").pack(side="left")
        self.language_var = tk.StringVar(value="English")
        self.language_menu = ttk.Combobox(lang_frame,
                                        textvariable=self.language_var,
                                        values=["Poly", "Latin", "English", "Spanish", "French"],
                                        width=15)
        self.language_menu.pack(side="right")
        
        # Word count selection
        words_frame = ttk.Frame(settings_frame)
        words_frame.pack(fill="x", pady=5)
        
        ttk.Label(words_frame, text="Number of Words:").pack(side="left")
        self.num_words_var = tk.IntVar(value=4)
        self.num_words_spinbox = ttk.Spinbox(words_frame,
                                           from_=1,
                                           to=10,
                                           textvariable=self.num_words_var,
                                           width=5)
        self.num_words_spinbox.pack(side="right")
        
        # Password display frame
        password_frame = ModernFrame(container)
        password_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        
        self.result = ttk.Entry(password_frame,
                              width=50,
                              style='Custom.TEntry',
                              font=('Courier', 12))
        self.result.pack(fill="x", pady=10)
        
        # Generate button
        ttk.Button(container,
                  text="Generate Password",
                  style='Generate.TButton',
                  command=self.generate).grid(row=3,
                                            column=0,
                                            pady=10)
        
        # Status message
        self.status_label = ttk.Label(container,
                                    text="",
                                    style='Status.TLabel',
                                    wraplength=400)
        self.status_label.grid(row=4, column=0, pady=5)
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
    
    def generate(self):
        try:
            language = self.language_var.get().lower()
            num_words = self.num_words_var.get()
            password = self.generator.generate_password(num_words=num_words, language=language)
            
            # Update UI with new password
            self.result.delete(0, tk.END)
            self.result.insert(0, password)
            
            # Copy to clipboard and show status
            self.copy_to_clipboard(password)
            self.show_status("✓ Password generated and copied to clipboard!")
            
            # Highlight the password
            self.result.selection_range(0, tk.END)
            self.result.focus()
            
        except Exception as e:
            self.show_error(f"Error: {str(e)}")
    
    def copy_to_clipboard(self, text):
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
        except Exception as e:
            self.show_error(f"Failed to copy: {str(e)}")
    
    def show_status(self, message):
        self.status_label.config(text=message, foreground="green")
        self.root.after(3000, lambda: self.status_label.config(text=""))
    
    def show_error(self, message):
        self.status_label.config(text=message, foreground="#c42b1c")

if __name__ == "__main__":
    root = tk.Tk()
    app = PolyPhraseGUI(root)
    root.mainloop()
