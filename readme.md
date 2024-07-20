# Email Campaign Sender Project

This project is an Email Campaign Sender built using Django. It allows users to create and manage email campaigns, configure SMTP settings, and send emails with options for rotating sender information.

## Table of Contents
1. [Features](#features)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [SMTP and Sender Rotation](#smtp-and-sender-rotation)
7. [File Structure](#file-structure)
8. [Troubleshooting](#troubleshooting)

## Features
- Create and manage email campaigns
- Add attachment content to campaigns
- Configure SMTP settings for sending emails
- Options for rotating sender information
- Import subscriber emails from text files

## Requirements
- Python 3.8+
- Django 3.2+
- Additional Python packages as specified in `requirements.txt`

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/ohunayogege/email-campaign-sender.git
    cd email-campaign-sender
    ```

2. **Create a virtual environment:**
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run database migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

## Configuration

1. **Add SMTP Configurations:**
   - Go to the Django admin panel (`http://127.0.0.1:8000`).
   - Select SMTP at the navbar.
   - Add SMTP configurations in the SMTP Configuration section.

2. **Prepare Sender Information Files:**
   - Create three text files: `first_names.txt`, `last_names.txt`, and `emails.txt`.
   - Populate these files with first names, last names, and email addresses, respectively. Each entry should be on a new line.

## Usage

1. **Create a Campaign:**
   - Go to the Campaigns page and click "Create Campaign".
   - Fill in the campaign details including title, subject, content, and attachment content.
   - Select the sender type (Rotate Sender or Default Sender).
   - Save the campaign.

2. **Send a Campaign:**
   - On the Campaigns page, click the "Send" button next to the campaign you want to send.
   - Select the domain and SMTP configuration.
   - Click "Send".

## SMTP and Sender Rotation

- **Rotate Sender:** If selected, the sender's name and email will be picked randomly from the provided text files (`first_names.txt`, `last_names.txt`, `emails.txt`).
- **Default Sender:** If selected, the default SMTP configuration's sender information will be used.

## File Structure

```
email-campaign-sender/
├── .gitignore
├── first_names.txt
├── last_names.txt
├── emails.txt
├── requirements.txt
├── templates/
│ ├── campaign_list.html
│ ├── campaign_form.html
│ ├── add_smtp_configuration.html
│ ├── confirm_delete_all.html
│ ├── confirm_delete_campaign.html
│ ├── dashboard.html
│ ├── delete_smtp_configuration.html
│ ├── import_subscribers.html
│ ├── message_log_list.html
│ ├── subscriber_list.html
│ ├── smtp_list.html
│ ├── index.html
│ └── base.html
├── web/
│ ├── init.py
│ ├── admin.py
│ ├── apps.py
│ ├── consumers.py
│ ├── forms.py
│ ├── models.py
│ ├── urls.py
│ ├── utils.py
│ ├── views.py
├── manage.py
├── requirements.txt
└── campaign/
├── init.py
├── celery.py
├── settings.py
├── urls.py
└── wsgi.py
```


## Troubleshooting

- **Issues with SMTP Configuration:**
  - Ensure SMTP settings are correct (host, port, username, password).
  - Verify the SMTP server allows external connections.

- **Issues with Sender Rotation:**
  - Check that the text files (`first_names.txt`, `last_names.txt`, `emails.txt`) are correctly populated and located in the project directory.
  - Ensure the paths to these files are correctly specified in the `get_random_sender_info` function.

For additional help, refer to the Django documentation or raise an issue via WhatsApp (08149983395).
