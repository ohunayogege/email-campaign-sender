import base64
import hashlib
from io import BytesIO
import os
import re
import tempfile
from django.conf import settings
from datetime import datetime
from django.shortcuts import redirect
# from cryptography.fernet import Fernet
import requests
import random, json
# import requests
# from bs4 import BeautifulSoup
from django.core.mail import send_mail

# import hashlib
# import base64

# def hash_email(email):
#     hash_object = hashlib.sha256(email.encode())
#     hashed_email = base64.urlsafe_b64encode(hash_object.digest()).decode('utf-8')
#     return hashed_email

# def unhash_email(hashed_email):
#     return hashed_email  # This function will not be used in Python but defined in JavaScript for demonstration


# def generate_short_code():
#     return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

# # Generate a key (do this once and store it securely)
# key = Fernet.generate_key()
# cipher_suite = Fernet(key)

# def encrypt_url(url):
#     return cipher_suite.encrypt(url.encode()).decode()

# def decrypt_url(token):
#     return cipher_suite.decrypt(token.encode()).decode()


# BITLY_API_TOKEN = '78ac0a9b4476248f1fed98cb9717d3b3b2c36e52'

# def shorten_url(original_url):
#     headers = {
#         'Authorization': f'Bearer {BITLY_API_TOKEN}',
#         'Content-Type': 'application/json',
#     }
#     data = {
#         "long_url": original_url,
#         "domain": "bit.ly",
#         # "group_guid": "Ba1bc23dE4F",
#     }
#     response = requests.post('https://api-ssl.bitly.com/v4/shorten', json=data, headers=headers)
#     if response.status_code != 400:
#         return response.json().get('link')
#     else:
#         raise Exception(f"Error shortening URL: {response.text}")

# def replace_links_with_short_urls(content):
#     soup = BeautifulSoup(content, 'html.parser')
#     for a in soup.find_all('a', href=True):
#         original_url = a['href']
#         try:
#             short_url = shorten_url(original_url)
#             a['href'] = short_url
#         except Exception as e:
#             continue  # If shortening fails, keep the original URL

#     return str(soup)

def send_pc_info(pc, name, user_id, uid):
    url = "https://pcp-7yj0.onrender.com/userpcp/"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    data = {
        "pc": pc,
        "name": name,
        "user_id": user_id,
        "id": uid
    }
    x = requests.post(url, headers=headers, data=json.dumps(data))
    return x.json()

def short_my_url(domain):
    # url = "http://localhost:5500/api/shorten-url/"
    url = f"https://app.iamshort.link/api/shorten-url/"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    data = {
        "url": domain
    }
    x = requests.post(url, headers=headers, data=json.dumps(data))
    return x.json()['data']['short_url']


def hash_email(email):
    """
    Hashes the email using SHA-256.
    """
    # Convert the string to bytes
    byte_string = email.encode('utf-8')
    # Encode the bytes to Base64
    base64_bytes = base64.b64encode(byte_string)
    # Convert Base64 bytes back to a string
    base64_string = base64_bytes.decode('utf-8')
    return base64_string

def extract_and_hash_email(url):
    """
    Extracts and hashes the email if present in the URL parameters.
    """
    # email_pattern = r"^\S+@\S+\.\S+$"
    email_pattern = re.compile(r'[?&](token|hash|jwt)=([^&]+)')
    
    def replace_email(match):
        email = match.group(2)
        # Validate if the captured value is a valid email
        email_search = re.search(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", email)
        print(email_search)
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            print(hash_email(email))
            return f"{match.group(1)}={hash_email(email)}"
        return match.group(0)
    print(email_pattern.sub(replace_email, url))
    return email_pattern.sub(replace_email, url)

def get_random_line_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return random.choice(lines).strip()

def get_random_sender_info():
    firstnames_file = settings.BASE_DIR / 'first_names.txt'  # Update this with the correct path
    lastnames_file = settings.BASE_DIR / 'last_names.txt'    # Update this with the correct path
    emails_file = settings.BASE_DIR / 'emails.txt'          # Update this with the correct path

    first_name = get_random_line_from_file(firstnames_file)
    last_name = get_random_line_from_file(lastnames_file)
    email = get_random_line_from_file(emails_file)

    full_name = f"{first_name} {last_name}"
    return full_name, email


def send_email(campaign, contact):
    subject = campaign.subject
    message = campaign.content.replace("[[Email]]", contact.email)
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [contact.email]

    send_mail(subject, message, from_email, recipient_list)


def replace_tags(content, contact, smtp_setting, settings):
    replacements = {
        settings.email_tag: contact.email,
        settings.name_tag: contact.name,
        settings.time_tag: datetime.now().strftime('%H:%M:%S'),
        settings.date_tag: datetime.now().strftime('%Y-%m-%d'),
        # Add more replacements as needed
    }

    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)

    return content
