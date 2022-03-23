import os
import json
import time

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

options = Options()
# options.headless = True
options.binary_location = (
    "C:\\Users\\zarif\\AppData\\Local\\Firefox Nightly\\firefox.exe"
)
s = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(options=options, service=s)

EPISODE_NO = 1
BASE_DIR = os.getcwd()
BASE_URL = "https://onepiece.fandom.com/wiki"

os.makedirs(f"{BASE_DIR}/episodes") if not os.path.isdir(
    f"{BASE_DIR}/episodes"
) else None

try:

    while True:
        driver.get(f"{BASE_URL}/Episode_{EPISODE_NO}")

        with open("test.html", "w+", encoding="utf-8") as f:
            f.write((driver.page_source))

        delay = 5  # seconds
        try:
            short_summary = WebDriverWait(driver, delay).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[4]/div[3]/div[3]/main/div[3]/div[2]/div/p[4]",
                    )
                )
            )

            long_summary = ""
            long_summary_elements = driver.find_elements(
                By.CSS_SELECTOR, ".mw-parser-output > h2:nth-child(9) ~ p"
            )
            for i in long_summary_elements:
                long_summary += i.text
                long_summary += "\n"

            # anime_notes = ""
            # anime_notes_parent = driver.find_element(
            #     By.XPATH,
            #     "/html/body/div[4]/div[3]/div[2]/main/div[3]/div[2]/div/ul[2]",
            # )

            # print(anime_notes_parent)
            # anime_notes_element = anime_notes_parent.find_elements_by_tag_name("li")

            # for i in anime_notes_element:
            #     anime_notes += i.text
            #     anime_notes += "\n"

            print(f"Got info for {EPISODE_NO}")

        except TimeoutException:
            print("Loading took too much time!")

        finally:
            data = {
                "episode": EPISODE_NO,
                "short_summary": short_summary.text,
                "long_summary": long_summary,
                # "anime_notes": anime_notes,
            }
            json.dump(
                data, open(f"{BASE_DIR}/episodes/{EPISODE_NO}.json", "w+"), indent=4
            )
            time.sleep(2)
            EPISODE_NO += 1


finally:
    driver.close()
