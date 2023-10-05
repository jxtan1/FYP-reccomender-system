from random import randint
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException

class ScrapeLazada():
    
    def scrape(self):
        try:
            url = 'https://www.lazada.sg/shop-mobiles/?location=local'
            option = webdriver.ChromeOptions()
            option.add_argument('--disable-blink-features=AutomationControlled')
            option.add_argument('start-maximized')
            option.page_load_strategy = 'eager'
            driver = webdriver.Chrome(options=option)
            driver.get(url)
            
            # PART 1 scrape product urls for name, price, soldcount, url
            prodList = []
            try:
                prodDf = pd.read_excel('LazadaProducts.xlsx')
                if not prodDf.empty:
                    prodList = prodDf.values.tolist()
                else:
                    print('Ignoring empty LazadaProducts.xlsx.')
            except Exception as error:
                print(error)
                #print('LazadaProducts.xlsx has not been created yet.')
            reviewList = []
            try:
                reviewDf = pd.read_excel('LazadaReviews.xlsx')
                if not reviewDf.empty:
                    reviewList = reviewDf.values.tolist()
                else:
                    print('Ignoring empty LazadaReviews.xlsx')
            except Exception as error:
                print(error)
                #print('LazadaReviews.xlsx has not been created yet.')

            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.e5J1n")))
            except:
                self.detectCaptcha(driver)
            #for page in range(50):
            for page in range(int(driver.find_elements(By.CSS_SELECTOR, 'div.b7FXJ > div > ul > li > a')[-1].text)):
                self.detectCaptcha(driver)
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#root")))
                #time.sleep(5) # Mandatory wait for page to load
                # Load every single LOVELY product image
                while len(driver.find_elements(By.CSS_SELECTOR, 'div.ICdUp > div._95X4G > a > div > img[src^="data:image"]')) > 0:
                    imgs = driver.find_elements(By.CSS_SELECTOR, 'div.ICdUp > div._95X4G > a > div > img[src^="data:image"]')
                    for img in imgs:
                        try:
                            driver.execute_script("arguments[0].scrollIntoView(true);", img)
                        except StaleElementReferenceException:
                            print(StaleElementReferenceException)
                            break
                
                soup = BeautifulSoup(driver.page_source, "html.parser")
                prodcount = 0
                for product in soup.findAll('div', class_='Bm3ON'):                    
                    prodname = product.find('div', class_='RfADt').text

                    # Check for duplicate
                    if any(prodname == prod[0] for prod in prodList):
                        prodcount += 1
                        # Check if existing product image is an invalid url
                        prods = filter(lambda prod: prod[0] == prodname, prodList)
                        for prod in prods:
                            if ('data:image' in prod[-2]):
                                print('Updating image for ' + str(prodcount + 1) + ' ' + prodname)
                                prod[-2] = product.find('div', class_='picture-wrapper').find('img').get('src')
                        print('Skipping duplicate ' + str(prodcount + 1) + ' ' + prodname)
                        continue

                    price = product.find('span', class_='ooOxS').text.replace('$', '')
                    # Assume failure means product not sold & skip it
                    try:
                        soldcount = product.find('span', class_='_1cEkb').text.replace(' sold', '')
                    except:
                        print('Skipping ' + prodname + ' due to no sales...')
                        continue
                    prodimg = product.find('div', class_='picture-wrapper').find('img').get('src')
                    produrl = 'https:' + product.find('div', class_='RfADt').find('a').get('href')
                    # Check if product has been rated, skip unrated products
                    try:
                        ratings = int(product.find('span', class_='qzqFw').text.replace('(', '').replace(')', '')) # Cannot use data since not accurate by lazada
                    except:
                        print('Skipping ' + prodname + ' due to no reviews')
                        continue
                    
                    # Scrape seller + reviews
                    seller, description = self.scrapeProduct(driver, produrl, reviewList)
                    soup = BeautifulSoup(driver.page_source, "html.parser") # Refresh bs4
                    
                    prodList.append(
                        (prodname, price, soldcount, seller, description, prodimg, produrl)
                        )
                    prodcount += 1
                    print (str(prodcount + 1) + ' ' + prodname + ': ' + produrl)
                #Click next page
                if len(driver.find_elements(By.CSS_SELECTOR, ".ant-pagination-next > button[disabled]"))>0:
                    break # Cannot click next page
                else:
                    button_next=WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".ant-pagination-next > button")))
                    time.sleep(randint(0,2))
                    driver.execute_script("arguments[0].click();", button_next)

        # Always try to save to file
        finally:
            df = pd.DataFrame(prodList, columns=['Product Name', 'Price', 'Total Sold', 'Seller', 'Description', 'Image', 'Product Page'])
            if not df.empty:
                df.drop_duplicates(inplace=True,ignore_index=True)
                print(df)
                df.to_excel('LazadaProducts.xlsx', index=False)

            df = pd.DataFrame(reviewList, columns=['Product Name', 'Rating', 'Reviewer', 'Content'])
            if not df.empty:
                df.drop_duplicates(inplace=True,ignore_index=True)
                df.to_excel('LazadaReviews.xlsx', index=False)
                print('Data saved to excel')

            driver.close()
    
    # PART 2
    def scrapeProduct(self, driver, url, reviewList):
        # Scrape seller & description from product page & reviews from each review page
        driver.execute_script("window.open()") # Make new window
        tabs = driver.window_handles
        driver.switch_to.window(tabs[1]) # Change to new window
        driver.get(url)
        # Wait 5 seconds upon captcha completion
        # if self.detectCaptcha(driver):
        #     time.sleep(5)
        self.detectCaptcha(driver)
        WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.ID, 'module_seller_info')))
        driver.execute_script("arguments[0].scrollIntoView(true);", driver.find_element(By.CSS_SELECTOR, '#module_seller_info > div > div.pdp-seller-info-pc'))
        WebDriverWait(driver,60).until(EC.visibility_of_element_located((By.ID, 'module_product_detail')))
        driver.execute_script("arguments[0].scrollIntoView(true);", driver.find_element(By.ID, 'module_product_detail'))
        #time.sleep(5)
        WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'pdp-product-detail')))
        #driver.execute_script("arguments[0].scrollIntoView(true);", driver.find_element(By.CSS_SELECTOR, '#module_product_detail > div > div'))
        #WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.CLASS_NAME, '#module_product_detail > div > div > div > div.html-content.pdp-product-highlights > ul')))
        soup = BeautifulSoup(driver.page_source, "html.parser")
        # Scrape seller & every review page for product name, rating, reviewer, content
        seller = soup.find('a', class_='seller-name__detail-name').text
        description = soup.find('div', class_='pdp-product-detail').find('ul').text
        print('Description:\n' + description)
        #description = soup.find('div', id='module_product_detail').text
        #Check if there were multiple list items and handle accordingly
        WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.ID, 'module_product_review')))
        #Force scrolling the page to try and load reviews
        driver.execute_script("arguments[0].scrollIntoView(true);", driver.find_element(By.ID, 'module_product_review'))
        reviewcount = 0
        retryPg = 0
        oldPg = 0
        # Loop until no more next review page
        while(True):
            # Attempt to go back one page if captcha was solved
            # if self.detectCaptcha(driver):
            #     button_prev=WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button.next-pagination-item.prev")))
            #     driver.execute_script("arguments[0].click();", button_prev)
            #     oldPg -= 1
            #     continue
            self.detectCaptcha(driver)
            # Skip product review page if no reviews found
            try:
                WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'mod-reviews')))
                driver.execute_script("arguments[0].scrollIntoView(false);", driver.find_element(By.CLASS_NAME, 'review-pagination'))
            except:
                print("Skipping product review page with no reviews...")
                break
            currPg = int(driver.find_element(By.CSS_SELECTOR, 'button.next-pagination-item.current').text)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            WebDriverWait(driver,5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"div.item"))) # Wait for reviews to load
            # Try to click to the next page 3 times if page does not change
            if currPg <= oldPg:
                if retryPg < 3:
                    retryPg += 1
                    button_next=WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button.next-pagination-item.next")))
                    driver.execute_script("arguments[0].click();", button_next)
                    oldPg = currPg
                    continue
                else:
                    print('Failed to click to next page after 3 tries, next product...')
                    break
            prodname = soup.find('h1', class_='pdp-mod-product-badge-title').text
            print('Reading ' + prodname + ' review page ' + str(currPg))
            # Find all reviews in the review page
            for review in soup.findAll('div', class_='item'):
                starsrc = "//laz-img-cdn.alicdn.com/tfs/TB19ZvEgfDH8KJjy1XcXXcpdXXa-64-64.png"
                rating = len(review.find('div', class_='container-star starCtn left').findAll('img', attrs={"class": "star", "src": starsrc}))
                reviewer = review.find('div', class_='middle').find('span').text
                content = review.find('div', class_='content').text
                reviewList.append(
                    (prodname, rating, reviewer, content)
                )
                reviewcount += 1
                print(str(reviewcount) + ' ' + str(rating) + 'stars ' + reviewer + ': ' + content)
            # Attempt to click next review page
            # time.sleep(randint(0, 2)) # Can I remove this since every button press does not require a url request?
            # Break out when next page does not go to the next page (This might be useless unless shifted to before appending)
            if (currPg <= oldPg):
                continue
            # Break out when next page unclickable
            if len(driver.find_elements(By.CSS_SELECTOR, "button.next-pagination-item.next[disabled]"))>0:
                break
            # Continue when next page clickable
            else:
                button_next=WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button.next-pagination-item.next")))
                driver.execute_script("arguments[0].click();", button_next)
                oldPg = currPg
        # Return back to previous window
        driver.close() # Close current window
        driver.switch_to.window(tabs[0]) # Switch back to previous window
        return seller, description
    
    # Review page duplicates before and after captcha appearance
    def detectCaptcha(self, driver):
        captcha = False
        captchaList = ["body > div.J_MIDDLEWARE_FRAME_WIDGET", "body > punish-component", "body > div.J_MIDDLEWARE_FRAME_WIDGET > div > a:contains('关闭')", "div.baxia-dialog[style='display: block;']"]
        #time.sleep(2)
        for captchacss in captchaList:
            try:
                WebDriverWait(driver, 0.25).until(EC.visibility_of_element_located((By.CSS_SELECTOR, captchacss)))
                while len(driver.find_elements(By.CSS_SELECTOR, captchacss)) > 0:
                    print("!!!CAPTCHA!!!")
                    captcha = True
                    #Try to auto solve it (Sliding action detected as a bot...)
                    #driver.switch_to.frame("baxia-dialog-content")
                    #time.sleep(2)
                    #slider = driver.find_element(By.ID, "nc_1_n1z")
                    #x = driver.find_element(By.ID, "nc_1__scale_text").size['width']
                    #action = ActionChains(driver)
                    #Seems to detect actual mouse movement... Could try tweaking actions with some pause() in between
                    #action.move_to_element(slider).click_and_hold(slider).move_by_offset(x, 0).release().perform()
                    #driver.switch_to.default_content()
                    #Try to bring window to front to alert for manual captcha solving
                    driver.switch_to.window(driver.current_window_handle)
                    time.sleep(5) # Delay on captcha detection message
                    
                time.sleep(1) # Wait a moment after captcha is solved
                break # Stop looking for other captchas once one is found
            except:
                captcha = False

        # Return captcha detection status
        return captcha
    
sl = ScrapeLazada()
sl.scrape()