# QuickInvite

**Fast, safe Canvas invitations from your terminal.**

QuickInvite is a Python command-line tool for sending course and community invitations through the **Canvas Conversations API**.

It can discover your Canvas courses, list active course users, preview recipients and messages, personalize message templates, filter recipients, prevent duplicate sends, and create Canvas Inbox conversations.

QuickInvite is designed around a simple principle:

> **Preview first. Send explicitly.**

Running:

```bash
quickinvite
```

or:

```bash
python main.py
```

displays a compact command summary and exits.

QuickInvite is a traditional CLI. It does not use interactive menus, arrow-key navigation, or a full-screen terminal interface.

---

## What QuickInvite Does

QuickInvite can:

- Connect to Canvas using the Canvas REST API
- List courses available to your Canvas account
- List active users in a course
- Target students by default
- Filter by Canvas enrollment role
- Preview invitations before sending
- Send Canvas Inbox conversations
- Filter recipients with a CSV file
- Personalize messages using templates
- Track previously contacted recipients
- Skip duplicate recipients
- Process recipients in batches
- Keep Canvas credentials outside source code
- Provide detailed usage instructions through `--help`

---

# Important: Canvas Inbox, Not Direct Email

QuickInvite creates **Canvas Inbox conversations**.

It does **not** send direct SMTP email and does not require scraping student email addresses.

The flow is:

```text
QuickInvite
     ↓
Canvas Conversations API
     ↓
Canvas Inbox
     ↓
Recipient
```

Depending on each recipient's Canvas notification settings, Canvas may also notify them through:

- Email
- Push notifications
- Other configured notification methods

Those notifications are controlled by Canvas and the recipient's own settings.

---

# Requirements

You will need:

- Python 3.10 or newer
- A Canvas account
- Access to the course you want to use
- A Canvas API access token
- Permission to view/message the intended recipients

QuickInvite cannot grant your account additional Canvas permissions.

It can only perform actions that your Canvas account is already authorized to perform.

---

# Installation

Clone the repository and enter the QuickInvite directory:

```bash
git clone https://github.com/Unknown903-dev/email-automation-scripts.git
cd email-automation-scripts/canvas-api-invite
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

## Activate the Virtual Environment

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```cmd
.venv\Scripts\activate.bat
```

Install QuickInvite:

```bash
pip install -e .
```

The `-e` installs the project in editable mode, which is useful when developing because source-code changes are immediately reflected without reinstalling the package.

After installation, verify that the command works:

```bash
quickinvite
```

You can also use:

```bash
python main.py
```

---

# Leaving the Virtual Environment

When you are finished:

```bash
deactivate
```

To return later:

```bash
cd email-automation-scripts/canvas-api-invite
source .venv/bin/activate
```

Then QuickInvite will once again be available:

```bash
quickinvite
```

---

# Canvas Configuration

QuickInvite reads Canvas credentials from a local `.env` file.

Create one from the included example:

```bash
cp .env.example .env
```

Open `.env` and configure:

```env
CANVAS_BASE_URL=https://YOUR-SCHOOL.instructure.com
CANVAS_TOKEN=your_canvas_token_here
```

For example:

```env
CANVAS_BASE_URL=https://school.instructure.com
CANVAS_TOKEN=12345~example_token
```

Do not add a trailing API path such as:

```text
/api/v1
```

unless the current configuration specifically requires it.

QuickInvite handles the Canvas API routes internally.

---

# Getting a Canvas Access Token

Canvas commonly provides access-token management under:

```text
Canvas
→ Account
→ Settings
→ New Access Token
```

The exact interface may differ depending on your institution.

Some institutions disable personal Canvas access tokens entirely. If the option is unavailable, contact your institution or Canvas administrator.

When creating a token:

- Give it a recognizable purpose
- Use the shortest practical expiration period
- Revoke it when you are finished
- Never publish it
- Never commit it to Git
- Never place it directly in Python source code

Treat a Canvas access token like a password.

---

# Never Commit Your Token

Your `.env` file should remain local.

Before committing code, verify:

```bash
git status
```

Files such as:

```text
.env
```

should not appear as staged files.

If a real Canvas token is ever accidentally committed to a public repository, revoke the token immediately and create a new one.

Removing the token from a later commit is not enough because it may remain in Git history.

---

# Starting QuickInvite

Run:

```bash
quickinvite
```

or:

```bash
python main.py
```

QuickInvite displays a compact overview similar to:

```text
QuickInvite

Usage: quickinvite [options]

╭───────────────────────────────────────────────────────╮
│                                                       │
│   Send Canvas course invitations quickly and safely   │
│                                                       │
╰───────────────────────────────────────────────────────╯

Options:

  -c, --courses            List Canvas courses
  -u, --users <course_id>  List users in a course
  -p, --preview            Preview an invitation
  -s, --send               Send an invitation
      --version            Show version number
  -h, --help               Show detailed help
```

Running QuickInvite by itself does **not** contact Canvas or send messages.

---

# Detailed Help

For complete usage instructions:

```bash
quickinvite --help
```

or:

```bash
python main.py --help
```

The help screen explains the complete workflow, available options, templates, recipient filtering, configuration, and safety behavior.

---

# Recommended Workflow

A typical QuickInvite session follows this process:

```text
1. List Courses
       ↓
2. Choose Course ID
       ↓
3. List Students
       ↓
4. Prepare Message
       ↓
5. Preview
       ↓
6. Review Recipients
       ↓
7. Explicitly Send
```

---

# 1. List Your Canvas Courses

Run:

```bash
quickinvite --courses
```

or:

```bash
python main.py --courses
```

Example output:

```text
Canvas Courses

┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Course ID ┃ Course                         ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 12345     │ CSE 100 - Software Engineering │
│ 67890     │ CSE 195 - Capstone             │
└───────────┴────────────────────────────────┘
```

Find the course you want and copy its Canvas course ID.

For example:

```text
12345
```

You will use that ID in subsequent commands.

---

# 2. List Students in a Course

Use:

```bash
quickinvite --users 12345
```

Replace:

```text
12345
```

with the Canvas course ID.

For example:

```bash
quickinvite --users 67890
```

QuickInvite requests **active enrollments**.

By default, the role is:

```text
student
```

This means the normal command excludes:

- Teachers
- Teaching assistants
- Observers
- Designers

unless another role is explicitly requested.

---

# Recipient Roles

The normal invitation workflow targets:

```text
student
```

QuickInvite can also work with other Canvas enrollment roles when explicitly selected.

Depending on Canvas support and permissions, roles may include:

```text
student
teacher
ta
observer
designer
```

For example:

```bash
quickinvite --users 12345 --role ta
```

would request active teaching assistants instead of active students.

For normal student-community invitations, leave the role at its default:

```text
student
```

---

# 3. Create Your Message

Messages are stored in ordinary text files.

For example:

```text
examples/sample_message.txt
```

A simple message might contain:

```text
Hi {{name}},

You're invited to join our class community:

https://discord.gg/example
```

This keeps the message body separate from the command itself and makes messages easier to review before sending.

---

# Message Templates

QuickInvite supports placeholders that can be replaced using information provided by Canvas.

Available placeholders include:

```text
{{id}}
{{name}}
{{sortable_name}}
{{login_id}}
{{email}}
```

Example:

```text
Hi {{name}},

Welcome!

Your Canvas login is {{login_id}}.

You can join our class community here:

https://discord.gg/example
```

QuickInvite renders the available values for each recipient.

Not every Canvas instance exposes every field.

For example, `email` may not be available depending on:

- Canvas permissions
- Institutional configuration
- Account privacy settings
- API response behavior

Your message should therefore avoid depending on optional fields unless you know your Canvas account can access them.

---

# 4. Preview Before Sending

Preview the operation with:

```bash
quickinvite --preview \
  --course-id 12345 \
  --subject "Class Community Invite" \
  --message-file examples/sample_message.txt
```

Preview mode is the recommended first step.

It should show information such as:

```text
Course
Recipients
Subject
Message
Mode: DRY RUN
```

A preview does **not** create real Canvas conversations.

Conceptually:

```text
--preview

Canvas Users
     ↓
Recipient Filtering
     ↓
Template Rendering
     ↓
Preview
     ↓
STOP
```

The Canvas send endpoint should not be called.

---

# 5. Send the Message

After reviewing the preview, perform the real send using:

```bash
quickinvite --send \
  --course-id 12345 \
  --subject "Class Community Invite" \
  --message-file examples/sample_message.txt
```

The important distinction is:

```text
--preview
    ↓
Nothing sent


--send
    ↓
Real Canvas conversations created
```

Only use `--send` when you are ready to contact the selected recipients.

---

# Dry-Run Safety

QuickInvite is designed around explicit sending.

Running:

```bash
quickinvite
```

does not send anything.

Running:

```bash
quickinvite --help
```

does not send anything.

Running:

```bash
quickinvite --courses
```

does not send anything.

Running:

```bash
quickinvite --users 12345
```

does not send anything.

Running:

```bash
quickinvite --preview ...
```

does not send anything.

A real message operation requires:

```bash
--send
```

This behavior is intentional and should not be removed without a strong reason.

---

# Filtering Recipients with CSV

You can restrict an invitation to specific people instead of messaging every eligible student in the course.

Create a CSV file such as:

```csv
name
Jane Student
Alex Student
```

Then preview using:

```bash
quickinvite --preview \
  --course-id 12345 \
  --subject "Class Community Invite" \
  --message-file examples/sample_message.txt \
  --recipients-csv examples/sample_recipients.csv
```

When ready:

```bash
quickinvite --send \
  --course-id 12345 \
  --subject "Class Community Invite" \
  --message-file examples/sample_message.txt \
  --recipients-csv examples/sample_recipients.csv
```

Depending on which values Canvas exposes, recipient matching may use fields such as:

```text
id
name
sortable_name
login_id
email
```

---

# CSV Privacy

A real recipient CSV may contain student information.

Do not commit those files to the repository.

Examples include:

```text
student names
Canvas IDs
login IDs
email addresses
course membership information
```

Example files in the repository should contain fake/sample data only.

---

# Duplicate Prevention

QuickInvite maintains a sent log so recipients are not repeatedly contacted by accident.

The default location is:

```text
data/sent_log.csv
```

The process is approximately:

```text
Eligible Canvas Users
        ↓
Recipient Filters
        ↓
Read Sent Log
        ↓
Already Contacted?
     ↙             ↘
   Yes              No
    ↓                ↓
  Skip          Eligible to Send
```

This provides protection against accidentally rerunning the same invitation.

---

# Sent Log Privacy

The sent log may contain Canvas-derived information.

It should remain local.

Do not commit:

```text
data/sent_log.csv
```

to a public repository.

---

# Allowing Previously Contacted Recipients

QuickInvite includes an option to disable duplicate protection when explicitly needed.

Use:

```text
--no-dedupe
```

only when you intentionally want previously recorded recipients to be eligible again.

Example:

```bash
quickinvite --preview \
  --course-id 12345 \
  --subject "Updated Community Invite" \
  --message-file examples/sample_message.txt \
  --no-dedupe
```

Preview the results carefully before combining this option with `--send`.

---

# Batch Processing

Canvas API requests may be processed in batches.

QuickInvite supports configurable batch sizes.

The default should generally be sufficient.

If you need to specify a different value:

```text
--batch-size <number>
```

Example:

```bash
quickinvite --preview \
  --course-id 12345 \
  --subject "Class Community Invite" \
  --message-file examples/sample_message.txt \
  --batch-size 25
```

Changing the batch size does not bypass Canvas API permissions or limits.

---

# Group Conversations

QuickInvite may support creating a shared Canvas conversation through:

```text
--group-conversation
```

Without this mode, normal invitation behavior should be preferred when recipients should receive individual conversations.

Be careful with shared conversations because recipients may be able to see information or replies involving other participants depending on Canvas behavior.

Preview and understand the intended conversation mode before using it.

---

# Common Commands

## Open QuickInvite

```bash
quickinvite
```

## Detailed Help

```bash
quickinvite --help
```

## Version

```bash
quickinvite --version
```

## List Courses

```bash
quickinvite --courses
```

## List Students

```bash
quickinvite --users 12345
```

## Preview

```bash
quickinvite --preview \
  --course-id 12345 \
  --subject "Class Community Invite" \
  --message-file examples/sample_message.txt
```

## Send

```bash
quickinvite --send \
  --course-id 12345 \
  --subject "Class Community Invite" \
  --message-file examples/sample_message.txt
```

## Preview Selected Recipients

```bash
quickinvite --preview \
  --course-id 12345 \
  --subject "Class Community Invite" \
  --message-file examples/sample_message.txt \
  --recipients-csv examples/sample_recipients.csv
```

---

# Using `python main.py`

Installing QuickInvite gives you the cleaner:

```bash
quickinvite
```

command.

However, the traditional Python entry point is also supported:

```bash
python main.py
```

Equivalent examples:

```bash
python main.py --courses
```

```bash
python main.py --users 12345
```

```bash
python main.py --preview \
  --course-id 12345 \
  --subject "Class Community Invite" \
  --message-file examples/sample_message.txt
```

The installed `quickinvite` command is recommended for normal use.

---

# Project Structure

The QuickInvite application is organized approximately as:

```text
canvas-api-invite/
│
├── src/
│   └── canvas_inviter/
│       ├── cli.py
│       ├── canvas_client.py
│       └── supporting modules
│
├── examples/
│   ├── sample_message.txt
│   └── sample_recipients.csv
│
├── tests/
│   └── automated tests
│
├── data/
│   └── local runtime data
│
├── main.py
├── pyproject.toml
├── .env.example
├── .gitignore
└── README.md
```

The general architecture is:

```text
             QuickInvite CLI
                    │
                    ▼
          Command / Input Logic
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
 Recipient Logic       Message Templates
          │                   │
          └─────────┬─────────┘
                    ▼
               CanvasClient
                    │
                    ▼
             Canvas REST API
```

Canvas HTTP request logic should remain separate from terminal presentation code.

---

# Development

Because QuickInvite is installed with:

```bash
pip install -e .
```

changes made inside:

```text
src/canvas_inviter/
```

are immediately reflected when you run:

```bash
quickinvite
```

This makes local development straightforward.

---

# Testing

QuickInvite includes automated tests for important CLI and safety behavior.

Run the test suite from:

```text
canvas-api-invite/
```

using:

```bash
python -m unittest discover -s tests -v
```

If pytest is installed and supported by the project, you may also use:

```bash
pytest -v
```

Important behaviors that should remain tested include:

- Dry-run never performs a real send
- `quickinvite` does not initialize Canvas unnecessarily
- `quickinvite --help` does not require Canvas credentials
- CLI options map to the correct behavior
- Existing Canvas API logic remains functional

Automated tests should **never perform a real Canvas message send**.

---

# Testing the CLI Manually

A safe manual test sequence is:

```bash
quickinvite
```

Then:

```bash
quickinvite --help
```

Then:

```bash
quickinvite --version
```

Then:

```bash
quickinvite --courses
```

Then use a real course ID:

```bash
quickinvite --users 12345
```

Finally, test preview:

```bash
quickinvite --preview \
  --course-id 12345 \
  --subject "QuickInvite Test" \
  --message-file examples/sample_message.txt
```

Do not test:

```bash
--send
```

unless you intentionally want real Canvas conversations to be created.

---

# Troubleshooting

## `quickinvite: command not found`

Make sure the virtual environment is active:

```bash
source .venv/bin/activate
```

Then reinstall:

```bash
pip install -e .
```

Check:

```bash
which python
which pip
which quickinvite
```

On Windows:

```cmd
where python
where quickinvite
```

---

## Canvas Token Error

Verify `.env` contains:

```env
CANVAS_BASE_URL=https://YOUR-SCHOOL.instructure.com
CANVAS_TOKEN=your_token_here
```

Make sure:

- The token has not expired
- The token has not been revoked
- The Canvas URL is correct
- There are no unnecessary quotation marks
- You are using the correct Canvas environment

---

## Course Does Not Appear

QuickInvite can only display courses visible to the authenticated Canvas account.

Possible causes include:

- The course is concluded
- The account does not have access
- The wrong Canvas account/token is being used
- Your institution restricts API access
- Canvas does not return the course for the requested state

---

## Students Do Not Appear

By default, QuickInvite requests active students.

Verify:

- The course ID is correct
- The students are actively enrolled
- Your Canvas account can view the roster
- The selected role is correct

Remember:

```text
Default role = student
```

Teachers and TAs are excluded unless explicitly selected.

---

## A Recipient Was Skipped

Check the local sent log:

```text
data/sent_log.csv
```

The recipient may already be recorded as contacted.

Duplicate prevention is intentional.

Use `--no-dedupe` only when you understand why the recipient should be contacted again.

---

## Email Is Missing

Canvas does not always expose users' email addresses through the API.

This depends on the institution and your permissions.

QuickInvite does not need direct email addresses to send Canvas Inbox conversations.

---

# Security

QuickInvite should never expose:

```text
CANVAS_TOKEN
```

in:

- CLI output
- Logs
- Exceptions shown to ordinary users
- Git commits
- Screenshots
- Example configuration files

`.env.example` should contain placeholders only.

For example:

```env
CANVAS_BASE_URL=https://YOUR-SCHOOL.instructure.com
CANVAS_TOKEN=your_canvas_token_here
```

Never place a real token in `.env.example`.

---

# Privacy

Canvas-derived information can include private educational information.

Do not publicly commit:

- Student names
- Canvas user IDs
- Login IDs
- Email addresses
- Enrollment information
- Course membership information
- Recipient lists
- Send logs
- Real message histories
- Canvas access tokens

Files that should normally stay local include:

```text
.env
data/sent_log.csv
local recipient CSV files
local message logs
```

Before every public commit:

```bash
git status
```

Review the files carefully.

---

# Responsible Use

QuickInvite is intended for legitimate course and community communication.

Do not use it for:

- Spam
- Harassment
- Unwanted advertising
- Unauthorized mass messaging
- Scraping student information
- Circumventing Canvas permissions
- Circumventing institutional policies
- Contacting users who would not reasonably expect the message

Having technical access to an API does not automatically mean every possible use of that API is appropriate or authorized.

Use QuickInvite only within the permissions and policies applicable to your Canvas account and institution.

---

# Design Principles

QuickInvite intentionally favors:

```text
Simple commands
Safe defaults
Explicit sending
Readable output
Minimal UI complexity
Separated business logic
Testable behavior
Private credential handling
```

The project intentionally does **not** try to be a full-screen terminal application.

Running:

```bash
quickinvite
```

should remain fast and simple.

---

# Quick Reference

```text
COMMAND                                      PURPOSE

quickinvite                                  Show QuickInvite
quickinvite --help                           Detailed instructions
quickinvite --version                        Show version

quickinvite --courses                        List Canvas courses
quickinvite --users <course_id>              List active students

quickinvite --preview ...                    Preview only
quickinvite --send ...                       Perform real send

--course-id <id>                             Select Canvas course
--subject "<text>"                           Canvas message subject
--message-file <path>                        Message body/template
--recipients-csv <path>                      Restrict recipients
--role <role>                                Select enrollment role
--batch-size <n>                             Configure batch size
--sent-log <path>                            Select sent-log file
--no-dedupe                                  Allow prior recipients
--group-conversation                         Shared conversation mode
```

For the authoritative list of options in your installed version:

```bash
quickinvite --help
```

---

# Disclaimer

QuickInvite is an independent, unofficial open-source project.

It is not affiliated with, sponsored by, or endorsed by:

- Instructure
- Canvas
- Discord
- Microsoft
- Any educational institution

Users are responsible for complying with:

- Their institution's policies
- Applicable privacy requirements
- Canvas API policies and terms
- Rules governing student information
- Any requirements applicable to the community being promoted

The software is provided as an automation tool. The user remains responsible for deciding who should be contacted and whether they have authorization to do so.

---

# License

QuickInvite is distributed as part of the `email-automation-scripts` repository under the MIT License.

See the repository's:

```text
LICENSE
```

file for the complete license terms.