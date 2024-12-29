from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
import csv
import re
from datetime import datetime
import sys

sys.stdout.reconfigure(encoding='utf-8')


def scrape_products(driver, data, max_products):
    products_scraped = 0
    while products_scraped < max_products:
        try:
            elements = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, './/span[contains(@class,"productContainer")]'))
                )
            
            for i in range(len(elements)):
                try:
                    elements = driver.find_elements(By.XPATH, './/span[contains(@class,"productContainer")]')
                    element = elements[i]

                    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    product_box = element.find_element(By.XPATH, ".//ancestor::a[contains(@id, 'productBox')]")
                    sku = product_box.get_attribute("id").replace("productBox-", "")
                    
                    full_name = element.find_element(By.XPATH, ".//div[@data-qa='product-name']").text
                    brand_name, product_name = full_name.split('\n', 1) if '\n' in full_name else (full_name, full_name)
                    name = product_name.replace("…","")

                    try:
                        rating = element.find_element(By.XPATH, './/div[(@class= "sc-9cb63f72-2 dGLdNc")]').text
                        rating_count = element.find_element(By.XPATH, './/span[contains(@class,"sc-9cb63f72-5")]').text
                    except:
                        rating = "NA"
                        rating_count = "NA"

                    try:
                        Sponsered_text = element.find_element(By.XPATH, './/div[(@class= "sc-95ea18ef-24 gzboVs")]')
                        if Sponsered_text.text == "Sponsored":
                            Sponsered = "Y"
                        else:
                            Sponsered = "N"
                    except:
                        Sponsered = "N"

                    sales_price = element.find_element(By.XPATH, ".//strong[@class='amount']").text
                    price = element.find_element(By.CLASS_NAME, "oldPrice").text if element.find_elements(By.CLASS_NAME, "oldPrice") else sales_price

                    express = "Y" if element.find_elements(By.XPATH, './/img[@alt="noon-express"]') else "N"

                    try:
                        rank_text = element.find_element(By.XPATH, './/div[@class="sc-4d61bf64-3 bbEraH"]//span[contains(@class, "sc-4d61bf64-5")]').text
                        rank_match = re.match(r"#(\d+)", rank_text)
                        if rank_match:
                            Rank = rank_match.group(1)
                        else:
                            Rank = "NA"
                    except:
                        Rank = "NA"

                    product_url = product_box.get_attribute('href') or "NA"

                    data.append({
                        "Date & Time": date_time,
                        "sku": sku,
                        "name": name,
                        "brand": brand_name,
                        "Average Rating": rating,
                        "Rating Count": rating_count,
                        "Sponsered": Sponsered,
                        "price": price,
                        "Sales Price": sales_price,
                        "Express": express,
                        "Rank": Rank,
                        "Link": product_url,
                    })
                    products_scraped += 1
                    print(f"Product {products_scraped}: {product_name} scraped.")
                    if products_scraped >= max_products:
                        break

                except StaleElementReferenceException:
                    print("Stale element detected, retrying...")
                except Exception as e:
                    print(f"Error occurred: {e}")

            try:
                next_page_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//li[@class='next']/a[@class='arrowLink']"))
                )
                next_page_button.click()
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, './/span[contains(@class,"productContainer")]'))
                )
            except TimeoutException:
                print("No more pages available or timeout occurred.")
                break

        except Exception as e:
            print(f"Error in main scraping loop: {e}")
            break


def write_to_csv(data):
    with open('noon_products.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [ 'Date & Time', 'sku', 'name', 'brand', 'Average Rating', 'Rating Count', 'Sponsered', 'price', 'Sales Price', 'Express', 'Rank', 'Link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.get("https://www.noon.com/uae-en/sports-and-outdoors/exercise-and-fitness/yoga-16328/")

    scraped_data = []
    max_products = 200
    scrape_products(driver, scraped_data, max_products)
    print(f"{len(scraped_data)} products scraped.")
    write_to_csv(scraped_data)
    print("Product data saved to CSV file.")
    driver.quit()