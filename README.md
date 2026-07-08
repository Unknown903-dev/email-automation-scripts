# Student Community Invite Automation

A Python automation project for helping students connect with course-based online communities more easily.

This project started as a simple desktop automation tool that helped reduce the repetitive work of manually inviting students to class Discord/community spaces. The original version used cursor and keyboard automation. The newer version rebuilds the workflow using the Canvas API, making it safer, more reliable, and easier to maintain.

## Project Purpose

In many classes, students benefit from joining shared course communities where they can ask questions, share resources, and support each other. Manually inviting students one by one can be slow, repetitive, and difficult to scale.

This project was created to automate part of that process while keeping the workflow controlled, reviewable, and responsible.

## Repository Structure

```text
email-automation-scripts/
├── canvas-api-invite/
│   └── Modern Canvas API version
│
├── send-email-by-cursor/
│   └── Original cursor/keyboard automation prototype
│
└── LICENSE
```

## Recommended Version

The recommended version is:

```text
canvas-api-invite/
```

This version uses the Canvas API instead of controlling the mouse and keyboard. It is more reliable because it does not depend on screen size, browser position, or manually clicking through the interface.

## Versions

### 1. `canvas-api-invite/`

Modern API-based rebuild.

This version can:

* Connect to Canvas using an API token.
* List courses visible to the Canvas account.
* List active users in a course.
* Send Canvas Inbox messages.
* Preview messages with dry-run mode before sending.
* Filter recipients using a CSV file.
* Avoid duplicate messages using a local sent log.
* Keep private tokens and student data out of GitHub.

This is the main version of the project going forward.

### 2. `send-email-by-cursor/`

Legacy prototype.

This was the original version of the project. It used cursor movement, keyboard input, and local text files to automate repetitive invitation workflows.

This version is kept for project history, but it is not the recommended version because it depends on screen layout and can break if the browser window, zoom level, or interface changes.

## Why This Project Matters

This project helped solve a real coordination problem: inviting students into course-based support communities without requiring someone to manually message or invite each person.

The automation helped reduce repetitive work and made it easier to grow academic support spaces where students could connect with classmates, ask questions, and share resources.

## Features

The current Canvas API rebuild supports:

* Canvas API authentication
* Course listing
* Course user listing
* Canvas Inbox message sending
* Dry-run safety mode
* Recipient filtering
* Duplicate prevention
* Local send logs
* Environment-based configuration
* Private token handling through `.env`

## Safety and Responsible Use

This project should only be used for legitimate academic or community invitation workflows.

Do not use this project for:

* Spam
* Unwanted mass messaging
* Harassment
* Scraping private student information
* Sending messages without proper permission
* Bypassing school or platform policies

The Canvas API version is designed with safer defaults, including dry-run mode and duplicate prevention.

## Getting Started

Go into the Canvas API version:

```bash
cd canvas-api-invite
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r package.txt
```

Create a local `.env` file:

```bash
cp .env.example .env
```

Then update `.env` with your Canvas information:

```env
CANVAS_BASE_URL=https://your-school.instructure.com
CANVAS_TOKEN=your_canvas_token_here
```

Your `.env` file should not be committed to GitHub.

## Example Commands

List Canvas courses:

```bash
python main.py courses
```

List active students in a course:

```bash
python main.py users --course-id 12345
```

Preview a message without sending:

```bash
python main.py send \
  --course-id 12345 \
  --subject "Class Community Invite" \
  --message-file examples/sample_message.txt
```

Actually send the message:

```bash
python main.py send \
  --course-id 12345 \
  --subject "Class Community Invite" \
  --message-file examples/sample_message.txt \
  --send
```

Use a recipient CSV filter:

```bash
python main.py send \
  --course-id 12345 \
  --subject "Class Community Invite" \
  --message-file examples/sample_message.txt \
  --recipients-csv examples/sample_recipients.csv
```

## Privacy Notes

This project is designed to avoid committing private files.

The following should stay local:

```text
.env
data/sent_log.csv
local student CSV files
local message logs
```

The `.gitignore` file should prevent these files from being uploaded to GitHub.

## Future Improvements

Possible future improvements include:

* Better command-line output
* More automated tests
* Role-based recipient options
* Canvas section filtering
* Canvas group filtering
* Better error messages
* Confirmation prompts before sending
* Support for message templates
* Exportable summary reports
* Optional web dashboard

## Project Status

This project is actively being improved.

The original cursor automation version shows the first working prototype. The Canvas API version represents the cleaner and more professional rebuild.

## License

This project is licensed under the MIT License.