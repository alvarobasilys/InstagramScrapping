# InstagramScrapping

Get post link, total like, total comment, and post caption.

## Getting Started
1. Install all requirement libraries 
```
pip install -r requirement.txt
```
2. The default web driver used in this program is **Microsoft Edge** (you can skip this point if you using Microsoft Edge browser) and if you using **another browser (Google Chrome, Mozilla Firefox, etc)**, please download the web driver first from this following links:

| Browser           | Supported OS               | Maintained by    | Download                                                                            | Issue Tracker |
|-------------------|----------------------------|------------------|-------------------------------------------------------------------------------------|---------------|
| Chromium/Chrome   | Windows/macOS/Linux        | Google           | [Downloads](https://chromedriver.storage.googleapis.com/index.html)                 | [Issues](https://bugs.chromium.org/p/chromedriver/issues/list)        |
| Firefox           | Windows/macOS/Linux        | Mozilla          | [Downloads](https://github.com/mozilla/geckodriver/releases)                        | [Issues](https://github.com/mozilla/geckodriver/issues)        |
| Edge              | Windows 10                 | Microsoft        | [Downloads](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)  | [Issues](https://developer.microsoft.com/en-us/microsoft-edge/platform/issues/?page=1&q=webdriver)        |
| Internet Explorer | Windows                    | Selenium Project | [Downloads](https://selenium-release.storage.googleapis.com/index.html)             | [Issues](https://github.com/SeleniumHQ/selenium/labels/D-IE)        |
| Safari            | macOS El Capitan and newer | Apple            | Built in                                                                            | [Issues](https://bugreport.apple.com/logon)        |
| Opera             | Windows/macOS/Linux        | Opera            | [Downloads](https://github.com/operasoftware/operachromiumdriver/releases)          | [Issues](https://github.com/operasoftware/operachromiumdriver/issues)        |

3. After download the web driver, please open `InstagramScrapping.py` in code editor and **change Line 23** with this code. 

| Browser           | Code                                                               |
|-------------------|--------------------------------------------------------------------|
| Chromium/Chrome   | `self.driver = webdriver.Chrome(executable_path=<webdriver_dir>)`  |
| Firefox           | `self.driver = webdriver.Firefox(executable_path=<webdriver_dir>)` |
| Edge              | `self.driver = webdriver.Edge(executable_path=<webdriver_dir>)`    |
| Internet Explorer | `self.driver = webdriver.Ie(executable_path=<webdriver_dir>)`      |
| Safari            | `self.driver = webdriver.Safari()`                                 |
| Opera             | `self.driver = webdriver.Opera(executable_path=<webdriver_dir>)`   |

## How to use this program
Now you can open your terminal and try to start with following this command:
```
python InstagramScrapping.py -user_info "your_username","your_password" -target_link "https://www.instagram.com/instagram/" -load_loop 3 -csv_path "instagram.csv"
```
there're several variables that you can set, just run `python InstagramScrapping.py -help` command
