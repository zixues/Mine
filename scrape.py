import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_website(website):
    print("[scrape_website] Launching Chrome browser...")

    chrome_drive_path = "./chromedriver.exe"
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(service=Service(chrome_drive_path), options=options)

    try:
        start_time = time.time()
        driver.get(website)
        print(f"[scrape_website] Navigated to {website}")

        # Wait for known product-specific content containers
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".product-detail, .product-info, .product-title, h1"))
            )
        except:
            print("⚠️ [scrape_website] Warning: Product-specific content may not be fully loaded")

        # Scroll to bottom to trigger lazy loading
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        html = driver.page_source
        elapsed = time.time() - start_time
        return html
    finally:
        driver.quit()

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_str = str(soup)
    return body_str

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())
    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    total_len = len(dom_content)
    chunks = [dom_content[i:i + max_length] for i in range(0, total_len, max_length)]
    for idx, chunk in enumerate(chunks):
        print(f" - Chunk {idx + 1} length: {len(chunk)} chars")
        if idx == 0:
            print(f"   Sample chunk start:\n{chunk[:300]}")
    return chunks
