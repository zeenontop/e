import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse

def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def fetch_html_with_selenium(url):
    driver = init_driver()
    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    driver.quit()
    return html

def fetch_resources_from_html(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    
    html_links = []
    css_links = []
    js_links = []
    media_links = []
    
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        if href.endswith('.html') or href.endswith('.php'):
            html_links.append(urljoin(base_url, href))

    for link in soup.find_all('link', {'rel': 'stylesheet'}):
        css_url = link.get('href')
        if css_url:
            css_links.append(urljoin(base_url, css_url))
    
    for script in soup.find_all('script', {'src': True}):
        js_url = script.get('src')
        if js_url:
            js_links.append(urljoin(base_url, js_url))
    
    for img in soup.find_all(['img', 'video'], {'src': True}):
        media_url = img.get('src')
        media_links.append(urljoin(base_url, media_url))
    
    return html_links, css_links, js_links, media_links

def download_files(file_links, folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    for file_url in file_links:
        file_name = os.path.join(folder_name, os.path.basename(urlparse(file_url).path))
        try:
            print(f"⬇️ تحميل: {file_url}")
            with open(file_name, 'wb') as file:
                file.write(requests.get(file_url).content)
        except Exception as e:
            print(f"❌ خطأ في تحميل {file_url}: {e}")

def save_files(html_code, file_name, css_files, js_files):
    with open(f"{file_name}.html", "w", encoding="utf-8") as html_file:
        html_file.write(html_code)
    
    with open(f"{file_name}_styles.css", "w", encoding="utf-8") as css_file:
        for css_file_url in css_files:
            css_file.write(f"@import url({css_file_url});\n")
    
    with open(f"{file_name}_scripts.js", "w", encoding="utf-8") as js_file:
        for js_file_url in js_files:
            js_file.write(f"// External JS: {js_file_url}\n")
    
    print("✅ تم حفظ الملفات بنجاح.")

def extract_code_from_url(url):
    html_code = fetch_html_with_selenium(url)
    if not html_code:
        print("❌ خطأ في جلب HTML")
        return
    
    html_links, css_links, js_links, media_links = fetch_resources_from_html(html_code, url)
    
    download_files(media_links, "media")

    save_files(html_code, "index", css_links, js_links)

    for idx, html_link in enumerate(html_links):
        extra_html_code = fetch_html_with_selenium(html_link)
        save_files(extra_html_code, f"page_{idx+1}", [], [])

if __name__ == "__main__":
    url = input("🔗 أدخل رابط الموقع: ")
    extract_code_from_url(url)
