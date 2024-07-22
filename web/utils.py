from io import BytesIO
import os
import re
import tempfile
from django.conf import settings
from django.shortcuts import redirect
from cryptography.fernet import Fernet
import string
import random
# from fpdf import FPDF
import requests
from bs4 import BeautifulSoup
# import asyncio
# from pyppeteer import launch



def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

# Generate a key (do this once and store it securely)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

def encrypt_url(url):
    return cipher_suite.encrypt(url.encode()).decode()

def decrypt_url(token):
    return cipher_suite.decrypt(token.encode()).decode()


BITLY_API_TOKEN = '78ac0a9b4476248f1fed98cb9717d3b3b2c36e52'

def shorten_url(original_url):
    headers = {
        'Authorization': f'Bearer {BITLY_API_TOKEN}',
        'Content-Type': 'application/json',
    }
    data = {
        "long_url": original_url,
        "domain": "bit.ly",
        # "group_guid": "Ba1bc23dE4F",
    }
    print(data)
    response = requests.post('https://api-ssl.bitly.com/v4/shorten', json=data, headers=headers)
    if response.status_code == 200:
        return response.json().get('link')
    else:
        raise Exception(f"Error shortening URL: {response.text}")

def replace_links_with_short_urls(content):
    soup = BeautifulSoup(content, 'html.parser')
    for a in soup.find_all('a', href=True):
        original_url = a['href']
        try:
            short_url = shorten_url(original_url)
            a['href'] = short_url
        except Exception as e:
            continue  # If shortening fails, keep the original URL

    return str(soup)


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


# async def generate_image_from_html(html_content):
#     browser = await launch(executablePath='path/to/chromium', headless=True)
#     page = await browser.newPage()
#     await page.setContent(html_content)
#     image_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
#     await page.screenshot({'path': image_file.name, 'fullPage': True})
#     await browser.close()
#     return image_file.name

# def generate_image_from_html_sync(html_content):
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     return loop.run_until_complete(generate_image_from_html(html_content))

# def generate_pdf_from_image(image_path):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.image(image_path, x=10, y=10, w=pdf.w - 20)
#     pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
#     pdf.output(pdf_file.name)
#     os.remove(image_path)
#     return pdf_file.name