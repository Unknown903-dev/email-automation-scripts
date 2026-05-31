# Email Automation Scripts

Email Automation Scripts is a collection of Python scripts created to help automate repetitive invitation workflows. The scripts were used to speed up the process of entering names or usernames into Outlook and Canvas invitation forms.

This project was built for educational and productivity purposes to reduce manual typing, save time, and make repeated invitation tasks more efficient.

## Purpose

The purpose of this project is to practice basic desktop automation with Python while solving a real repetitive task. Instead of manually typing each name one by one, the scripts read names from a text file and automate the process of entering them into an invitation field.

These scripts were created to help invite students into shared learning spaces and communities where they could collaborate, access resources, and connect with others.

## Features

* Reads names or usernames from text files
* Automates typing into Outlook or Canvas invitation fields
* Uses keyboard and mouse automation through Python
* Supports individual invitation workflows
* Supports Outlook group invitation workflows
* Includes a filtered Canvas script to help avoid inviting the same person more than once
* Tracks previously invited names using a text file

## Tech Stack

* Python
* Windows API through `ctypes`
* Text files for input and tracking

## Project Files

```text
email-automation-scripts/
├── Blue_email_invitations.py
├── canvas_email_invitations.py
├── canvas_email_invitations_filter_sent_emails.py
├── outlook_Group_inv.py
├── LICENSE
└── README.md
```

## Script Overview

### `Blue_email_invitations.py`

Automates entering names or usernames into Outlook using a list from a text file.

### `canvas_email_invitations.py`

Automates entering student names into Canvas invitation fields using a text file.

### `canvas_email_invitations_filter_sent_emails.py`

Automates Canvas invitations while checking a previous list of names to avoid sending duplicate invitations.

### `outlook_Group_inv.py`

Automates adding users to an Outlook group invitation workflow.

## How It Works

The scripts use Python to control the mouse and keyboard on a Windows machine. Each script moves the cursor to a specific location, clicks the input field, reads names from a text file, types each name, and presses Enter to submit it.

Some scripts include delays to give the website or application enough time to load before entering the next name.

## Example Input Files

Depending on the script, the program may expect text files such as:

```text
fun.txt
list.txt
current_class.txt
previous_classes.txt
```

Each file should contain one name or username per line.

Example:

```text
studentone
studenttwo
studentthree
```

## How to Run

1. Clone the repository:

```bash
git clone https://github.com/Unknown903-dev/email-automation-scripts.git
```

2. Open the project folder:

```bash
cd email-automation-scripts
```

3. Make sure the required input text file exists.

For example:

```text
fun.txt
```

4. Run one of the scripts:

```bash
python canvas_email_invitations.py
```

or:

```bash
python outlook_Group_inv.py
```

## Important Notes

These scripts depend on the screen layout and cursor positions. If the browser window, zoom level, or input field position changes, the coordinates in the script may need to be updated.

Because the scripts use Windows-specific automation through `ctypes`, they are intended for Windows environments.

## What I Learned

While building this project, I practiced using Python for desktop automation, reading data from text files, controlling keyboard and mouse input, and solving repetitive workflow problems. I also learned the importance of adding delays, avoiding duplicate actions, and making automation safer by tracking previously processed names.

## Future Improvements

* Refactor repeated mouse and keyboard logic into helper functions
* Move cursor coordinates into a configuration file
* Add clearer setup instructions for each script
* Add input validation for empty lines and duplicate names
* Add a dry-run mode to preview names before sending
* Replace coordinate-based automation with an official API if available
* Add `.gitignore` for temporary files and local input lists

## Responsible Use

These scripts should only be used for legitimate invitation workflows and only with people who should receive the invitation. They should not be used for spam, unwanted messages, or mass emailing without permission.
