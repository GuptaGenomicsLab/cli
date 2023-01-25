import tkinter as tk
from tkinter import filedialog
import os

try:
    from tool import bulk_rename
except ModuleNotFoundError:
    from scripts.bulk_rename.tool import bulk_rename

def gui():
    window = tk.Tk()
    window.title("Gupta Lab Tools - bulk_rename (GUI)")

    input_dir = tk.StringVar(window, value=os.getcwd())
    output_dir = tk.StringVar(window, value=os.getcwd())
    index_file = tk.StringVar(window, value=os.getcwd())
    seqtype = tk.StringVar(window, value="keep")

    tk.Label(window, text="Choose a directory containing files to rename:").pack()
    tk.Entry(window, textvariable=input_dir).pack()
    tk.Button(
        window,
        text="Choose directory",
        command=lambda: input_dir.set(filedialog.askdirectory())
    ).pack()

    tk.Label(window, text="Choose a directory to output renamed files to:").pack()
    tk.Entry(window, textvariable=output_dir).pack()
    tk.Button(
        window,
        text="Choose directory",
        command=lambda: output_dir.set(filedialog.askdirectory())
    ).pack()

    tk.Label(window, text="Choose a txt file containing the index of files to rename, comma separated:").pack()
    tk.Entry(window, textvariable=index_file).pack()
    tk.Button(
        window,
        text="Choose file",
        command=lambda: index_file.set(filedialog.askopenfilename())
    ).pack()

    tk.Label(window, text="Choose the extension for output files:").pack()
    tk.Radiobutton(window, text="faa/fna", variable=seqtype, value="keep").pack()
    tk.Radiobutton(window, text="txt", variable=seqtype, value="txt").pack()
    tk.Radiobutton(window, text="fasta", variable=seqtype, value="fasta").pack()
    def run():
        tk.messagebox.showinfo("Running", "Running bulk_rename...")
        errors = bulk_rename(input_dir.get(), output_dir.get(), index_file.get())
        if len(errors) > 0:
            tk.messagebox.showerror("Completed with Errors", "Completed. Failed to rename:\n" + '\n'.join(errors))
        else:
            tk.messagebox.showinfo("Completed", "Completed. All files were successfully renamed.")
            

    tk.Button(window, text="Run", command=run).pack()


    window.mainloop()

if __name__ == "__main__":
    gui()