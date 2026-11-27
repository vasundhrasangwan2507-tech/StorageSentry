import os
import shutil
import csv
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def run_organizer(target_path, output_widget):
    """
    Executes core file organization and prints output to the GUI text box.
    """
    output_widget.delete(1.0, tk.END)  # Clear previous console output
    
    def log_msg(msg):
        output_widget.insert(tk.END, msg + "\n")
        output_widget.see(tk.END)

    if not target_path or not os.path.exists(target_path):
        messagebox.showerror("Error", f"Invalid path input: '{target_path}' does not exist.")
        return

    # Extension lookup table for automatic routing
    DEFAULT_EXTENSION_MAPPING = {
        # Documents & Office (including Apple iWork)
        ".pdf": "Documents",
        ".doc": "Documents",
        ".docx": "Documents",
        ".txt": "Documents",
        ".rtf": "Documents",
        ".md": "Documents",
        ".csv": "Documents",
        ".xls": "Documents",
        ".xlsx": "Documents",
        ".ppt": "Documents",
        ".pptx": "Documents",
        ".pages": "Documents",
        ".numbers": "Documents",
        ".key": "Documents",

        # Images (including Apple HEIC/HEIF & macOS icons)
        ".jpg": "Images",
        ".jpeg": "Images",
        ".png": "Images",
        ".gif": "Images",
        ".webp": "Images",
        ".heic": "Images",
        ".heif": "Images",
        ".bmp": "Images",
        ".tif": "Images",
        ".tiff": "Images",
        ".svg": "Images",
        ".icns": "Images",
        ".ico": "Images",

        # Videos (including Apple QuickTime & iTunes containers)
        ".mp4": "Videos",
        ".mkv": "Videos",
        ".mov": "Videos",
        ".m4v": "Videos",
        ".avi": "Videos",
        ".webm": "Videos",
        ".flv": "Videos",

        # Audio
        ".mp3": "Audio",
        ".m4a": "Audio",
        ".aac": "Audio",
        ".wav": "Audio",
        ".flac": "Audio",
        ".ogg": "Audio",

        # Archives & Disk Images (including macOS installers & disk images)
        ".zip": "Archives",
        ".rar": "Archives",
        ".7z": "Archives",
        ".tar": "Archives",
        ".gz": "Archives",
        ".dmg": "Archives",
        ".pkg": "Archives",
        ".iso": "Archives",
        ".img": "Archives",

        # macOS Apps, Scripts & System Configs
        ".app": "macOS_Apps",
        ".scpt": "macOS_Scripts",
        ".command": "macOS_Scripts",
        ".sh": "macOS_Scripts",
        ".plist": "macOS_System",

        # Code & Data
        ".py": "Code",
        ".js": "Code",
        ".ts": "Code",
        ".html": "Code",
        ".css": "Code",
        ".c": "Code",
        ".cpp": "Code",
        ".h": "Code",
        ".v": "Code",
        ".sv": "Code",
        ".m": "Code",
        ".json": "Code",
        ".xml": "Code",
        ".yaml": "Code",
        ".yml": "Code",
    }
    extension_mapping = DEFAULT_EXTENSION_MAPPING

    category_bytes = {}
    total_bytes = 0
    log_records = []
    
    csv_filename = 'storagesentry_log.csv'
    file_exists = os.path.exists(csv_filename)

    try:
        with open(csv_filename, mode='a', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            if not file_exists:
                writer.writerow(['Timestamp', 'File Name', 'Category', 'Size (Bytes)'])

            for filename in os.listdir(target_path):
                file_path = os.path.join(target_path, filename)

                if os.path.isdir(file_path):
                    continue

                _, ext = os.path.splitext(filename)
                ext = ext.lower()
                category = extension_mapping.get(ext, 'Others')

                file_size = os.path.getsize(file_path)
                total_bytes += file_size
                category_bytes[category] = category_bytes.get(category, 0) + file_size

                category_dir = os.path.join(target_path, category)
                if not os.path.exists(category_dir):
                    os.makedirs(category_dir)

                destination_path = os.path.join(category_dir, filename)
                shutil.move(file_path, destination_path)

                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                writer.writerow([timestamp, filename, category, file_size])
                log_records.append((filename, category, file_size))

        # Analytics Report Generation
        log_msg("--- STORAGESENTRY v1.0 ANALYTICS REPORT ---")
        if total_bytes == 0:
            log_msg("No files processed or directory is empty.")
            messagebox.showinfo("Info", "Directory is empty or no files were processed.")
            return

        total_mb = total_bytes / (1024 * 1024)
        log_msg(f"Total Storage Processed: {total_mb:.2f} MB\n")

        log_msg("Category Percentage Distribution:")
        for cat, b_count in category_bytes.items():
            share_pct = (b_count / total_bytes) * 100
            log_msg(f" • {cat}: {share_pct:.2f}% ({b_count} bytes)")

        # Rule Alert Engine
        log_msg("\n--- RULE ALERT ENGINE ---")
        oversized_threshold = 50 * 1024 * 1024
        for filename, category, f_size in log_records:
            if f_size > oversized_threshold:
                log_msg(f"[ALERT] Oversized File: '{filename}' in '{category}' ({f_size / (1024*1024):.2f} MB > 50 MB)")

        for cat, b_count in category_bytes.items():
            share_pct = (b_count / total_bytes) * 100
            if share_pct > 50.0:
                log_msg(f"[ALERT] Storage Spike: Category '{cat}' occupies {share_pct:.2f}% of total storage.")

        messagebox.showinfo("Success", "Directory organized and logged successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

# --- GUI Application Window Setup ---
def create_gui():
    root = tk.Tk()
    root.title("StorageSentry v1.0 - Smart File Organizer")
    root.geometry("650x500")
    root.config(bg="#f4f4f9")

    # Header Label
    title_label = tk.Label(root, text="StorageSentry v1.0", font=("Arial", 16, "bold"), bg="#f4f4f9", fg="#333")
    title_label.pack(pady=10)

    # Frame for Directory Selection
    frame_path = tk.Frame(root, bg="#f4f4f9")
    frame_path.pack(pady=5, padx=15, fill=tk.X)

    lbl_path = tk.Label(frame_path, text="Target Folder:", font=("Arial", 10), bg="#f4f4f9")
    lbl_path.pack(side=tk.LEFT, padx=5)

    entry_path = tk.Entry(frame_path, font=("Arial", 10), width=45)
    entry_path.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

    def browse_folder():
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            entry_path.delete(0, tk.END)
            entry_path.insert(0, folder_selected)

    btn_browse = tk.Button(frame_path, text="Browse...", font=("Arial", 10), command=browse_folder, bg="#ddd")
    btn_browse.pack(side=tk.LEFT, padx=5)

    # Action Button
    btn_run = tk.Button(root, text="Run StorageSentry", font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", 
                        command=lambda: run_organizer(entry_path.get(), text_output))
    btn_run.pack(pady=10)

    # Output Console Screen
    lbl_output = tk.Label(root, text="Activity & Analytics Log:", font=("Arial", 10, "bold"), bg="#f4f4f9", fg="#333")
    lbl_output.pack(anchor="w", padx=20)

    text_output = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Consolas", 9), height=18, bg="#ffffff", fg="#222")
    text_output.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)

    root.mainloop()

if __name__ == '__main__':
    create_gui()
