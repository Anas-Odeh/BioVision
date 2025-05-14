# -*- coding: utf-8 -*-
"""
Created on Sun May 11 15:17:07 2025

@author: AnasO
"""

# =============================================================================
# BioVision AI Platform: A User-Friendly Tool for Medical Image Analysis

# This application provides an intuitive graphical interface for researchers to perform advanced analysis on medical images.
 
# It features two main tools:

# 1. Instance Segmentation: Uses AI (YOLO and SAM) to automatically detect and precisely outline objects of interest in images, allowing for detailed measurement and analysis.
# 2. Classification: Employs AI (YOLO) to categorize images into predefined classes, aiding in diagnostic and research workflows.

# BioVision simplifies complex image processing by offering a step-by-step interface to select images, configure AI models, 
# and obtain results, including visual outputs and organized data in Excel files. 
# It's designed to be accessible to both non-programmers and developers in the medical research field.
# =============================================================================


#%%

import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import sys

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):

    try:

        import pyi_splash

        pyi_splash.update_text("Initializing BioVision...")

    except ImportError:

        pass  

import itertools

import threading

from colorama import Fore, Style, init,Back

import time

from tqdm import tqdm

from PIL import Image, ImageTk

# Your initial application setup here
print("\nInitializing the application...\n\nplease wait...", flush=True)

init(autoreset=True)

def print_welcome_message():

    welcome_message = r"""
                             Welcome To  
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            ~  ____  _    __     ___     _             ~
            ~ | __ )(_) __\ \   / (_)___(_) ___  _ __  ~
            ~ |  _ \| |/ _ \ \ / /| / __| |/ _ \| '_ \ ~
            ~ | |_) | | (_) \ V / | \__ \ | (_) | | | |~
            ~ |____/|_|\___/ \_/  |_|___/_|\___/|_| |_|~
            ~                                          ~
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
             
"""
    print("\n" * 3, flush=True) 

    print(Fore.GREEN + Style.BRIGHT + welcome_message, flush=True)

    time.sleep(1)  

print_welcome_message()

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):

    try:

        pyi_splash.close()

    except ImportError:

        pass


init(autoreset=True)

class CircularProgress:
    
    def __init__(self, message="Loading", total_steps=100, delay=0.1):
    
        self.message = message
        
        self.total_steps = total_steps
        
        self.current_step = 0
        
        self.delay = delay
        
        self.busy = False
        
        self.spinner = itertools.cycle(['◜', '◠', '◝', '◞', '◡', '◟'])

    def spinner_task(self):
        
        while self.busy:
        
            progress = int(100 * self.current_step / self.total_steps)
            
            sys.stdout.write(f'\r{self.message} {next(self.spinner)} {progress}%')
            
            sys.stdout.flush()
            
            if self.current_step < self.total_steps:
            
                self.current_step += 1
            
            time.sleep(self.delay)
            
            if progress >= 100:
            
                self.busy = False
       
        sys.stdout.write('\r' + ' ' * (len(self.message) + 7) + '\r')  # Clean up

    def __enter__(self):
       
        self.busy = True
       
        threading.Thread(target=self.spinner_task).start()

    def __exit__(self, exception, value, tb):
      
        self.busy = False
       
        time.sleep(self.delay)


with CircularProgress("Importing libraries", total_steps=100):
    
    import tkinter as tk
   
    from tkinter import ttk, filedialog, messagebox
    
    from ultralytics import YOLO
    
    from ultralytics import SAM
    
    import os
    
    import cv2
    
    import numpy as np
    
    import pandas as pd
    
    import torch
    
    import threading
    
    from PIL import Image, ImageDraw, ImageFont
    
    from glob import glob
    
    import ctypes 
    
    # Enable DPI awareness for high-resolution displays (Windows-specific)
    try:
        
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Enables per-monitor DPI awareness
        
    except Exception:
        
        pass  # If not on Windows or DPI awareness is already set, ignore

print("Imports completed.\n\nPlease wait, you're almost there...\n\nLaunching the FibroTrack application...\n\n", flush=True)

def print_secondary_welcome():
    
    secondary_message = r"""
    
         --------------------------------------------------
        |        ✨ BioVision is Starting! ✨         |
        --------------------------------------------------
    
"""
    print(Fore.GREEN + Style.BRIGHT + secondary_message, flush=True)

    time.sleep(0.5)

print_secondary_welcome()


def print_3rd_welcome():

    secondary_message = r"""
    
       Don’t worry, I’m just negotiating with the server.

  +-------------+                     ___        |      |      |    
  |             |                     \ /]       |      |      |    
  |             |        _           _(_)        |      |      |    
  |             |     ___))         [  | \___    |      |      |    
  |             |     ) //o          | |     \   |      |      |    
  |             |  _ (_    >         | |      ]  |      |      |    
  |          __ | (O)  \__<          | | ____/   '------'------'    
  |         /  o| [/] /   \)        [__|/_                          
  |             | [\]|  ( \         __/___\_____                    
  |             | [/]|   \ \__  ___|            |                   
  |             | [\]|    \___E/%%/|____________|_____              
  |             | [/]|=====__   (_____________________)             
  |             | [\] \_____ \    |                  |              
  |             | [/========\ |   |                  |              
  |             | [\]     []| |   |                  |              
  |             | [/]     []| |_  |                  |              
  |             | [\]     []|___) |                  |    Odeh et al         
====================================================================
    
"""
    print(Fore.GREEN + Style.BRIGHT + secondary_message, flush=True)
   
    time.sleep(0.5)

print_3rd_welcome()


#%%

class ToolTip:
   
    """Tooltip for UI elements."""
    
    def __init__(self, widget, text):
      
        self.widget = widget
       
        self.text = text
        
        self.tip_window = None
        
        self.widget.bind("<Enter>", self.show_tip)
        
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        
        if self.tip_window or not self.text:
        
            return
        
        # Get widget position
        x = self.widget.winfo_rootx() + self.widget.winfo_width() // 2
       
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        
        # Create tooltip window
        self.tip_window = tw = tk.Toplevel(self.widget)
        
        tw.wm_overrideredirect(True)
        
        tw.wm_geometry(f"+{x}+{y}")
        
        # Create tooltip content with larger font
        label = tk.Label(
        
            tw,
            
            text=self.text,
            
            justify="left",
            
            background="#333333",
            
            foreground="white",
            
            relief="solid",
            
            borderwidth=1,
            
            font=("Segoe UI", 12),  
            
            padx=15,             
            
            pady=8
        )
        
        label.pack()

    def hide_tip(self, event=None):
        
        if self.tip_window:
          
            self.tip_window.destroy()
            
            self.tip_window = None

class BioVisionApp(tk.Tk):
    
    """Main Application combining segmentation and classification."""
   
    def __init__(self):
       
        super().__init__()
        
        self.state('zoomed') 
       
        self.title("BioVision AI Platform")
        
        # Set DPI awareness for better resolution (Windows)
        try:
           
            from ctypes import windll
            
            windll.shcore.SetProcessDpiAwareness(1)
        
        except:
           
            pass
            
        
        # Set background and configure grid weights
        self.configure(bg="#f5f5f5")  # Slightly lighter background for better contrast
       
        self.grid_columnconfigure(0, weight=1)
        
        self.grid_rowconfigure(0, weight=1)

        # Apply a theme
        style = ttk.Style()
        
        try:
        
            style.theme_use("clam")  # You can try different themes: clam, alt, default, classic
        
        except:
        
            pass

        # Configure styles with much larger fonts
        style.configure("TButton", font=("Segoe UI", 13))  # Increased button font
        
        style.configure("TLabelframe", font=("Segoe UI", 14))  # Increased label frame font
        
        style.configure("TLabelframe.Label", font=("Segoe UI", 14, "bold"))  # Increased label frame title font
        
        style.configure("TNotebook", font=("Segoe UI", 13))  # Tab font
        
        style.configure("TNotebook.Tab", font=("Segoe UI", 13, "bold"), padding=[15, 8])  # Tab padding and font
        
        # Custom progress bar styles with increased thickness
        style.configure("TProgressbar", thickness=25)  # Thicker progress bar
        
        style.configure("green.Horizontal.TProgressbar", background='#4CAF50', thickness=25)  # Green progress bar
        
        style.configure("processing.Horizontal.TProgressbar", background='#2196F3', thickness=25)  # Blue for processing
        
        style.configure("complete.Horizontal.TProgressbar", background='#4CAF50', thickness=25)  # Green for completion
        
        # Title Frame
        title_frame = ttk.Frame(self)
        
        title_frame.grid(row=0, column=0, sticky="ew", pady=(20, 0))
        
        title_frame.grid_columnconfigure(0, weight=1)
        
        # Title Label with a larger font
        title_label = ttk.Label(
        
            title_frame, 
            
            text="BioVision AI Platform", 
            
            font=("Segoe UI", 36, "bold"),  # Even larger font
            
            foreground="#2c3e50"
        )
        
        title_label.grid(row=0, column=0, pady=10)
        
        # Subtitle
        subtitle_label = ttk.Label(
        
            title_frame, 
            
            text="Advanced Image Analysis for Medical Research", 
            
            font=("Segoe UI", 16),
            
            foreground="#7f8c8d"
        )
        
        subtitle_label.grid(row=1, column=0, pady=(0, 20))
        
        # Create the notebook (tabbed interface)
        self.notebook = ttk.Notebook(self)
        
        self.notebook.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        
        self.grid_rowconfigure(1, weight=1)
        
        # Create tab frames
        self.segmentation_frame = ttk.Frame(self.notebook, padding="20 20 20 20")
        
        self.classification_frame = ttk.Frame(self.notebook, padding="20 20 20 20")
        
        # Add tabs to notebook
        self.notebook.add(self.segmentation_frame, text="Instance Segmentation")
        
        self.notebook.add(self.classification_frame, text="Classification")
        
        # Initialize both applications within the tabs
        self.initialize_segmentation_tab()
        
        self.initialize_classification_tab()
        
        # Status bar at the bottom
        status_frame = ttk.Frame(self)
        
        status_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 10))
        
        status_frame.grid_columnconfigure(0, weight=1)
        
        # Status info
        self.status_label = ttk.Label(
        
            status_frame, 
            
            text="Ready", 
            
            font=("Segoe UI", 12),  # Larger font
            
            foreground="#777777"
        )
        
        self.status_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        # Version info on the right
       
        version_label = ttk.Label(
        
            status_frame, 
            
            text="v1.0.0", 
            
            font=("Segoe UI", 12),  
            
            foreground="#777777"
        )
        
        version_label.grid(row=0, column=1, sticky="e", padx=5, pady=5)
        
        # Set up binding for tab changes
        
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

    def on_tab_change(self, event):
        
        """Handle tab changes."""
        
        tab_id = self.notebook.select()
        
        tab_name = self.notebook.tab(tab_id, "text")
        
        self.status_label.config(text=f"Active: {tab_name}")

    def initialize_segmentation_tab(self):
        
        """Initialize the segmentation tab with all required widgets."""
        
        # Configure proper weights for the segmentation frame
        
        self.segmentation_frame.grid_columnconfigure(0, weight=1)
        
        self.segmentation_frame.grid_rowconfigure(3, weight=1)
        
        # Variables for paths
        
        self.seg_yolo_model_path = None
        
        self.seg_sam_model_path = None
        
        self.seg_image_folder = None
        
        self.seg_output_dir = None
        
        self.seg_global_excel_data = []  # Store results for Excel
        
        # Create a frame for selection buttons with better layout
        
        seg_selection_frame = ttk.LabelFrame(self.segmentation_frame, text="Configuration", padding=(20, 15))
        
        seg_selection_frame.grid(row=0, column=0, sticky="ew", pady=(0, 25))
        
        # Configure columns for better distribution
       
        seg_selection_frame.grid_columnconfigure(0, weight=1)
        
        seg_selection_frame.grid_columnconfigure(1, weight=1)
        
        seg_selection_frame.grid_columnconfigure(2, weight=1)
        
        seg_selection_frame.grid_columnconfigure(3, weight=1)
        
        # Buttons for file/folder selection with increased width and height
        
        btn_width = 20  # Width to accommodate text
        
        # Row 0: Buttons
        seg_btn_yolo = ttk.Button(
        
            seg_selection_frame, 
            
            text="Select YOLO Model", 
            
            command=self.seg_select_yolo_model, 
            
            width=btn_width
        )
        
        seg_btn_yolo.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        ToolTip(seg_btn_yolo, "Select the YOLO model file (.pt) for object detection.")

        seg_btn_sam = ttk.Button(
        
            seg_selection_frame, 
            
            text="Select SAM Model", 
            
            command=self.seg_select_sam_model, 
            
            width=btn_width
        )
        
        seg_btn_sam.grid(row=0, column=1, padx=20, pady=20, sticky="w")
        
        ToolTip(seg_btn_sam, "Select the SAM model file (.pt) for segmentation.")

        seg_btn_image_folder = ttk.Button(
        
            seg_selection_frame, 
            
            text="Select Image Folder", 
            
            command=self.seg_select_image_folder, 
            
            width=btn_width
        )
        
        seg_btn_image_folder.grid(row=0, column=2, padx=20, pady=20, sticky="w")
        
        ToolTip(seg_btn_image_folder, "Select the folder containing the images to process.")

        seg_btn_output_dir = ttk.Button(
        
            seg_selection_frame, 
            
            text="Select Output Directory", 
            
            command=self.seg_select_output_dir, 
            
            width=btn_width
        )
        
        seg_btn_output_dir.grid(row=0, column=3, padx=20, pady=20, sticky="w")
        
        ToolTip(seg_btn_output_dir, "Select the directory where results will be saved.")

        # Row 1: Labels with much larger fonts
        
        self.seg_lbl_yolo = ttk.Label(
        
            seg_selection_frame, 
            
            text="YOLO Model: Not selected", 
            
            font=("Segoe UI", 13),  # Much larger font
            
            foreground="#555555"
        )
        
        self.seg_lbl_yolo.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")

        self.seg_lbl_sam = ttk.Label(
        
            seg_selection_frame, 
            
            text="SAM Model: Not selected", 
            
            font=("Segoe UI", 13),  # Much larger font
            
            foreground="#555555"
        )
        
        self.seg_lbl_sam.grid(row=1, column=1, padx=20, pady=(0, 20), sticky="w")

        self.seg_lbl_image_folder = ttk.Label(
        
            seg_selection_frame, 
            
            text="Image Folder: Not selected", 
            
            font=("Segoe UI", 13),  
            
            foreground="#555555"
        )
        
        self.seg_lbl_image_folder.grid(row=1, column=2, padx=20, pady=(0, 20), sticky="w")

        self.seg_lbl_output_dir = ttk.Label(
        
            seg_selection_frame, 
            
            text="Output Directory: Not selected", 
            
            font=("Segoe UI", 13),  # Much larger font
            
            foreground="#555555"
        )
        
        self.seg_lbl_output_dir.grid(row=1, column=3, padx=20, pady=(0, 20), sticky="w")

        # Progress Frame
        
        seg_progress_frame = ttk.LabelFrame(self.segmentation_frame, text="Progress", padding=(20, 15))
        
        seg_progress_frame.grid(row=1, column=0, sticky="ew", pady=(0, 25))
        
        seg_progress_frame.grid_columnconfigure(0, weight=1)
        
        # Progress bar with increased height
        
        self.seg_progress_bar = ttk.Progressbar(
        
            seg_progress_frame, 
            
            orient="horizontal", 
            
            length=400, 
            
            mode="determinate",
            
            style="green.Horizontal.TProgressbar"
        )
        
        self.seg_progress_bar.grid(row=0, column=0, sticky="ew", padx=20, pady=20)

        self.seg_lbl_progress = ttk.Label(
        
            seg_progress_frame, 
            
            text="Ready to process images", 
            
            font=("Segoe UI", 13),  # Much larger font
            
            foreground="#555555"
        )
        
        self.seg_lbl_progress.grid(row=1, column=0, pady=(0, 15))

        # Results display with better scrollbar integration
        
        seg_results_frame = ttk.LabelFrame(self.segmentation_frame, text="Processing Results", padding=(20, 15))
        
        seg_results_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 25))
        
        seg_results_frame.grid_columnconfigure(0, weight=1)
        
        seg_results_frame.grid_rowconfigure(0, weight=1)
        
        # Create a frame for the text widget and scrollbar
        
        seg_text_frame = ttk.Frame(seg_results_frame)
        
        seg_text_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        seg_text_frame.grid_columnconfigure(0, weight=1)
        
        seg_text_frame.grid_rowconfigure(0, weight=1)
        
        # Text widget with larger font and colors
        
        self.seg_results_text = tk.Text(
        
            seg_text_frame, 
            
            height=12,  
            
            width=80,
            
            font=("Consolas", 14),  
            
            background="#f9f9f9",
            
            foreground="#333333",
            
            borderwidth=1,
            
            relief="solid",
            
            wrap=tk.WORD,  # Wrap by word for better readability
            
            padx=10,      # Add padding within text widget
            
            pady=10
        )
        
        self.seg_results_text.grid(row=0, column=0, sticky="nsew")
        
        # Add scrollbar to the text widget
        
        seg_scrollbar = ttk.Scrollbar(seg_text_frame, command=self.seg_results_text.yview)
        
        seg_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.seg_results_text.config(yscrollcommand=seg_scrollbar.set)

        # Control buttons frame
        
        seg_btn_frame = ttk.Frame(self.segmentation_frame)
        
        seg_btn_frame.grid(row=3, column=0, sticky="ew", pady=(0, 15))
        
        seg_btn_frame.grid_columnconfigure(0, weight=1)
        
        # Process button
        
        self.seg_btn_process = ttk.Button(
        
            seg_btn_frame, 
            
            text="Start Processing", 
            
            command=self.seg_process_images_thread,
            
            style="Process.TButton",
            
            width=25  # Increased width
        )
        
        self.seg_btn_process.grid(row=0, column=0, pady=20)
        
        ToolTip(self.seg_btn_process, "Start processing images with YOLO and SAM.")

        # Initial welcome message with more comprehensive information
        
        self.seg_results_text.tag_configure("title", font=("Consolas", 16, "bold"), foreground="#2c3e50")
        
        self.seg_results_text.tag_configure("subtitle", font=("Consolas", 14, "bold"), foreground="#34495e")
        
        self.seg_results_text.tag_configure("normal", font=("Consolas", 14), foreground="#333333")
        
        self.seg_results_text.tag_configure("highlight", font=("Consolas", 14), foreground="#1976D2")
        
        self.seg_results_text.insert(tk.END, "Welcome to BioVision Segmentation Tool\n\n", "title")
        
        # Add comprehensive welcome message
        
        seg_welcome_text = (
        
            "This tool combines YOLO object detection with SAM (Segment Anything Model) for "
            "advanced medical image segmentation and analysis.\n\n"
            
            "APPLICATIONS:\n"
            "• Medical Imaging: Segment breast cancer cells, brain tumors, and white blood cells\n"
            "• Histopathology: Analyze tissue samples and cell structures\n"
            "• Microscopy: Segment and analyze microscopic structures\n"
            "• Research: Extract region properties for quantitative analysis\n\n"
            
            "HOW TO USE:\n"
            "1. Select your trained YOLO model file (.pt) for object detection\n"
            "2. Select the SAM model file (.pt) for precise segmentation\n"
            "3. Choose a folder containing images to process\n"
            "4. Select where to save the results\n"
            "5. Click 'Start Processing' and wait for results\n\n"
            
            "OUTPUTS:\n"
            "• Detected objects (from YOLO)\n"
            "• Segmentation masks (from SAM)\n"
            "• Isolated objects on black background\n"
            "• Binary masks for further analysis\n"
            "• Excel file with detailed region properties\n\n"
            
            "Please select the required models and folders to begin.\n"
        )
        
        self.seg_results_text.insert(tk.END, seg_welcome_text, "normal")
        
        self.seg_results_text.insert(tk.END, "=" * 40 + "\n", "normal")  # Separator line

    def initialize_classification_tab(self):
        
        """Initialize the classification tab with all required widgets."""
        
        # Configure proper weights for the classification frame
        
        self.classification_frame.grid_columnconfigure(0, weight=1)
        
        self.classification_frame.grid_rowconfigure(3, weight=1)
        
        # Variables for paths
        
        self.cls_yolo_model_path = None
        
        self.cls_image_folder = None
        
        self.cls_output_dir = None
        
        self.cls_all_predictions = []  # Store results for Excel
        
        # Create a frame for selection buttons with better layout
        
        cls_selection_frame = ttk.LabelFrame(self.classification_frame, text="Configuration", padding=(20, 15))
        
        cls_selection_frame.grid(row=0, column=0, sticky="ew", pady=(0, 25))
        
        # Configure columns for better distribution
        
        cls_selection_frame.grid_columnconfigure(0, weight=1)
        
        cls_selection_frame.grid_columnconfigure(1, weight=1)
        
        cls_selection_frame.grid_columnconfigure(2, weight=1)
        
        # Buttons for file/folder selection with increased width and height
        
        btn_width = 22  # Width to accommodate text
        
        # Row 0: Buttons
        
        cls_btn_yolo = ttk.Button(
        
            cls_selection_frame, 
            
            text="Select YOLO Model", 
            
            command=self.cls_select_yolo_model, 
            
            width=btn_width
        )
        
        cls_btn_yolo.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        ToolTip(cls_btn_yolo, "Select the YOLO model file (.pt) for classification.")

        cls_btn_image_folder = ttk.Button(
        
            cls_selection_frame, 
            
            text="Select Image Folder", 
            
            command=self.cls_select_image_folder, 
            
            width=btn_width
        )
        
        cls_btn_image_folder.grid(row=0, column=1, padx=20, pady=20, sticky="w")
        
        ToolTip(cls_btn_image_folder, "Select the folder containing the images to process.")

        cls_btn_output_dir = ttk.Button(
        
            cls_selection_frame, 
            
            text="Select Output Directory", 
            
            command=self.cls_select_output_dir, 
            
            width=btn_width
        )
        
        cls_btn_output_dir.grid(row=0, column=2, padx=20, pady=20, sticky="w")
        
        ToolTip(cls_btn_output_dir, "Select the directory where results will be saved.")

        # Row 1: Labels with much larger fonts
        
        self.cls_lbl_yolo = ttk.Label(
        
            cls_selection_frame, 
            
            text="YOLO Model: Not selected", 
            
            font=("Segoe UI", 13),  # Much larger font
            
            foreground="#555555"
        )
        
        self.cls_lbl_yolo.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")

        self.cls_lbl_image_folder = ttk.Label(
        
            cls_selection_frame, 
            
            text="Image Folder: Not selected", 
            
            font=("Segoe UI", 13),  # Much larger font
            
            foreground="#555555"
        )
        
        self.cls_lbl_image_folder.grid(row=1, column=1, padx=20, pady=(0, 20), sticky="w")

        self.cls_lbl_output_dir = ttk.Label(
        
            cls_selection_frame, 
            
            text="Output Directory: Not selected", 
            
            font=("Segoe UI", 13),  # Much larger font
            
            foreground="#555555"
        )
        
        self.cls_lbl_output_dir.grid(row=1, column=2, padx=20, pady=(0, 20), sticky="w")

        # Progress Frame
        
        cls_progress_frame = ttk.LabelFrame(self.classification_frame, text="Progress", padding=(20, 15))
        
        cls_progress_frame.grid(row=1, column=0, sticky="ew", pady=(0, 25))
        
        cls_progress_frame.grid_columnconfigure(0, weight=1)
        
        # Progress bar with increased height
        
        self.cls_progress_bar = ttk.Progressbar(
        
            cls_progress_frame, 
            
            orient="horizontal", 
            
            length=400, 
            
            mode="determinate",
            
            style="green.Horizontal.TProgressbar"
        )
        
        self.cls_progress_bar.grid(row=0, column=0, sticky="ew", padx=20, pady=20)

        self.cls_lbl_progress = ttk.Label(
        
            cls_progress_frame, 
            
            text="Ready to process images", 
            
            font=("Segoe UI", 13),  # Much larger font
            
            foreground="#555555"
        )
        
        self.cls_lbl_progress.grid(row=1, column=0, pady=(0, 15))

        # Results display with better scrollbar integration
        
        cls_results_frame = ttk.LabelFrame(self.classification_frame, text="Processing Results", padding=(20, 15))
        
        cls_results_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 25))
        
        cls_results_frame.grid_columnconfigure(0, weight=1)
        
        cls_results_frame.grid_rowconfigure(0, weight=1)
        
        # Create a frame for the text widget and scrollbar
        
        cls_text_frame = ttk.Frame(cls_results_frame)
        
        cls_text_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        cls_text_frame.grid_columnconfigure(0, weight=1)
        
        cls_text_frame.grid_rowconfigure(0, weight=1)
        
        # Text widget with larger font and colors
        
        self.cls_results_text = tk.Text(
        
            cls_text_frame, 
            
            height=12,  # Adjusted height to match larger font
            
            width=80,
            
            font=("Consolas", 14),  # Much larger font
            
            background="#f9f9f9",
            
            foreground="#333333",
            
            borderwidth=1,
            
            relief="solid",
            
            wrap=tk.WORD,  # Wrap by word for better readability
            
            padx=10,      # Add padding within text widget
            
            pady=10
        )
        
        self.cls_results_text.grid(row=0, column=0, sticky="nsew")
        
        # Add scrollbar to the text widget
        
        cls_scrollbar = ttk.Scrollbar(cls_text_frame, command=self.cls_results_text.yview)
        
        cls_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.cls_results_text.config(yscrollcommand=cls_scrollbar.set)

        # Control buttons frame
        
        cls_btn_frame = ttk.Frame(self.classification_frame)
        
        cls_btn_frame.grid(row=3, column=0, sticky="ew", pady=(0, 15))
        
        cls_btn_frame.grid_columnconfigure(0, weight=1)
        
        # Process button
        
        self.cls_btn_process = ttk.Button(
        
            cls_btn_frame, 
            
            text="Start Processing", 
            
            command=self.cls_process_images_thread,
            
            style="Process.TButton",
            
            width=25  # Increased width
        )
        
        self.cls_btn_process.grid(row=0, column=0, pady=20)
        
        ToolTip(self.cls_btn_process, "Start classifying images with YOLO.")

        # Initial welcome message with more comprehensive information
        
        self.cls_results_text.tag_configure("title", font=("Consolas", 16, "bold"), foreground="#2c3e50")
        
        self.cls_results_text.tag_configure("subtitle", font=("Consolas", 14, "bold"), foreground="#34495e")
        
        self.cls_results_text.tag_configure("normal", font=("Consolas", 14), foreground="#333333")
        
        self.cls_results_text.tag_configure("highlight", font=("Consolas", 14), foreground="#1976D2")
        
        self.cls_results_text.insert(tk.END, "Welcome to YOLOv11 Classification Tool\n\n", "title")
        
        # Add comprehensive welcome message
        
        cls_welcome_text = (
        
            "This tool provides an easy-to-use interface for image classification using YOLOv11 model. "
            "It's designed for both non-programming researchers and python-developers.\n\n"
            
            "APPLICATIONS:\n"
            "• Medical Imaging: Classify breast cancer, brain tumors, and white blood cells\n"
            "• Research: Apply to any image classification task without programming knowledge\n"
            "• Development: Platform for testing YOLOv11 classification model\n\n"
            
            "HOW TO USE:\n"
            "1. Select your appropriate trained YOLOv11 model file (best.pt)\n"
            "2. Choose a folder containing images to classify\n"
            "3. Select where to save the results(Output Directory Button)\n"
            "4. Click 'Start Processing' and wait for results\n\n"
            
            "OUTPUTS:\n"
            "• Labeled images with classification results\n"
            "• Excel file with complete analysis\n\n"
            
            "Please select the required files and folders to begin.\n"
        )
        
        self.cls_results_text.insert(tk.END, cls_welcome_text, "normal")
       
        self.cls_results_text.insert(tk.END, "=" * 40 + "\n", "normal")  # Separator line

    # ==== SEGMENTATION TAB METHODS ====
    def seg_select_yolo_model(self):
        
        """Select YOLO model file (.pt) for segmentation."""
        
        self.seg_yolo_model_path = filedialog.askopenfilename(
        
            title="Select YOLO Model for Segmentation",
            
            filetypes=[("YOLO Model Files", "*.pt"), ("All Files", "*.*")]
        )
        
        if self.seg_yolo_model_path:
        
            self.seg_lbl_yolo.config(
            
                text=f"YOLO Model: ✅ {os.path.basename(self.seg_yolo_model_path)}", 
                
                foreground="#4CAF50"  # Green color for selected
            )
            
            self.status_label.config(text=f"YOLO model selected for segmentation: {os.path.basename(self.seg_yolo_model_path)}")
        
        else:
        
            self.seg_lbl_yolo.config(
            
                text="YOLO Model: Not selected",
                
                foreground="#555555"
            )
            
        self.seg_check_all_selected()

    def seg_select_sam_model(self):
       
        """Select SAM model file (.pt)."""
        
        self.seg_sam_model_path = filedialog.askopenfilename(
        
            title="Select SAM Model",
            
            filetypes=[("SAM Model Files", "*.pt"), ("All Files", "*.*")]
        )
        
        if self.seg_sam_model_path:
        
            self.seg_lbl_sam.config(
            
                text=f"SAM Model: ✅ {os.path.basename(self.seg_sam_model_path)}", 
                
                foreground="#4CAF50"  # Green color for selected
            )
            
            self.status_label.config(text=f"SAM model selected: {os.path.basename(self.seg_sam_model_path)}")
        
        else:
        
            self.seg_lbl_sam.config(
            
                text="SAM Model: Not selected",
                
                foreground="#555555"
            )
            
        self.seg_check_all_selected()

    def seg_select_image_folder(self):
        
        """Select folder containing images to process for segmentation."""
        
        self.seg_image_folder = filedialog.askdirectory(title="Select Image Folder for Segmentation")
        
        if self.seg_image_folder:
        
            self.seg_lbl_image_folder.config(
            
                text=f"Image Folder: ✅ {os.path.basename(self.seg_image_folder)}",
                
                foreground="#4CAF50"  # Green color for selected
            )
            
            self.status_label.config(text=f"Image folder selected for segmentation: {os.path.basename(self.seg_image_folder)}")
        
        else:
            
            self.seg_lbl_image_folder.config(
        
                text="Image Folder: Not selected",
                
                foreground="#555555"
            )
            
        self.seg_check_all_selected()

    def seg_select_output_dir(self):
        
        """Select folder to save segmentation results."""
        
        self.seg_output_dir = filedialog.askdirectory(title="Select Output Directory for Segmentation")
        
        if self.seg_output_dir:
        
            self.seg_lbl_output_dir.config(
            
                text=f"Output Directory: ✅ {os.path.basename(self.seg_output_dir)}",
                
                foreground="#4CAF50"  # Green color for selected
            )
            
            self.status_label.config(text=f"Output directory selected for segmentation: {os.path.basename(self.seg_output_dir)}")
        
        else:
        
            self.seg_lbl_output_dir.config(
            
                text="Output Directory: Not selected",
                
                foreground="#555555"
            )
            
        self.seg_check_all_selected()

    def seg_check_all_selected(self):
        
        """Check if all paths are selected for segmentation."""
       
        if all([self.seg_yolo_model_path, self.seg_sam_model_path, self.seg_image_folder, self.seg_output_dir]):
        
            # Change the button style to indicate readiness
            
            style = ttk.Style()
            
            style.configure("Process.TButton", background="#4CAF50", foreground="#FFFFFF")
            
            self.seg_btn_process.config(style="Process.TButton")
        
        else:
            
            # Reset button style
            
            style = ttk.Style()
            
            style.configure("Process.TButton", font=("Segoe UI", 16, "bold"))
            
            self.seg_btn_process.config(style="Process.TButton")

    def seg_process_images_thread(self):
        
        """Start segmentation processing in a thread."""
        
        # Disable the process button while processing
        
        self.seg_btn_process.config(state="disabled")
        
        self.status_label.config(text="Processing images for segmentation...")
        
        # Change progress bar style to show active processing
        
        self.seg_progress_bar.config(style="processing.Horizontal.TProgressbar")
        
        threading.Thread(target=self.seg_process_images).start()

    def seg_log(self, message):
        
        """Log messages to the segmentation results text widget."""
        
        self.seg_results_text.insert(tk.END, message + "\n")
        
        self.seg_results_text.see(tk.END)  # Auto-scroll to the end
        
        print(message)
        
        self.update_idletasks()  # Force update the UI

    def seg_process_images(self):
        
        """Process images using YOLO and SAM for segmentation."""
        
        if not all([self.seg_yolo_model_path, self.seg_sam_model_path, self.seg_image_folder, self.seg_output_dir]):
        
            messagebox.showerror("Error", "Please select YOLO model, SAM model, image folder, and output directory.")
            
            # Re-enable the process button
            
            self.seg_btn_process.config(state="normal")
            
            self.status_label.config(text="Ready")
            
            return

        # Clear results area
        
        self.seg_results_text.delete(1.0, tk.END)
        
        self.seg_global_excel_data = []

        # Load YOLO model
        
        try:
        
            self.seg_log(f"Loading YOLO model from {self.seg_yolo_model_path}...")
            
            yolo_model = YOLO(self.seg_yolo_model_path)
            
            self.seg_log("YOLO model loaded successfully.")
        
        except Exception as e:
        
            self.seg_log(f"Error loading YOLO model: {e}")
            
            messagebox.showerror("Error", f"Failed to load YOLO model: {e}")
            
            # Re-enable the process button
            
            self.seg_btn_process.config(state="normal")
            
            self.seg_progress_bar.config(style="green.Horizontal.TProgressbar")
            
            self.status_label.config(text="Error loading YOLO model")
            
            return

        # Load SAM model
        
        try:
            
            self.seg_log(f"Loading SAM model from {self.seg_sam_model_path}...")
        
            sam_model = SAM(self.seg_sam_model_path)
            
            self.seg_log("SAM model loaded successfully.")
        
        except Exception as e:
        
            self.seg_log(f"Error loading SAM model: {e}")
            
            messagebox.showerror("Error", f"Failed to load SAM model: {e}")
            
            # Re-enable the process button
            
            self.seg_btn_process.config(state="normal")
            
            self.seg_progress_bar.config(style="green.Horizontal.TProgressbar")
            
            self.status_label.config(text="Error loading SAM model")
            
            return

        # Prepare output directories
        
        self.seg_log("Creating output directories...")
        
        detect_dir = os.path.join(self.seg_output_dir, 'detect')
        
        segment_predict_dir = os.path.join(self.seg_output_dir, 'segment', 'predict')
        
        analysis_dir = os.path.join(self.seg_output_dir, 'segmented_images_for_analysis')
        
        binary_masks_dir = os.path.join(self.seg_output_dir, 'binary_masks')

        os.makedirs(detect_dir, exist_ok=True)
        
        os.makedirs(segment_predict_dir, exist_ok=True)
        
        os.makedirs(analysis_dir, exist_ok=True)
        
        os.makedirs(binary_masks_dir, exist_ok=True)
        
        self.seg_log("Output directories created.")

        # Process each image
        
        image_files = [f for f in os.listdir(self.seg_image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tif'))]
        
        if not image_files:
        
            self.seg_log("No images found in the selected folder.")
            
            messagebox.showerror("Error", "No images found in the selected folder.")
            
            # Re-enable the process button
            
            self.seg_btn_process.config(state="normal")
            
            self.seg_progress_bar.config(style="green.Horizontal.TProgressbar")
            
            self.status_label.config(text="No images found")
            
            return

        total_images = len(image_files)
        
        self.seg_log(f"Found {total_images} images to process.")

        # Initialize progress bar to 0
        
        self.seg_progress_bar["value"] = 0
        
        self.seg_lbl_progress.config(text="Processing started...")
        
        self.update_idletasks()

        for idx, image_file in enumerate(image_files):
        
            try:
            
                image_path = os.path.join(self.seg_image_folder, image_file)
                
                original_filename = os.path.splitext(os.path.basename(image_path))[0]

                self.seg_log(f"Processing image {idx+1}/{total_images}: {image_file}")

                # YOLO inference
                
                self.seg_log(f"Running YOLO detection on {image_file}...")
                
                results = yolo_model(image_path, save=True, project=detect_dir, name='', exist_ok=True)
                
                self.seg_log(f"YOLO detection completed for {image_file}")

                for result in results:
                
                    boxes = result.boxes.xyxy
                    
                    try:
                    
                        self.seg_log(f"Running SAM segmentation with {len(boxes)} detected objects...")
                        
                        sam_results = sam_model(result.orig_img, bboxes=boxes)

                        # Save segmented images and masks
                        
                        for i, sam_result in enumerate(sam_results):
                        
                            save_path = os.path.join(segment_predict_dir, f'{original_filename}_mask_{i}.png')
                            
                            sam_result.save(save_path)
                            
                            self.seg_log(f"Saved segmentation mask {i+1} to {save_path}")

                            for mask_index, mask_data in enumerate(sam_result.masks.data):
                            
                                if isinstance(mask_data, torch.Tensor):
                                
                                    mask_data = mask_data.cpu().numpy()

                                mask = mask_data.astype(np.uint8) * 255
                                
                                rgb_image = cv2.cvtColor(result.orig_img, cv2.COLOR_BGR2RGB)
                                
                                black_background = np.zeros_like(rgb_image)
                                
                                black_background[mask > 0] = rgb_image[mask > 0]

                                analysis_path = os.path.join(
                                
                                    analysis_dir, f'{original_filename}_analysis_{i}_mask_{mask_index}.png'
                                )
                                
                                cv2.imwrite(analysis_path, cv2.cvtColor(black_background, cv2.COLOR_RGB2BGR))
                                
                                self.seg_log(f"Saved segmented image for analysis: {os.path.basename(analysis_path)}")

                                binary_mask_path = os.path.join(
                                
                                    binary_masks_dir, f'{original_filename}_binary_mask_{i}_mask_{mask_index}.png'
                                )
                                
                                cv2.imwrite(binary_mask_path, mask)
                                
                                self.seg_log(f"Saved binary mask: {os.path.basename(binary_mask_path)}")

                                # Calculate region properties
                                
                                self.seg_log("Calculating region properties...")
                                
                                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                                
                                if contours:
                                
                                    cnt = contours[0]
                                    
                                    area = cv2.contourArea(cnt)
                                    
                                    M = cv2.moments(cnt)
                                    
                                    if M["m00"] != 0:
                                    
                                        cx = int(M["m10"] / M["m00"])
                                        
                                        cy = int(M["m01"] / M["m00"])
                                        
                                        centroid = (cx, cy)
                                    
                                    else:
                                        
                                        centroid = (0, 0)

                                    if len(cnt) >= 5:
                                    
                                        ellipse = cv2.fitEllipse(cnt)
                                        
                                        orientation = ellipse[2]
                                        
                                        axis_major_length = max(ellipse[1])
                                        
                                        axis_minor_length = min(ellipse[1])
                                        
                                        eccentricity = np.sqrt(1 - (axis_minor_length / axis_major_length) ** 2)
                                    
                                    else:
                                    
                                        orientation = 0
                                        
                                        axis_major_length = 0
                                        
                                        axis_minor_length = 0
                                        
                                        eccentricity = 0

                                    equivalent_diameter = np.sqrt(4 * area / np.pi)
                                    
                                    solidity = area / cv2.contourArea(cv2.convexHull(cnt))
                                    
                                    x, y, w, h = cv2.boundingRect(cnt)
                                    
                                    extent = area / (w * h)

                                    self.seg_global_excel_data.append({
                                    
                                        'Image Name': f'{original_filename}_analysis_{i}_mask_{mask_index}.png',
                                        
                                        'Area': area,
                                        
                                        'Centroid': centroid,
                                        
                                        'Orientation': orientation,
                                        
                                        'Axis Major Length': axis_major_length,
                                        
                                        'Axis Minor Length': axis_minor_length,
                                        
                                        'Eccentricity': eccentricity,
                                        
                                        'Equivalent Diameter': equivalent_diameter,
                                        
                                        'Solidity': solidity,
                                        
                                        'Extent': extent,
                                    })
                                    
                                    self.seg_log(f"Region properties calculated. Area: {area:.2f}, "
                                                 
                                             f"Centroid: {centroid}, Ecc: {eccentricity:.4f}")

                    except Exception as e:
                        
                        self.seg_log(f"Error running SAM on {image_file}: {e}")
                        
                        continue

                self.seg_log(f"Completed processing image: {image_file}")
                
                self.seg_log("-" * 30)

            except Exception as e:
               
                self.seg_log(f"Error processing {image_file}: {e}")
                
                self.seg_log("-" * 30)
                
                continue
            
            finally:
            
                # Update progress bar and label
                
                percentage = int(((idx + 1) / total_images) * 100)
                
                self.seg_progress_bar["value"] = percentage
                
                self.seg_lbl_progress.config(text=f"Processing {idx + 1}/{total_images} ({percentage}%)")
                
                self.status_label.config(text=f"Segmentation: Processing {idx + 1}/{total_images}")
                
                self.update_idletasks()

        # Change progress bar style to show completion
        
        self.seg_progress_bar.config(style="complete.Horizontal.TProgressbar")

        # Save Excel summary
        
        if self.seg_global_excel_data:
        
            self.seg_log("\nSaving results to Excel...")
            
            df = pd.DataFrame(self.seg_global_excel_data)
            
            excel_file = os.path.join(binary_masks_dir, 'Summary_analysis_all_images.xlsx')
            
            df.to_excel(excel_file, index=False)
            
            self.seg_log(f"Excel file saved at: {excel_file}")
            
            messagebox.showinfo("Success", f"Processing completed! Excel file saved at:\n{excel_file}")
        
        else:
        
            self.seg_log("\nNo data to save in Excel file.")
            
            messagebox.showinfo("Info", "No data to save in Excel file.")

        self.seg_lbl_progress.config(text="Processing completed!")
        
        self.status_label.config(text="Segmentation processing completed")
        
        # Re-enable the process button
        
        self.seg_btn_process.config(state="normal")

    # ==== CLASSIFICATION TAB METHODS ====
    
    def cls_select_yolo_model(self):
    
        """Select YOLO model file (.pt) for classification."""
        
        self.cls_yolo_model_path = filedialog.askopenfilename(
        
            title="Select YOLO Model for Classification",
            
            filetypes=[("YOLO Model Files", "*.pt"), ("All Files", "*.*")]
        )
        
        if self.cls_yolo_model_path:
        
            self.cls_lbl_yolo.config(
            
                text=f"YOLO Model: ✅ {os.path.basename(self.cls_yolo_model_path)}", 
                
                foreground="#4CAF50"  # Green color for selected
            )
            
            self.status_label.config(text=f"YOLO model selected for classification: {os.path.basename(self.cls_yolo_model_path)}")
        
        else:
        
            self.cls_lbl_yolo.config(
            
                text="YOLO Model: Not selected",
                
                foreground="#555555"
            )
            
        self.cls_check_all_selected()

    def cls_select_image_folder(self):
        
        """Select folder containing images to process for classification."""
        
        self.cls_image_folder = filedialog.askdirectory(title="Select Image Folder for Classification")
        
        if self.cls_image_folder:
        
            self.cls_lbl_image_folder.config(
            
                text=f"Image Folder: ✅ {os.path.basename(self.cls_image_folder)}",
                
                foreground="#4CAF50"  # Green color for selected
            )
            
            self.status_label.config(text=f"Image folder selected for classification: {os.path.basename(self.cls_image_folder)}")
        
        else:
            
            self.cls_lbl_image_folder.config(
            
                text="Image Folder: Not selected",
                
                foreground="#555555"
            )
            
        self.cls_check_all_selected()

    def cls_select_output_dir(self):
        
        """Select folder to save classification results."""
        
        self.cls_output_dir = filedialog.askdirectory(title="Select Output Directory for Classification")
        
        if self.cls_output_dir:
        
            self.cls_lbl_output_dir.config(
            
                text=f"Output Directory: ✅ {os.path.basename(self.cls_output_dir)}",
                
                foreground="#4CAF50"  # Green color for selected
            )
            
            self.status_label.config(text=f"Output directory selected for classification: {os.path.basename(self.cls_output_dir)}")
        
        else:
        
            self.cls_lbl_output_dir.config(
            
                text="Output Directory: Not selected",
                
                foreground="#555555"
            )
            
        self.cls_check_all_selected()

    def cls_check_all_selected(self):
        
        """Check if all paths are selected for classification."""
        
        if all([self.cls_yolo_model_path, self.cls_image_folder, self.cls_output_dir]):
        
            # Change the button style to indicate readiness
            
            style = ttk.Style()
            
            style.configure("Process.TButton", background="#4CAF50", foreground="#FFFFFF")
            
            self.cls_btn_process.config(style="Process.TButton")
        
        else:
        
            # Reset button style
            
            style = ttk.Style()
            
            style.configure("Process.TButton", font=("Segoe UI", 16, "bold"))
            
            self.cls_btn_process.config(style="Process.TButton")

    def cls_process_images_thread(self):
        
        """Start classification processing in a thread."""
        
        # Disable the process button while processing
        
        self.cls_btn_process.config(state="disabled")
        
        self.status_label.config(text="Processing images for classification...")
        
        # Change progress bar style to show active processing
        
        self.cls_progress_bar.config(style="processing.Horizontal.TProgressbar")
        
        threading.Thread(target=self.cls_process_images).start()

    def cls_log(self, message):
        
        """Log messages to the classification results text widget."""
        
        self.cls_results_text.insert(tk.END, message + "\n")
        
        self.cls_results_text.see(tk.END)  # Auto-scroll to the end
        
        print(message)
        
        self.update_idletasks()  # Force update the UI

    def cls_process_images(self):
        
        """Process images using YOLO for classification."""
        
        if not all([self.cls_yolo_model_path, self.cls_image_folder, self.cls_output_dir]):
        
            messagebox.showerror("Error", "Please select YOLO model, image folder, and output directory.")
            
            # Re-enable the process button
            self.cls_btn_process.config(state="normal")
            
            self.status_label.config(text="Ready")
            
            return

        # Clear previous results
        
        self.cls_results_text.delete(1.0, tk.END)
        
        self.cls_all_predictions = []

        # Define the output folder for all predictions
        
        output_root_folder = os.path.join(self.cls_output_dir, 'predictions')
        
        os.makedirs(output_root_folder, exist_ok=True)

        # Load YOLO model
        
        try:
        
            self.cls_log(f"Loading YOLO model from {self.cls_yolo_model_path}...")
            
            model = YOLO(self.cls_yolo_model_path)
            
            self.cls_log("YOLO model loaded successfully.")
            
        except Exception as e:
            
            self.cls_log(f"Error loading YOLO model: {e}")
            
            messagebox.showerror("Error", f"Failed to load YOLO model: {e}")
            
            # Re-enable the process button
            
            self.cls_btn_process.config(state="normal")
            
            # Reset progress bar style
            
            self.cls_progress_bar.config(style="green.Horizontal.TProgressbar")
            
            self.status_label.config(text="Error loading model")
            
            return

        # Get image files
        
        image_files = glob(os.path.join(self.cls_image_folder, '*.jpg')) + \
                     glob(os.path.join(self.cls_image_folder, '*.png')) + \
                     glob(os.path.join(self.cls_image_folder, '*.jpeg')) + \
                     glob(os.path.join(self.cls_image_folder, '*.tif')) + \
                     glob(os.path.join(self.cls_image_folder, '*.tiff'))
        
        if not image_files:
            
            self.cls_log("No images found in the selected folder.")
            
            messagebox.showerror("Error", "No images found in the selected folder.")
            
            # Re-enable the process button
            
            self.cls_btn_process.config(state="normal")
            
            # Reset progress bar style
            
            self.cls_progress_bar.config(style="green.Horizontal.TProgressbar")
            
            self.status_label.config(text="No images found")
            
            return

        total_images = len(image_files)
        
        self.cls_log(f"Found {total_images} images to process.")

        # Initialize progress bar
        
        self.cls_progress_bar["value"] = 0
        
        self.cls_lbl_progress.config(text="Processing started...")
        
        self.update_idletasks()

        # Process each image
        
        for idx, image_path in enumerate(image_files):
        
            try:
            
                self.cls_log(f"Processing image {idx+1}/{total_images}: {os.path.basename(image_path)}")
                
                # Perform inference
                
                results = model(image_path)
                
                result = results[0]
                
                # Access the Probs object
                
                probs = result.probs
                
                # Get the index of the class with the highest probability
                
                top_class_index = probs.top1
                
                predicted_class_name = model.names[top_class_index]
                
                confidence = probs.top1conf.item()
                
                self.cls_log(f"Predicted class: {predicted_class_name}")
                
                self.cls_log(f"Confidence: {confidence:.4f}")
                
                self.cls_log("-" * 30)
                
                # Save the predicted image
                
                try:
                
                    image = Image.open(image_path).convert("RGB")
                    
                    draw = ImageDraw.Draw(image)
                    
                    try:
                    
                        font = ImageFont.truetype("arial.ttf", 24)  # Larger font for image labels
                    
                    except IOError:
                    
                        font = ImageFont.load_default()
                    
                    text = f"Predicted: {predicted_class_name}\nConfidence: {confidence:.2f}"
                    
                    text_color = (255, 0, 0)  # Red color
                    
                    text_position = (15, 15)  # Slightly offset from edge
                    
                    # Add shadow effect for better visibility
                    
                    shadow_color = (0, 0, 0)
                    
                    draw.text((text_position[0]+2, text_position[1]+2), text, fill=shadow_color, font=font)
                    
                    draw.text(text_position, text, fill=text_color, font=font)
                    
                    # Save the predicted image to the output folder
                    
                    image_file_name_without_extension = os.path.splitext(os.path.basename(image_path))[0]
                    
                    output_image_path = os.path.join(output_root_folder, f"{image_file_name_without_extension}_predicted.jpg")
                    
                    image.save(output_image_path)
                    
                    self.cls_log(f"Predicted image saved to: {output_image_path}")
                
                except Exception as e:
                    
                    self.cls_log(f"Error saving predicted image {os.path.basename(image_path)}: {e}")
                
                # Store the prediction information
                
                self.cls_all_predictions.append({
                
                    'Image Name': os.path.basename(image_path),
                    
                    'Predicted Class': predicted_class_name,
                    
                    'Confidence': confidence
                })
                
                
            except FileNotFoundError:
                
                self.cls_log(f"Error: Image not found at {image_path}")
                
            except Exception as e:
                
                self.cls_log(f"An error occurred while processing {os.path.basename(image_path)}: {e}")
                
            finally:
                
                self.cls_log("-" * 30)  # Reduced separator length for larger font
                
                # Update progress bar
                
                percentage = int(((idx + 1) / total_images) * 100)
                
                self.cls_progress_bar["value"] = percentage
                
                self.cls_lbl_progress.config(text=f"Processing {idx + 1}/{total_images} ({percentage}%)")
                
                self.status_label.config(text=f"Classification: Processing {idx + 1}/{total_images}")
                
                self.update_idletasks()

        # Change progress bar style to show completion
        
        self.cls_progress_bar.config(style="complete.Horizontal.TProgressbar")

        # Save all predictions to a single Excel file
        
        if self.cls_all_predictions:
           
            df = pd.DataFrame(self.cls_all_predictions)
        
            excel_file_path = os.path.join(output_root_folder, "all_predictions.xlsx")
            
            df.to_excel(excel_file_path, index=False)
            
            self.cls_log(f"\nAll predictions saved to Excel: {excel_file_path}")
            
            messagebox.showinfo("Success", f"Processing completed! Excel file saved at:\n{excel_file_path}")
        
        else:
            
            self.cls_log("\nNo images were processed, so no Excel file was created.")
        
            messagebox.showinfo("Info", "No images were processed, so no Excel file was created.")

        self.cls_lbl_progress.config(text="Processing completed!")
        
        self.status_label.config(text="Classification processing completed")
        
        # Re-enable the process button
    
        self.cls_btn_process.config(state="normal")

if __name__ == "__main__":
    
    app = BioVisionApp()
    
    app.mainloop()