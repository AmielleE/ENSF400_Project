import tkinter as tk
from tkinter import filedialog, messagebox

SUPPORTED_EXTENSIONS = (".pdf", ".txt")

class FileUploadUI:
    def __init__(self, root):
        self.root = root
        self.root.title("On My Agenda - Upload Course Outlines")
        self.root.geometry("500x400")

        self.files = []

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self.root, text="Upload Course Outlines", font=("Arial", 16))
        title.pack(pady=10)

        # Upload Button
        upload_btn = tk.Button(self.root, text="Select Files", command=self.select_files)
        upload_btn.pack(pady=5)

        # Listbox to show selected files
        self.file_listbox = tk.Listbox(self.root, width=60, height=10)
        self.file_listbox.pack(pady=10)

        # Remove button
        remove_btn = tk.Button(self.root, text="Remove Selected", command=self.remove_selected)
        remove_btn.pack(pady=5)

        # Process button
        process_btn = tk.Button(self.root, text="Process Files", command=self.process_files)
        process_btn.pack(pady=20)

    def select_files(self):
        selected = filedialog.askopenfilenames(
            title="Select Course Outline Files",
            filetypes=[("Supported Files", "*.pdf *.txt")]
        )

        for file in selected:
            if file.lower().endswith(SUPPORTED_EXTENSIONS):
                if file not in self.files:
                    self.files.append(file)
                    self.file_listbox.insert(tk.END, file)
            else:
                messagebox.showwarning("Invalid File", f"{file} is not a supported format.")

    def remove_selected(self):
        selected_indices = self.file_listbox.curselection()

        for index in reversed(selected_indices):
            self.file_listbox.delete(index)
            del self.files[index]

    def process_files(self):
        if not self.files:
            messagebox.showwarning("No Files", "Please upload at least one file.")
            return

        # Placeholder for backend integration
        messagebox.showinfo("Processing", f"{len(self.files)} file(s) ready for processing.")


if __name__ == "__main__":
    root = tk.Tk()
    app = FileUploadUI(root)
    root.mainloop()