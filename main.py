import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from utils import process_csv

df = None


# Modify the upload_file function to show/hide the spinner
def upload_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )
    if file_path:
        try:
            global df
            df = pd.read_csv(file_path)
            df = process_csv(df)
            messagebox.showinfo("Success", "File processed successfully!")
            frame.focus_set()
            download_button.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process file: {e}")


# Modify the download_file function to show/hide the spinner
def download_file():
    save_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
    )
    if save_path:
        try:
            global df
            df.to_csv(save_path, index=False)
            messagebox.showinfo("Success", f"File saved as {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")


# Create the main application window
root = tk.Tk()
root.title("CSV File Processor")
root.geometry("400x200")


# Create a frame for better layout management
frame = tk.Frame(root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# Create and place the upload button
upload_button = tk.Button(
    frame,
    text="Upload CSV File",
    command=upload_file,
    padx=10,
    pady=5,
)
upload_button.pack(pady=10)

# Create and place the download button (initially disabled)
download_button = tk.Button(
    frame,
    text="Download Processed CSV",
    command=download_file,
    state=tk.DISABLED,
    padx=10,
    pady=5,
)
download_button.pack(pady=10)


# Run the application
root.mainloop()
