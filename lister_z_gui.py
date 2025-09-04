import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from docx import Document
import json

def is_hidden_file(entry):
    hidden_names = {"desktop.ini", "thumbs.db", "._.ds_store", ".ds_store", ".gitignore", ".gitkeep"}
    if entry.name.startswith('.') or entry.name.lower() in hidden_names:
        return True
    try:
        import ctypes
        attrs = ctypes.windll.kernel32.GetFileAttributesW(str(entry.path))
        if attrs != -1 and attrs & 2:
            return True
    except Exception:
        pass
    return False

def list_files_and_folders(directory, mode="B", list_option=1, recursive=True, specific_subfolders=None, ignore_hidden=False):
    folder_name = os.path.basename(os.path.normpath(directory))
    disk_letter = os.path.splitdrive(os.path.abspath(directory))[0].replace(":", "")
    output_filename_base = f"{folder_name} ({disk_letter})"
    folders = []
    files = []
    import re
    for entry in os.scandir(directory):
        if ignore_hidden and is_hidden_file(entry):
            continue
        if entry.is_dir():
            if not specific_subfolders:
                folders.append(entry.path)
            else:
                entry_name_clean = re.sub(r'\W+', '', entry.name).lower()
                for sub in specific_subfolders:
                    sub_clean = re.sub(r'\W+', '', sub).lower()
                    if sub_clean == entry_name_clean:
                        folders.append(entry.path)
                        break
        elif entry.is_file():
            files.append(entry.path)
    def get_all_sub_files(folder):
        sub_files = []
        if not specific_subfolders:
            for root, _, file_list in os.walk(folder):
                for f in file_list:
                    sub_files.append(os.path.join(root, f))
        else:
            for entry in os.scandir(folder):
                if entry.is_file():
                    sub_files.append(entry.path)
        return sub_files
    sub_files_map = {}
    if recursive:
        for folder in folders:
            sub_files_map[folder] = get_all_sub_files(folder)
    output_file_path = os.path.join(directory, f"{output_filename_base}.{'docx' if mode.upper() == 'A' else ('json' if mode.upper() == 'C' else 'txt')}")
    if mode.upper() == "A":
        try:
            doc = Document()
            doc.add_heading(f"{folder_name}", level=1)
            if list_option in [1, 2]:
                for folder in folders:
                    write_folder_structure_docx(doc, folder, list_option=list_option)
            if list_option == 1:
                for file in files:
                    p = doc.add_paragraph()
                    p.add_run("• ")
                    base, ext = os.path.splitext(os.path.basename(file))
                    run = p.add_run(base)
                    run.bold = True
                    p.add_run(ext)
            credits_p = doc.add_paragraph()
            credits_run = credits_p.add_run("Credits: User Lum-10 from GitHub and AI tools")
            credits_run.font.size = 127000
            doc.save(output_file_path)
            messagebox.showinfo("Success", f"List generated successfully: {output_file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"DOCX generation failed: {e}")
    elif mode.upper() == "C":
        def folder_to_dict(folder):
            d = {"folder": os.path.basename(folder), "files": [], "subfolders": []}
            for entry in os.scandir(folder):
                if entry.is_file():
                    d["files"].append(entry.name)
                elif entry.is_dir():
                    d["subfolders"].append(folder_to_dict(entry.path))
            return d
        db = {"root": folder_name, "files": [os.path.basename(f) for f in files] if list_option in [1, 3] else [], "folders": []}
        for folder in folders:
            db["folders"].append(folder_to_dict(folder))
        with open(output_file_path, "w", encoding="utf-8") as json_file:
            json.dump(db, json_file, indent=2)
            json_file.write("\n/* Credits: User Lum-10 from GitHub and AI tools */\n")
        messagebox.showinfo("Success", f"JSON database exported: {output_file_path}")
    else:
        with open(output_file_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(f"{folder_name}\n\n")
            if list_option in [1, 2]:
                for folder in folders:
                    write_folder_structure_txt(txt_file, folder, list_option=list_option)
            if list_option == 1 or list_option == 3:
                if list_option == 1:
                    for file in files:
                        base, ext = os.path.splitext(os.path.basename(file))
                        txt_file.write(f"• {base}{ext}\n")
                elif list_option == 3:
                    for file in files:
                        base, ext = os.path.splitext(os.path.basename(file))
                        txt_file.write(f"• {base}{ext}\n")
            txt_file.write("\n\nCredits: User Lum-10 from GitHub and AI tools\n")
        messagebox.showinfo("Success", f"List generated successfully: {output_file_path}")

def write_folder_structure_docx(doc, folder, indent=0, list_option=1):
    p = doc.add_paragraph("    " * indent)
    p.add_run("• ")
    run = p.add_run(os.path.basename(folder))
    run.bold = True
    entries = sorted(os.scandir(folder), key=lambda e: (not e.is_dir(), e.name.lower()))
    subfolder_count = 0
    subfile_count = 0
    import inspect
    specific_subfolders = inspect.currentframe().f_back.f_locals.get('specific_subfolders', None)
    for entry in entries:
        if entry.is_dir():
            if not specific_subfolders:
                subfolder_count += 1
                write_folder_structure_docx(doc, entry.path, indent + 1, list_option)
        elif entry.is_file() and list_option == 1:
            subfile_count += 1
            sub_p = doc.add_paragraph("    " * (indent + 1) + f"{subfile_count}. ")
            base, ext = os.path.splitext(entry.name)
            sub_run = sub_p.add_run(base)
            sub_run.italic = True
            sub_p.add_run(ext)

def write_folder_structure_txt(txt_file, folder, indent=0, list_option=1):
    txt_file.write(f"{'    ' * indent}• {os.path.basename(folder)}\n")
    entries = sorted(os.scandir(folder), key=lambda e: (not e.is_dir(), e.name.lower()))
    subfolder_count = 0
    subfile_count = 0
    import inspect
    specific_subfolders = inspect.currentframe().f_back.f_locals.get('specific_subfolders', None)
    for entry in entries:
        if entry.is_dir():
            if not specific_subfolders:
                subfolder_count += 1
                write_folder_structure_txt(txt_file, entry.path, indent + 1, list_option)
        elif entry.is_file() and list_option == 1:
            subfile_count += 1
            base, ext = os.path.splitext(entry.name)
            txt_file.write(f"{'    ' * (indent + 1)}{subfile_count}. {base}{ext}\n")

def run_gui():
    root = tk.Tk()
    root.title("Files & Folders Lister Z")
    root.geometry("500x400")
    def select_directory():
        return filedialog.askdirectory()
    def run_lister():
        directory = select_directory()
        if not directory:
            return
        if not os.path.isdir(directory):
            messagebox.showerror("Error", f"The directory '{directory}' does not exist.")
            return
        mode = simpledialog.askstring("Mode", "Do you want to generate the output as DOCX (A), TXT (B), or JSON (C)?").strip().lower()
        if mode in ["a", "docx"]:
            mode = "A"
        elif mode in ["b", "txt"]:
            mode = "B"
        elif mode in ["c", "json"]:
            mode = "C"
        else:
            messagebox.showerror("Error", "Invalid input. Please enter DOCX/A or TXT/B, or JSON/C.")
            return
        list_option = simpledialog.askinteger("Listing Option", "Choose listing option:\n1. Both folders and files\n2. Only folders\n3. Only files", minvalue=1, maxvalue=3)
        filter_input = simpledialog.askstring("Filter", "Enter sub-folder names or keywords to filter (comma-separated), or leave blank to include all:")
        if filter_input:
            specific_subfolders = [folder.strip() for folder in filter_input.split(",") if folder.strip()]
        else:
            specific_subfolders = None
        hide_hidden_input = messagebox.askyesno("Hide Hidden Files", "Do you want to hide hidden files such as desktop.ini?")
        list_files_and_folders(directory, mode=mode, list_option=list_option, recursive=True, specific_subfolders=specific_subfolders, ignore_hidden=hide_hidden_input)
    tk.Button(root, text="Run Files & Folders Lister", command=run_lister, height=2, width=30).pack(pady=40)
    tk.Label(root, text="Credits: user Lum-10 from GitHub and AI tools", font=("Arial", 8)).pack(side="bottom", pady=10)
    root.mainloop()

if __name__ == "__main__":
    run_gui()
