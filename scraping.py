import time
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Scraper:
    def __init__(self, player_id):
        self.player_id = player_id
        self.card_data_dict = {}
        self.options = Options()
        self.options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(options=self.options)
        self.wait = WebDriverWait(self.driver, 10)

    def run(self):
        try:
            self.driver.get('https://www.midasbuy.com/midasbuy/jo/buy/pubgm')
            print('Driver created and page loaded')
            self.accept_cookies()
            # self.login_user()
            # self.driver.refresh()
            # self.close_next_adds()
            player_name = self.add_user_id()
            return player_name
        finally:
            time.sleep(20)
            self.driver.quit()

    def close_adds(self):
        try:
            close_btn = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[@class='PopVipRecommendLogin_close__l+yAq']//i[@class='i-midas:error icon']")))
            ActionChains(self.driver).move_to_element(close_btn).click(close_btn).perform()
            time.sleep(1)
        except Exception as e:
            print('Close button not found', e)

    def close_next_adds(self):
        try:
            close_btn = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[@class='PatFacePopWrapper_close-btn__erWAb']")))
            ActionChains(self.driver).move_to_element(close_btn).click(close_btn).perform()
            time.sleep(1)
        except Exception as e:
            print('Next close button not found', e)

    def accept_cookies(self):
        self.driver.set_window_size(1920, 1080)
        try:
            self.close_adds()
            cookies_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[11]/div[3]/div[1]/div/div")))
            ActionChains(self.driver).move_to_element(cookies_btn).click(cookies_btn).perform()
            time.sleep(1)
        except Exception as e:
            print('Cookies button not found', e)

    def login_user(self):
        try:
            login_main_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[1]/div/div[2]/div[4]")))
            login_main_btn.click()
            time.sleep(1)

            iframe = self.wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[@id='login-iframe']")))
            self.driver.switch_to.frame(iframe)
            print('iframe found')

            try:
                email_field = self.driver.find_element(By.XPATH, ".//input[@type='email']")
                email_field.send_keys('ahmad.mhanna954@gmail.com')
                time.sleep(1)

                continue_button = self.driver.find_element(By.XPATH, ".//div[@class='btn comfirm-btn']")
                continue_button.click()
                time.sleep(1)

                password_field = self.driver.find_element(By.XPATH, ".//input[@type='password']")
                password_field.send_keys('Zzz@1234')
                time.sleep(1)

                signin_button = self.driver.find_element(By.XPATH, ".//div[@class='btn comfirm-btn']")
                signin_button.click()
                time.sleep(5)
            except Exception as e:
                print("login not found", e)

        except (NoSuchElementException, TimeoutException) as e:
            print("iframe not found", e)

    def add_user_id(self):
        try:
            try:
                add_user_id_btn = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//div[@class='UserTabBox_login_text__8GpBN']")))
                ActionChains(self.driver).move_to_element(add_user_id_btn).click(add_user_id_btn).perform()
                print('Add user button clicked')
            except Exception as e:
                print('Add user button not found', e)
                try:
                    add_other_user_id_btn = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//span[@class='UserTabBox_switch_btn__428iM']")))
                    ActionChains(self.driver).move_to_element(add_other_user_id_btn).click(
                        add_other_user_id_btn).perform()
                    print('Switch user button clicked')
                except Exception as e:
                    print('Other user button not found', e)
                    raise Exception("Unable to find a button to add or switch user ID.")

            input_field = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='Input_input__s4ezt']//input[@type='text']")))
            input_field.clear()
            input_field.click()
            input_field.send_keys(f"{self.player_id}")
            time.sleep(1)

            # Click the submit button
            submit_btn = self.wait.until(EC.presence_of_element_located(
                (By.XPATH,
                 "//div[@class='BindLoginPop_btn_wrap__eiPwz']//div[@class='Button_btn__P0ibl Button_btn_primary__1ncdM']")))
            ActionChains(self.driver).move_to_element(submit_btn).click(submit_btn).perform()

            try:
                player_name = self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//div[@class='UserTabBox_user_head_text__M0ViN']//span[@class='UserTabBox_name__4ogGM']")))
                print("Player name found:", player_name.text)
                return player_name.text
            except Exception as e:
                print('Invalid player id', e)
                return "Invalid player id"

        except Exception as e:
            print('Error in adding user ID:', e)
            return None


class CardScraper:
    def __init__(self, player_id, item_id):
        self.player_id = player_id
        self.item_id = int(item_id)
        self.card_data_dict = {}
        self.options = Options()
        self.options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(options=self.options)
        self.wait = WebDriverWait(self.driver, 10)

    def run(self):
        try:
            self.driver.get('https://www.midasbuy.com/midasbuy/jo/buy/pubgm')
            print('Driver created and page loaded')
            self.accept_cookies()
            # self.driver.refresh()
            # self.close_next_adds()
            self.get_card_data()
            return self.card_data_dict
        finally:
            time.sleep(20)
            self.driver.quit()

    def close_adds(self):
        try:
            close_btn = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[@class='PopVipRecommendLogin_close__l+yAq']//i[@class='i-midas:error icon']")))
            ActionChains(self.driver).move_to_element(close_btn).click(close_btn).perform()
            time.sleep(1)
        except Exception as e:
            print('Close button not found', e)

    def close_next_adds(self):
        try:
            close_btn = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[@class='PatFacePopWrapper_close-btn__erWAb']")))
            ActionChains(self.driver).move_to_element(close_btn).click(close_btn).perform()
            time.sleep(1)
        except Exception as e:
            print('Next close button not found', e)

    def accept_cookies(self):
        self.driver.set_window_size(1920, 1080)
        try:
            self.close_adds()
            cookies_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[11]/div[3]/div[1]/div/div")))
            ActionChains(self.driver).move_to_element(cookies_btn).click(cookies_btn).perform()
            time.sleep(1)
        except Exception as e:
            print('Cookies button not found', e)

    def get_card_data(self):
        try:
            data_dict = {}
            main_card_div = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='abTest_type_have_filter__LAY20 abTest_recharge_class_box__lK8IP  abTest_type_gifts__BA+Q6 ']")))

            for index, card in enumerate(main_card_div):
                ActionChains(self.driver).move_to_element(card).perform()
                card_discount = card.find_element(By.XPATH, ".//div[@class='abTest_discountTag_num__LCFLo']")
                card_uc = card.find_element(By.XPATH, ".//div[@class='abTest_val__wyibD']")
                card_price = card.find_element(By.XPATH, ".//div[@class='abTest_price__sww4i abTest_discount__oplOy']//div")
                if index == (self.item_id - 1):
                    data_dict['card discount'] = card_discount.text
                    data_dict['card uc'] = card_uc.text
                    data_dict['card price'] = card_price.text
                    self.card_data_dict[index] = data_dict
                    print(index, 'card data', card_discount.text)
                    break
                time.sleep(1)

        except Exception as e:
            print('Card data not found', e)


# player_id = '5240037068'
# scraper = Scraper(player_id=player_id)
# scraper.run()
