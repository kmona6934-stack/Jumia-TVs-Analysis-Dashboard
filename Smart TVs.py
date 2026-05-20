from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

def scrape_jumia_live(target_count=100):
    print(f"Starting Smart TVs Experiment (15k - 40k) ...\n")
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    scraped_data = []
    page_number = 1
    
    try:
        while len(scraped_data) < target_count:
            print(f"Navigating to page: {page_number}")
            url = f"https://www.jumia.com.eg/electronic-television-video/?price=15000-40000&page={page_number}"
            driver.get(url)
            time.sleep(5) 

            for scroll in range(1, 4):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1.5)
            
            product_elements = driver.find_elements(By.XPATH, "//article[@class='prd _fb col c-prd']")
            print(f"Found {len(product_elements)} potential products on page {page_number}")
            
            if len(product_elements) == 0:
                break
                
            for item in product_elements:
                if len(scraped_data) >= target_count:
                    break
                try:
                    name = item.find_element(By.XPATH, ".//h3[@class='name']").text.strip()
                    row_price = item.find_element(By.XPATH, ".//div[@class='prc']").text.strip()
                    product_url = item.find_element(By.TAG_NAME, "a").get_attribute("href")
                    
                    brand = name.split()[0]
                    
                    try:
                        discount = item.find_element(By.XPATH, ".//div[contains(@class, 'bdg _dsct')]").text.strip()
                    except:
                        discount = "0%"

                    clean_price = row_price.replace("EGP", "").replace(",", "").replace(" ", "").strip()
                    numeric_price = float(clean_price)

                    if 15000 <= numeric_price <= 40000:
                        scraped_data.append({
                            "Brand": brand,
                            "Product Name": name,
                            "Price (EGP)": numeric_price,
                            "Discount": discount,
                            "URL": product_url
                        })
                        print(f"[{len(scraped_data)}] Added: {brand} - {numeric_price} EGP")
                        
                except Exception:
                    continue
            
            page_number += 1
            
    finally:
        driver.quit()

    df = pd.DataFrame(scraped_data)
    file_name = "jumia_SmartTVs_Report.csv"
    df.to_csv(file_name, index=False, encoding="utf-8-sig") 
    print(f"\nSaved {len(df)} TVs to {file_name}")
    return df

final_dataset = scrape_jumia_live(target_count=100)
