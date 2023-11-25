from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

class TestA():
    def setup_method(self, method):
        options = Options()
        # options.add_argument('--headless')  # ヘッドレスモードでブラウザを起動
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Remote(command_executor='http://chrome:4444/wd/hub', options=options)
        self.driver.implicitly_wait(10)  # 10秒まで待機する
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_a(self):
        self.driver.get("https://staging-user.photolize.jp/login")
        self.driver.get("http://saruya:saruya@photolize.jp/login")  # Basic認証
        self.driver.set_window_size(1463, 1039)
        self.input_and_click(By.ID, "input-7", ".v-btn__content", "company_code26")
        self.input(By.ID, "input-11", "aridome")
        self.input(By.ID, "input-14", "aridome")
        self.driver.find_element(By.CSS_SELECTOR, ".btn > .v-btn__content").click()

    def input(self, by, element_id, value):
        self.driver.find_element(by, element_id).send_keys(value)

    def input_and_click(self, by, input_id, click_selector, value):
        self.driver.find_element(by, input_id).click()
        element = self.driver.find_element(By.CSS_SELECTOR, click_selector)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(by, input_id).send_keys(value)
        element.click()

if __name__ == '__main__':
    options = Options()
    options.add_argument('--headless')  # ヘッドレスモードでブラウザを起動
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Remote(command_executor='http://chrome:4444/wd/hub', options=options)
    driver.implicitly_wait(10)  # 10秒間待機

    try:
        test_a = TestA()
        test_a.driver = driver
        test_a.test_a()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()