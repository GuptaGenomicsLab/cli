# Gupta CLI Tools (including GUI)
This all in one tool offers several utilies as a command line interface (CLI) or graphical user interface (GUI) for common computational tasks required in the lab.
Several (but not all) of these tools are also available through a graphical user interface.

Technical Note: In a future version, the scripts should be written to optionally accomodate a CLI or GUI interface directly, by removing dependencies on Click for the CLI.

### Usage
The following tools are currently available:
- fetch_prots (GUI, CLI): allows bulk downloading, processing, and renaming of protein or nucleotide sequences from NCBI for a single assembly.
- bulk_rename (GUI, CLI): allows for bulk renaming of genomes files in a directory, including extraction if neccessary.
- appindels query (wip) (CLI only): takes a single genome and runs it against the AppIndels server
    - may have unexpected or less useful result formatting (though data is correct)
- appindels bulk_query (wip) (CLI only): runs a directory of genomes against the AppIndels server
    - parallelization is not yet implemented

To get an idea of the options available, enter `--help` after any typed command
and a menu with all available options will be provided.
Running the GUI should be self explanatory.


## Installation
### Installation -- Packaged Executable (GUI only, CLI work in progress)
This tool is packaged automatically on GitHub Actions and uploaded to the releases page.
If you wish to have a portable, standalone executable, download the latest release from the page.
This is generally untested, and should only work on Windows -- it may have unexpected behaviours due to the nature of packaging Python executables.
Moreover, this may make it more difficult to update, as the executable will need to be replaced with the new version.

### Installation -- From Source
#### Requirements (Only for Source Installation)
- Python 3.10+
- Pipenv -- optional(see Appendix for installation instructions)
- Git (see Appendix for installation instructions)

#### Instructions
Open the Terminal in a folder where you wish to install the tool.
On newer versions, right click the file explorer and "Open in Terminal".
On older versions, copy the file path and type `cd <path>` in the Terminal,
replacing `<path>` with the path you copied.
1. Clone the repository using `git clone https://github.com/GuptaGenomicsLab/cli.git`.
You may be prompted to login to GitHub.
2. Open the Terminal and navigate to the repository directory by typing `cd gupta-cli`.
3. `pip install --editable .` to install dependencies.
    - If you prefer to use Pipenv, `pipenv install --system`.
4. `python cli.py` to test the tool.
    - if you see an error saying "no module found 'colorama'", run `pip install colorama` and try again.
5. Similarly, try to access the tool by typing `gcli`. This should have the same effect as the previous step.

The tool should now be installed and ready to use.
It can now be used as a command line tool.
To run the gui, you should be able to double click `gui.py`.
If this does not work, you can run the gui by typing `python gui.py` in the Terminal.

##### Updates
Simply navigate to the directory in Terminal and type `git pull`.
If dependencies are missing because they were added or removed, rerun step 3.

### Optional - Add to PATH
If you want to be able to access the command line tool from anywhere, you can add the tool to your PATH.
This step is covered in several other guides but I will add an additional guide [here](https://linuxhint.com/add-directory-to-path-environment-variables-windows/).

For Linux:
```bash
export PATH=$PATH:/path/to/gupta-cli
```

## Appendix
### Installing Python, Pipenv, Git
On newer versions of Windows (and all Linux versions),
Python and Git are best installed using a package manager from the Terminal.
Open the Terminal and type `winget` to ensure that the Windows Package Manager is installed.
If it is not, follow the instructions [here](https://docs.microsoft.com/en-us/windows/package-manager/winget/). Alternatively, skip to a manual installation.
If you are using Linux, presumably you know how to work the packager manager so the provided instructions are Windows-specific.

Type into the Terminal:
```bash
winget install Python.Python
winget install Git.Git
```
This will install Python and Git using the Windows Package Manager.

Alternatively, you can install Python and Git **manually**.
Python should be installed from [here](https://www.python.org/downloads/).
Git should be installed from [here](https://git-scm.com/downloads).

Once Python is installed, open the Terminal and type `pip install pipenv`.