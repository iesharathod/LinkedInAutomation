from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import csv
import time


# Correct file path with .exe extension
chrome_driver_path = r"C:\Users\ishar\OneDrive\Desktop\chromedriver-win64\chromedriver.exe"

def configurations():
    options = Options()
    # opens the window in full screen
    options.add_argument("--start-maximized")

    # Specify the path to the chromedriver executable using Service
    service = Service(chrome_driver_path)

    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Example usage
if __name__ == "__main__":
    driver = configurations()
    driver.get("https://www.google.com")
    print(driver.title)
    driver.quit()

# this class deals with the CSV file operations like opening the file, setting up the writer, inserting new row, etc.
class Csv_io:
    def __init__(self, filename, mode, newline):
        self.filename = filename
        self.mode = mode
        self.newline = newline

        self.openfile()
        self.writer_setup()

    # opens file
    def openfile(self):
        self.file_to_write = open(self.filename, mode=self.mode, newline=self.newline)

    # initialises the writer object
    def writer_setup(self):
        self.csv_writer = csv.writer(self.file_to_write)

    # inserts a new row into the CSV file
    def insert_row(self, info):
        self.csv_writer.writerow(info)

    def __str__(self):
        return 'this class deals with the CSV file operations'

# this class deals with the DOM operations like grabbing the elements using selectors, clicking on elements, sending text to elements, etc.
class Webpage:
    def __init__(self, driver):
        self.driver = driver

    # opens the given url
    def visit(self, url):
        self.driver.get(url)

    def click_with_xpath_selector(self, xpath_selector):
        self.driver.find_element_by_xpath(xpath_selector).click()

    # clicks the element selected using CSS Selector
    def click_with_css_selector(self, css_selector):
        self.driver.find_element_by_css_selector(css_selector).click()

    # gets the element selected using CSS Selector
    def grab_element_with_css_selector(self, css_selector):
        return self.driver.find.elements(css_selector)

    # gets the elements* selected using CSS Selector
    def grab_elements_with_css_selector(self, css_selector):
        return self.driver.find_elements_by_css_selector(css_selector)

    # sends the entered text to the element selected using CSS Selector
    def type_value_with_css_selector(self, css_selector, keys):
        self.driver.find_element_by_css_selector(css_selector).send_keys(keys)

    # gets the text from the element selected using CSS Selector
    def grab_text_with_css_selector(self, css_selector):
        return self.driver.find_element_by_css_selector(css_selector).text

    # returns the url of the current page
    def get_url(self):
        return self.driver.current_url

# this class deals with the browser operations like ending the session, going back to previous page, wait, etc.
class Browser:
    def __init__(self, driver):
        self.driver = driver

    # end the current session
    def end_session(self):
        self.driver.quit()

    # go back to previous page
    def go_back(self):
        self.driver.back()

    # wait/sleep for given time
    def wait(self, duration):
        self.driver.implicitly_wait(duration)

# this is the user class
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

# logs text onto python console
def log(text):
    print(text)

# main function
def main():
    driver = configurations()
    webpage = Webpage(driver)
    browser = Browser(driver)

    user = User("your_username", "your_password")
    csv_io = Csv_io('OutputFolder/dataset.csv', 'a', '')

    browser.wait(2)

    webpage.visit("https://www.linkedin.com/login")

    webpage.type_value_with_css_selector("input[id='username']", user.username)
    webpage.type_value_with_css_selector("input[id='password']", user.password)
    webpage.click_with_css_selector("button[type='submit']")

    for keyword in ["example1", "example2"]:  # Replace with your actual keywords
        for page in range(1, 3):  # Adjust the range as needed
            time.sleep(2)

            link = f"https://www.linkedin.com/search/results/people/?keywords={keyword}&origin=CLUSTER_EXPANSION&page={page}"
            webpage.visit(link)

            list_of_cards = webpage.grab_elements_with_css_selector("li[class='reusable-search__result-container ']")

            log(f"a total of {len(list_of_cards)} Connections found on page {page} for {keyword}")

            for i in range(1, len(list_of_cards) + 1):
                time.sleep(2)

                try:
                    button_on_card = webpage.grab_element_with_css_selector(
                        f"li[class= 'reusable-search__result-container ']:nth-child({i}) button").is_enabled()

                    button_text = webpage.grab_text_with_css_selector(
                        f"li[class= 'reusable-search__result-container ']:nth-child({i}) button span")

                    if button_on_card and button_text == 'Connect':
                        time.sleep(1)
                        webpage.click_with_css_selector(
                            f"li[class= 'reusable-search__result-container ']:nth-child({i}) span a span span")

                        time.sleep(2)

                        name_grab = webpage.grab_text_with_css_selector("h1")
                        browser.wait(10)
                        connect_xpath = "/html[1]/body[1]/div[6]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/main[1]/section[1]/div[2]/div[3]/div[1]/button[1]"
                        webpage.click_with_xpath_selector(connect_xpath)
                        time.sleep(2)

                        webpage.click_with_css_selector("button[aria-label='Send now']")

                        description1 = webpage.grab_text_with_css_selector("div[class= 'text-body-medium break-words']")
                        description2 = webpage.grab_text_with_css_selector("span[class = 'text-body-small inline t-black--light break-words']")

                        link_to_profile = webpage.get_url()

                        time.sleep(1)

                        log(f"{name_grab} who is {description1} at {description2} for profile {link_to_profile}")

                        info = [name_grab, description1, description2, link_to_profile]

                        csv_io.insert_row(info)

                        time.sleep(1)

                    webpage.visit(link)
                    browser.wait(10)

                except NoSuchElementException:
                    pass
                except Exception as e:
                    log(e)

        log("All New Connection's data appended to dataset.csv")

    browser.end_session()
    csv_io.insert_row(["---------", "----------", "----------", "-------------"])
import os

output_folder = 'OutputFolder'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

if __name__ == "__main__":
    main()
