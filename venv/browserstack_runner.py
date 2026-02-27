import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import BS_USERNAME, BS_ACCESS_KEY

BROWSERSTACK_URL = f"https://{BS_USERNAME}:{BS_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

browsers = [
    {
        "browserName": "Chrome",
        "browserVersion": "latest",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "11",
            "projectName": "El Pais Scraper",
            "buildName": "Opinion Section Analysis",
            "sessionName": "Chrome Test"
        }
    },
    {
        "browserName": "Firefox",
        "browserVersion": "latest",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "10",
            "projectName": "El Pais Scraper",
            "buildName": "Opinion Section Analysis",
            "sessionName": "Firefox Test"
        }
    },
    {
        "browserName": "Edge",
        "browserVersion": "latest",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "11",
            "projectName": "El Pais Scraper",
            "buildName": "Opinion Section Analysis",
            "sessionName": "Edge Test"
        }
    }
]


def run_test(capabilities):
    driver = None
    try:
        options = webdriver.ChromeOptions()
        for key, value in capabilities.items():
            options.set_capability(key, value)

        driver = webdriver.Remote(
            command_executor=BROWSERSTACK_URL,
            options=options
        )

        driver.get("https://elpais.com/opinion/")

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "article"))
        )

        print("Page loaded successfully")

        # Mark as passed
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed","reason": "Page loaded successfully"}}'
        )

    except Exception as e:
        print("Error:", str(e))
        if driver:
            driver.execute_script(
                f'browserstack_executor: {{"action": "setSessionStatus", "arguments": {{"status":"failed","reason": "{str(e)}"}}}}'
            )

    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    threads = []

    for caps in browsers:
        thread = threading.Thread(target=run_test, args=(caps,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("All BrowserStack tests completed.")