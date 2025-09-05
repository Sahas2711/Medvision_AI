#!/usr/bin/env python3
"""
Screenshot Capture Script for Aarogya Drishti
This script helps capture screenshots of the application for README documentation
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    """Setup Chrome driver with appropriate options"""
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"Error setting up Chrome driver: {e}")
        print("Please install ChromeDriver and ensure it's in your PATH")
        return None

def capture_screenshots():
    """Capture screenshots of different application views"""
    
    # Create screenshots directory
    screenshots_dir = "screenshots"
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)
    
    driver = setup_driver()
    if not driver:
        return
    
    try:
        # Navigate to the application
        app_url = "file://" + os.path.abspath("frontend/index.html")
        driver.get(app_url)
        
        # Wait for page to load
        time.sleep(3)
        
        # 1. Main Dashboard
        print("Capturing main dashboard...")
        driver.save_screenshot(f"{screenshots_dir}/01_main_dashboard.png")
        
        # 2. Upload Modal
        print("Capturing upload interface...")
        upload_btn = driver.find_element(By.CSS_SELECTOR, ".btn-primary")
        upload_btn.click()
        time.sleep(2)
        driver.save_screenshot(f"{screenshots_dir}/02_upload_interface.png")
        
        # Close modal
        close_btn = driver.find_element(By.CSS_SELECTOR, ".close")
        close_btn.click()
        time.sleep(1)
        
        # 3. Features Section
        print("Capturing features section...")
        driver.execute_script("document.getElementById('features').scrollIntoView();")
        time.sleep(2)
        driver.save_screenshot(f"{screenshots_dir}/03_ai_modules.png")
        
        # 4. Disease Information Section
        print("Capturing disease information...")
        driver.execute_script("document.getElementById('diseases').scrollIntoView();")
        time.sleep(2)
        driver.save_screenshot(f"{screenshots_dir}/04_disease_info.png")
        
        # 5. Precaution Hub
        print("Capturing precaution hub...")
        driver.execute_script("document.querySelector('.precaution-hub').scrollIntoView();")
        time.sleep(2)
        driver.save_screenshot(f"{screenshots_dir}/05_precaution_hub.png")
        
        # 6. Doctor Finder (if available)
        try:
            doctor_finder_url = "file://" + os.path.abspath("frontend/doctor-finder.html")
            driver.get(doctor_finder_url)
            time.sleep(3)
            print("Capturing doctor finder...")
            driver.save_screenshot(f"{screenshots_dir}/06_doctor_finder.png")
        except:
            print("Doctor finder page not found, skipping...")
        
        print(f"\nScreenshots saved in '{screenshots_dir}' directory!")
        print("You can now replace the placeholder images in README.md with these actual screenshots.")
        
    except Exception as e:
        print(f"Error capturing screenshots: {e}")
    
    finally:
        driver.quit()

def create_screenshot_guide():
    """Create a guide for updating README with actual screenshots"""
    
    guide_content = """
# Screenshot Update Guide

After running the screenshot capture script, follow these steps to update your README.md:

## 1. Upload Screenshots to GitHub
1. Create a `screenshots` folder in your repository
2. Upload all captured screenshots to this folder
3. Note the GitHub raw URLs for each image

## 2. Update README.md Image Links
Replace the placeholder image URLs with your actual screenshot URLs:

### Main Dashboard
```markdown
![Main Dashboard](https://raw.githubusercontent.com/yourusername/Medvision_AI/main/screenshots/01_main_dashboard.png)
```

### Upload Interface
```markdown
![Upload Interface](https://raw.githubusercontent.com/yourusername/Medvision_AI/main/screenshots/02_upload_interface.png)
```

### AI Modules
```markdown
![AI Modules](https://raw.githubusercontent.com/yourusername/Medvision_AI/main/screenshots/03_ai_modules.png)
```

### Disease Information
```markdown
![Disease Info](https://raw.githubusercontent.com/yourusername/Medvision_AI/main/screenshots/04_disease_info.png)
```

### Precaution Hub
```markdown
![Precaution Hub](https://raw.githubusercontent.com/yourusername/Medvision_AI/main/screenshots/05_precaution_hub.png)
```

### Doctor Finder
```markdown
![Doctor Finder](https://raw.githubusercontent.com/yourusername/Medvision_AI/main/screenshots/06_doctor_finder.png)
```

## 3. Add Analysis Result Screenshots
To capture analysis results:
1. Run your application
2. Upload sample medical images
3. Capture screenshots of the results
4. Add them to the README under the respective model sections

## 4. Alternative: Use GitHub Issues for Image Hosting
1. Create a new issue in your repository
2. Drag and drop images into the issue description
3. Copy the generated URLs
4. Use these URLs in your README
5. You can close the issue after copying URLs

## 5. Tips for Better Screenshots
- Use high-resolution displays (1920x1080 or higher)
- Ensure good lighting and contrast
- Capture full-screen views for better visibility
- Include sample data/results for demonstration
- Consider creating GIFs for interactive features
"""
    
    with open("SCREENSHOT_GUIDE.md", "w") as f:
        f.write(guide_content)
    
    print("Screenshot guide created: SCREENSHOT_GUIDE.md")

if __name__ == "__main__":
    print("Aarogya Drishti Screenshot Capture Tool")
    print("=" * 40)
    
    print("\nThis script will capture screenshots of your application.")
    print("Make sure your application is running and accessible.")
    
    choice = input("\nDo you want to:\n1. Capture screenshots\n2. Create screenshot guide\n3. Both\nEnter choice (1/2/3): ")
    
    if choice in ["1", "3"]:
        print("\nStarting screenshot capture...")
        capture_screenshots()
    
    if choice in ["2", "3"]:
        print("\nCreating screenshot guide...")
        create_screenshot_guide()
    
    print("\nDone! Check the generated files and follow the guide to update your README.")