# Textbased Taskhours View

This tool is a simple web-based display of scheduled and actual daily work hours entered in text format, which are then tabulated.

![](capt.png)

## Features

- Aggregates task times by category, filebase, daily, and monthly.
- Outputs the aggregated data in HTML format.
- Watch mode to continually update the aggregated data as new task times are recorded.

## Running the EXE (Windows)

Download and decompress this Project from "Code -> Download ZIP"

In explorer, go to the app directory and double click on the "TaskhourView.exe" file.

## Running in Python

### Prerequisites

- [Git](https://git-scm.com/)
- [Python 3.11](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)

### Installation

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

### Running the App

Navigate to the src directory and execute the main.py file:

```bash
cd src
python main.py
```


## How to edit text files

Prepare text files in the input directory.

### Example 1）

The following represents that the actual work for task 1 was 1 hour on June 1, 2023.

**example1.txt**

```txt
2023/6/1

 **** Task 1
```

- Each `*` counts as 15 minutes (0.25 hours) of actual work.
- Write multiple symbols and then write the task name after leaving a space.

### Example 2）

The following represents that the planned and actual work for task 1 was 1 hour on June 1, 2023.

**example2.txt**

```txt
2023/6/1

 ==== Task 1
 ****
```

- Each `=` counts as 15 minutes (0.25 hours) of planned work.
- For `*` on the next line of `=`, the task name can be omitted.

### Example 3）

The following represents that the planned and actual work for task 1 was 1 hour, the planned work for task 2 was 0.5 hours, and the actual work was 0 hours on June 1, 2023.

**example3.txt**

```txt
2023/6/1

 ===  = Task 1
  ***  *
    == Task 2
```

- You can write multiple tasks as shown above.
- Symbols can be continued in the line by leaving a space.
  (However, if other strings are entered, other strings are aggregated as task names)

### Example 4）

To describe multiple dates, do as follows.

**example4.txt**

```txt
2023/6/2

 === Task 2
 *****

2023/6/1

 ===  = Task 1
  ***  *
    == Task 2
     ** **
```


- In this case, in the monthly and file unit aggregation, task 2 will be planned for 1.25 hours and actual 2.25 hours.

### Example 5）

Having a scale makes it easy to plan and make it clear when and what was done.

**example5.txt**

```txt
2023/6/2
9   10  11  12  13  14  15  16  17  18  19

============    =============== Task 1
************    ***************
                               ===== Task 2
```

The above `9 10 11 12 ... ` rows are not relevant to the tabulation process.

### Example 6）

Categories can be set for planned and actual.
It can be edited in app/setting.json.

**app/setting.json**

```json
[
    { 
        "type": "Customer Business", 
        "sepPlan": "=", 
        "sepDone": "*"
    },
    { 
        "type": "Internal Business", 
        "sepPlan": "-", 
        "sepDone": "+"
    },
    { 
        "type": "Task Category 3", 
        "sepPlan": ">", 
        "sepDone": "@"
    }
]
```

For example, in the following case, it is 1 hour as an internal business.

**example6.txt**

```txt
2023/6/2
9   10  11  12  13  14  15  16  17  18  19
---- Internal Online Meeting
++++
```

### Example 7）

Multiple text files can be placed.
It is easy to manage by dividing files by business phase.

- app/input/ 
  - [Sample_Phase1.txt](app/input/Sample_Phase1.txt)
  - [Sample_Phase2.txt](app/input/Sample_Phase2.txt)


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


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License, see the LICENSE.txt file for details.
