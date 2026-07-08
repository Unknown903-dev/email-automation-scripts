# Canvas API Invite Automation

A safer rebuild of the old coordinate-based email automation scripts. Instead of moving the mouse and typing into Canvas/Outlook, this project uses the Canvas API to send Canvas Inbox messages to course users.

## What this does

- Lists Canvas courses available to your token
- Lists active course users by role, usually students
- Sends Canvas Inbox messages through the Canvas Conversations API
- Supports dry-run mode by default
- Filters recipients from a CSV file
- Skips people already recorded in `data/sent_log.csv`
- Keeps your Canvas token out of GitHub using `.env`

## Important note

This sends **Canvas Inbox conversations**, not direct SMTP email. Students may still receive email/push notifications depending on their Canvas notification settings. This is safer and more Canvas-native than scraping email addresses or automating browser clicks.

Use this only for legitimate course/community communication where recipients would reasonably expect the message. Do not use this for spam or unwanted mass messaging.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r package.txt
cp .env.example .env
```

Edit `.env`:

```bash
CANVAS_BASE_URL=https://YOUR-SCHOOL.instructure.com
CANVAS_TOKEN=your_canvas_token_here
```

Your Canvas token should be treated like a password. Do not commit it or share it.
you can find this on canvas head over to 
```bash
profile -> settings -> new access token
```
fill out the info and make sure it expires within a day or two, no longer then a week is reccomended for secuirty reasons

## Commands

### 1. List your courses

```bash
python main.py courses
```

Output example:

```text
12345   CSE 100 - Software Engineering
67890   CSE 195 - Capstone
```

### 2. List students in a course

```bash
python main.py users --course-id 12345
```

### 3. Dry-run a message

Dry-run is the default. Nothing sends unless you add `--send`.

```bash
python main.py send \
  --course-id 12345 \
  --subject "Class Discord Invite" \
  --message-file examples/sample_message.txt
```

### 4. Actually send

```bash
python main.py send \
  --course-id 12345 \
  --subject "Class Discord Invite" \
  --message-file examples/sample_message.txt \
  --send
```

### 5. Send only to selected people

Create a CSV such as:

```csv
name
Jane Student
Alex Student
```

Then run:

```bash
python main.py send \
  --course-id 12345 \
  --subject "Class Discord Invite" \
  --message-file examples/sample_message.txt \
  --recipients-csv examples/sample_recipients.csv \
  --send
```

The CSV can match any of these columns when Canvas exposes them:

```text
id,name,sortable_name,login_id,email
```

## Message templates

The message file supports simple placeholders:

```text
Hi {{name}},

Discord invite: https://discord.gg/example
```

Available placeholders:

```text
{{id}}
{{name}}
{{sortable_name}}
{{login_id}}
{{email}}
```

If a placeholder is used, the script sends messages one person at a time so each recipient gets a personalized message.

## Safety features

- `--send` is required before anything sends
- `data/sent_log.csv` prevents duplicate messages
- `.env` is ignored by Git
- `data/*.csv` is ignored by Git so student data is not accidentally committed
- `--recipients-csv` lets you restrict a send to specific students

## Canvas permissions

The tool can only do what your Canvas account is allowed to do. If your token cannot see a course, list users, or send conversations, the API will return an error.
