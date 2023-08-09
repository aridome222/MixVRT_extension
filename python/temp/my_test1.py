from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os

if __name__ == '__main__':
    # Selenium サーバへ接続
    options = Options()
    options.add_argument('--headless')  # ヘッドレスモードでブラウザを起動
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Remote(command_executor='http://chrome:4444/wd/hub', options=options)
    driver.implicitly_wait(10)  # 10秒間待機

    try:
        # Googleにアクセス
        driver.get("https://www.google.com/?hl=ja")
        driver.set_window_size(1463, 1039)

        # 検索ボックスに "selenium" と入力して検索
        search_box = driver.find_element(By.NAME, "q")
        search_box.click()
        search_box.send_keys("selenium" + Keys.RETURN)

        # 検索結果ページが表示されるまで待機
        driver.find_element(By.CSS_SELECTOR, ".g > div .kvH3mc .LC20lb")

        # 最初の検索結果のリンクをクリック
        element = driver.find_element(By.CSS_SELECTOR, ".g > div .kvH3mc .LC20lb")
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        element.click()

        # 検索結果のタイトルを出力
        result_elems = driver.find_elements(By.CSS_SELECTOR, ".entry-title.mh-posts-list-title")
        for elem in result_elems:
            print(elem.text)

        # 検索結果の画面キャプチャを取得し保存
        FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img1.png")  # ファイル名
        w = driver.execute_script("return document.body.scrollWidth;")
        h = driver.execute_script("return document.body.scrollHeight;")
        driver.set_window_size(w, h)
        driver.save_screenshot(FILENAME)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
