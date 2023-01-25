import tkinter as tk
from tkinter import filedialog
import os

from scripts.fetch_prots.command import fetch_prots

def gui():
    window = tk.Tk()
    window.title("Gupta Lab Tools - fetch_prots (GUI)")

    # choose file
    filepath = tk.StringVar(window, value=os.getcwd())
    tk.Label(window, text="Choose a CSV list of assemblies to download from NCBI:").pack()
    tk.Entry(window, textvariable=filepath).pack()
    tk.Button(
        window,
        text="Choose file",
        command=lambda: filepath.set(filedialog.askopenfilename(filetypes=[("NCBI Index CSV", "*.csv")]))
    ).pack()

    species_name = tk.StringVar(window)
    tk.Label(window, text="Enter the species name to use for naming files:").pack()
    tk.Entry(window, textvariable=species_name).pack()

    # choice between protein and nucleotide
    seqtype = tk.StringVar(window, value="protein")
    tk.Label(window, text="Choose the sequence type to download:").pack()
    tk.Radiobutton(window, text="Protein", variable=seqtype, value="protein").pack()
    tk.Radiobutton(window, text="Nucleotide", variable=seqtype, value="nucleotide").pack()

    # optionals
    skip_statistics = tk.BooleanVar(window, value=False)
    skip_renaming = tk.BooleanVar(window, value=False)
    output_dir = tk.StringVar(window, value=None)
    start_at = tk.IntVar(window, value=0)
    stop_at = tk.IntVar(window, value=None)

    # create frame for optional options
    optional_frame = tk.LabelFrame(window, text="Additional Options")
    tk.Checkbutton(optional_frame, text="Skip statistics", variable=skip_statistics).pack()
    tk.Checkbutton(optional_frame, text="Skip renaming", variable=skip_renaming).pack()
    tk.Label(optional_frame, text="Output directory:").pack()
    tk.Entry(optional_frame, textvariable=output_dir).pack()
    tk.Button(optional_frame, text="Choose directory", command=lambda: output_dir.set(filedialog.askdirectory())).pack()
    tk.Label(optional_frame, text="Start at index:").pack()
    tk.Entry(optional_frame, textvariable=start_at).pack()
    tk.Label(optional_frame, text="Stop at index:").pack()
    tk.Entry(optional_frame, textvariable=stop_at).pack()
    optional_frame.pack()

    def run():
        command = f"python \"{os.path.join(os.getcwd(), 'cli.py')}\" fetch-prots \"{filepath.get()}\" \"{species_name.get()}\" -t {seqtype.get()}"
        if skip_statistics.get():
            command += " --skip-statistics"
        if skip_renaming.get():
            command += " --skip-renaming"
        if output_dir.get():
            command += f" -o {output_dir.get()}"
        if start_at.get() != 0:
            command += f" --start-at {start_at.get()}"
        if stop_at.get() is not None and stop_at.get() != 0:
            command += f" --stop-at {stop_at.get()}"

        print("Starting the CLI fetch_prots tool.")
        print(command)
        os.system(command)
        tk.messagebox.showinfo("Finished", "Finished downloading sequences.")

    tk.Button(window, text="Run", command=run).pack()
    window.mainloop()
