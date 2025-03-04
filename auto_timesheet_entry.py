from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime

try:
    from config import UNANET_URL, PROJECT_CODE, HOURS_TO_ENTER
except ImportError:
    print("Config file not found. Please create config.py with your settings:")
    print("UNANET_URL = 'your-unanet-url'")
    print("PROJECT_CODE = 'your-project-code'")
    print("HOURS_TO_ENTER = '8'")
    exit(1)

def wait_and_find_element(driver, by, value, timeout=10):
    """Wait for an element to be present and return it."""
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )

def enter_timesheet_hours(driver):
    """Enter specified hours for today in the project row and save."""
    print(f"\nEntering {HOURS_TO_ENTER} hours for today in project row...")
    
    try:
        # Get today's date info
        today = datetime.now()
        target_day_str = str(today.day)
        weekday_abbr = today.strftime("%a").upper()
        print(f"Looking for cell: {weekday_abbr} {target_day_str}")
        
        # Find all header cells to determine column index
        all_headers = driver.find_elements(By.XPATH, "//th[contains(@class, 'hours-weekday')]")
        
        # Find our target header
        column_index = None
        for i, header in enumerate(all_headers):
            try:
                dow = header.find_element(By.CLASS_NAME, "dow").text
                dom = header.find_element(By.CLASS_NAME, "dom").text
                if dow == weekday_abbr and dom == target_day_str:
                    column_index = i
                    print(f"Found today's column at index: {i}")
                    break
            except:
                continue
                
        if column_index is None:
            print("Could not find today's date in headers")
            return False
        
        # Find the timesheet table
        timesheet = driver.find_element(By.ID, "timesheet")
        
        # Find all project rows
        rows = timesheet.find_elements(By.XPATH, ".//tbody/tr[.//td[contains(@class, 'project')]]")
        
        # Look for project row
        for row in rows:
            try:
                project_cell = row.find_element(By.CSS_SELECTOR, "td.project")
                project_input = project_cell.find_element(By.CSS_SELECTOR, "input.ui-autocomplete-input")
                value = project_input.get_attribute("value").strip()
                
                if value == PROJECT_CODE:
                    print("Found project row, looking for today's cell...")
                    
                    # Get all cells in this row
                    cells = row.find_elements(By.TAG_NAME, "td")
                    
                    # Find first weekday-hours cell
                    first_weekday_index = None
                    for i, cell in enumerate(cells):
                        if 'weekday-hours' in cell.get_attribute('class'):
                            first_weekday_index = i
                            break
                            
                    if first_weekday_index is None:
                        print("Could not find weekday cells")
                        return False
                        
                    # Get target cell
                    target_cell_index = first_weekday_index + column_index
                    target_cell = cells[target_cell_index]
                    
                    # Find and update hours input
                    input_field = target_cell.find_element(By.CSS_SELECTOR, "input.hours")
                    print("Found input field...")
                    
                    # Scroll into view and focus
                    driver.execute_script("arguments[0].scrollIntoView(true);", input_field)
                    time.sleep(0.5)
                    
                    # Enter hours
                    input_field.click()
                    driver.execute_script("arguments[0].focus();", input_field)
                    time.sleep(0.5)
                    input_field.clear()
                    time.sleep(0.5)
                    input_field.send_keys(HOURS_TO_ENTER)
                    time.sleep(0.5)
                    
                    # Verify entry
                    current_value = input_field.get_attribute("value").strip()
                    print(f"Current value after entry: '{current_value}'")
                    
                    if current_value == HOURS_TO_ENTER:
                        # Save the timesheet
                        print("\nSaving timesheet...")
                        save_button = wait_and_find_element(
                            driver,
                            By.NAME,
                            "button_save"
                        )
                        save_button.click()
                        print("Clicked Save button")
                        time.sleep(2)
                        print("Save completed")
                        return True
                    
            except Exception as e:
                continue
                
        print("Could not find project row")
        return False
        
    except Exception as e:
        print(f"Error entering hours: {str(e)}")
        return False

def main():
    print("Starting Chrome automation...")

    # Connect to existing Chrome
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    try:
        driver = webdriver.Chrome(options=options)
        print("Successfully connected to existing Chrome!")
        
        # Open Unanet in new tab
        print("\nOpening new tab...")
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        
        print("Navigating to Unanet timesheet...")
        driver.get(UNANET_URL)
        
        # Wait for page load
        print("Waiting for page to load...")
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        print("Page loaded successfully!")
        
        # Check if we need to login
        try:
            username_field = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            print("Login page detected, please log in manually and run the script again.")
            return
        except:
            print("Already logged in, proceeding...")
        
        # Navigate to Current timesheet
        print("Looking for Time tab...")
        time_tab = wait_and_find_element(
            driver,
            By.XPATH,
            "//a[contains(@class, 'ui-menu-item-wrapper') and contains(text(), 'Time')]"
        )
        driver.execute_script("arguments[0].click();", time_tab)
        print("Clicked Time tab")
        
        # Wait for dropdown
        time.sleep(2)
        
        # Click Current
        print("Looking for Current in dropdown...")
        try:
            current_option = wait_and_find_element(
                driver,
                By.XPATH,
                "//a[contains(@class, 'ui-menu-item-wrapper') and text()='Current']"
            )
            driver.execute_script("arguments[0].click();", current_option)
        except:
            submenu = wait_and_find_element(
                driver,
                By.XPATH,
                "//ul[contains(@class, 'ui-menu-submenu')]"
            )
            current_option = submenu.find_element(By.XPATH, ".//a[text()='Current']")
            driver.execute_script("arguments[0].click();", current_option)
        print("Clicked Current option")
        
        # Wait for timesheet load
        time.sleep(5)
        
        # Enter and save hours
        enter_timesheet_hours(driver)
            
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    main()
