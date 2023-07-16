# Textbased Taskhours View

This tool is a simple web-based display of scheduled and actual daily work hours entered in text format, which are then tabulated.

![](capt.png)

## Features

- Aggregates task times by category, filebase, daily, and monthly.
- Outputs the aggregated data in HTML format.
- Watch mode to continually update the aggregated data as new task times are recorded.

## Prerequisites

- [Git](https://git-scm.com/)
- [Python 3.11](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)

## Installation

Clone the project:

```bash
git clone https://github.com/daiwata/textbased-tasktime-view.git
```

Navigate to the project directory:

```bash
cd textbased-taskhours-viewer
```

Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate
```

Install the requirements:

```bash
pip install -r requirements.txt
```

## Running the App

Navigate to the src directory and execute the main.py file:

```bash
cd src
python main.py
```

## Compile to EXE for Windows

Install additional packages:

```bash
pip install pyinstaller
pip install git+https://github.com/bottlepy/bottle.git
```

Navigate to the app directory and compile the app:

```bash
cd app
pyinstaller -wF --add-data="web/*;web/" main.py --clean --distpath . -n TaskhoursView.exe
```

## Running the EXE (Windows)

Download and decompress this Project from "Code -> Download ZIP"

In explorer, go to the app directory and double click on the "TaskhourView.exe" file.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License, see the LICENSE.txt file for details.
