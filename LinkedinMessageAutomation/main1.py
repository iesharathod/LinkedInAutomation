from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tabulate import tabulate
from selenium.webdriver.common.by import By
from selenium import webdriver


chrome_driver_path= "C:\Users\ishar\OneDrive\Desktop\chromedriver-win64\chromedriver"
driver = webdriver.Chrome(executable_path=chrome_driver_path)
driver.get("https://www.linkedin.com/")
