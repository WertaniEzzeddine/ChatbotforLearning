import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-extensions")
options.add_argument("--disable-popup-blocking")
driver = webdriver.Chrome(options=options)


# Helper function to generate unique credentials
def generate_unique_credentials():
    timestamp = int(time.time())
    full_name = f"Test User {timestamp}"
    email = "test1597@gmail.com"
    password = "password123"  # Use a fixed password for simplicity
    return full_name, email, password

# Set up WebDriver

driver.get("http://localhost:4200")  # Open the main page, assuming it redirects to the signup page

try:
    # Step 1: Wait for the signup button to appear and click it
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".auth-buttons .signup-btn"))
    )
    signup_button = driver.find_element(By.CSS_SELECTOR, ".auth-buttons .signup-btn")
    signup_button.click()

    # Step 2: Wait for the Signup Page to Load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "signup-box"))
    )

    # Generate unique credentials
    full_name, email, password = generate_unique_credentials()

    # Step 3: Fill out the Signup Form
    full_name_input = driver.find_element(By.CSS_SELECTOR, "input[name='fullName']")
    email_input = driver.find_element(By.CSS_SELECTOR, "input[name='email']")
    password_input = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
    register_button = driver.find_element(By.CSS_SELECTOR, ".register-btn")

    # Use JavaScript to set the value if send_keys is not working
    full_name_input.send_keys(full_name)
    email_input.send_keys(email)
    password_input.send_keys(password)
   
    # Click the register button
    register_button.click()
    time.sleep(2)
    print(f"Registration successful for: {full_name}, {email}")
    # Open the webpage
     # Replace with your actual URL
    # Wait for the email input to be visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "email"))
    )
    # Find and fill the email field
    email_input = driver.find_element(By.NAME, "email")
    email_input.send_keys("test1597@gmail.com")  # Replace with test email

    # Find and fill the password field
    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys("password123")  # Replace with test password

    # Find and click the login button
    login_button = driver.find_element(By.CLASS_NAME, "loginn-btn")
    login_button.click()    
    time.sleep(3)
    print("Login test passed.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the browser
    driver.quit()