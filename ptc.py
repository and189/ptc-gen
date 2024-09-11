import subprocess
import sys
import os
import random
import string
import time
import csv
import re
import imaplib
import email
import traceback
from datetime import datetime, timedelta
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# List of required packages
required_packages = [
    'random', 'time', 'undetected_chromedriver', 'selenium', 'os', 
    're', 'imaplib', 'email', 'csv', 'datetime', 'traceback'
]

def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        print(f"{package} not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"{package} installed successfully!")

# Install all required packages if they are missing
for package in required_packages:
    install_and_import(package)

# Configuration Section
EMAIL_CONFIG = {
    "user": "xxxx@gmail.com",
    "password": "xxxx xxxx xxxx xxxxx",
    "imap_host": "imap.gmail.com",
    "target_sender": "no-reply@tmi.pokemon.com"
}

DOMAIN_CONFIG = {
    "domains": ["kwstaylor.eu", "impreva.eu"]
}

PROXY_STATS_FILE = 'proxy_stats.csv'
PROXY_FILE = 'proxies.txt'
BLOCKED_PROXIES_FILE = 'blocked_proxies.txt'
LAST_PROXY_FILE = 'last_proxy.txt'

def save_account_to_csv(email, username, password, pin):
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    csv_file = 'accounts.csv'
    
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(['Email', 'Username', 'Password', 'PIN', 'Proxy', 'Date', 'Time'])
        writer.writerow([email, username, password, pin, proxy, date_time])
    
    print(f"Account saved to {csv_file}: {email}, {username}, {password}, {pin}, {date_time}")

def generate_random_birthdate():
    current_year = datetime.now().year
    year = random.randint(current_year - 35, current_year - 18)
    months = ["January", "February", "March", "April", "May", "June", 
              "July", "August", "September", "October", "November", "December"]
    month = random.choice(months)
    
    if month == "February":
        day = random.randint(1, 29) if year % 4 == 0 else random.randint(1, 28)
    elif month in ["April", "June", "September", "November"]:
        day = random.randint(1, 30)
    else:
        day = random.randint(1, 31)
    
    print(f"Generated random birthdate: {year}-{month}-{day}")
    return year, month, day

def get_random_name():
    first_names = [
        "Max", "Lukas", "Felix", "Jonas", "Leon", "Emma", "Anna", "Sophia", "Mia", "Noah", "Paul", "Elias", 
        "Lena", "Marie", "Clara", "Finn", "Ben", "Tom", "Julia", "Lea", "Erik", "Hanna", "Tim", "Laura", "Lara",
        "Nina", "Sara", "Pia", "Ole", "Marlon", "Simon", "Philipp", "Alexander", "Tobias", "Kevin", "David", "Florian",
        "Nico", "Robin", "Samuel", "Valentin", "Dominik", "Jannik", "Maya", "Ella", "Jule", "Greta", "Carla", "Sophie",
        "Fabian", "Hannes", "Mats", "Lia", "Amelie", "Lilly", "Mila", "Isabel", "Olivia", "Leonard", "Matthias", 
        "Sebastian", "Jan", "Jakob", "Julius", "Christian", "Patrick", "Daniel", "Oliver", "Dennis", "Stefan", "Nils", 
        "Lars", "Mike", "Nick", "Viktor", "Alina", "Caroline", "Charlotte", "Johanna", "Tina", "Elena", "Selina", 
        "Vanessa", "Lisa", "Monika", "Heidi", "Petra", "Melanie", "Sonja", "Lena", "Franziska", "Anja", "Katja", "Eva"
    ]
    
    last_names = [
        "Schmidt", "Mueller", "Weber", "Fischer", "Schneider", "Lehmann", "Koch", "Bauer", "Wagner", "Becker",
        "Hoffmann", "Schulz", "Krause", "Richter", "Wolf", "Neumann", "Zimmermann", "Hartmann", "Klein", "Schwarz",
        "Kruger", "Peters", "Lang", "Dietrich", "Huber", "Schroeder", "Engel", "Bergmann", "Otto", "Lorenz", 
        "Schmitt", "Bock", "Stein", "Albrecht", "Jung", "Schuster", "Vogel", "Friedrich", "Kuhn", "Weiss", "Brandt", 
        "Haas", "Schlegel", "Busch", "Mayer", "Seidel", "Lindner", "Kraus", "Kirchner", "Behrens", "Metzger", "Mohr", 
        "Seifert", "Reich", "Braun", "Eckert", "Wendt", "Wirth", "Fink", "Bauer", "Horn", "Hermann", "Thiele", 
        "Ernst", "Franke", "Linke", "Voigt", "Mayer", "Hahn", "Fischer", "Barth", "Roth", "Hein", "Kolb", "Schuster", 
        "Frank", "Weber", "Pohl", "Schilling", "Arnold", "Scherer", "Ulrich", "Schwab", "Winkler", "Haase", "Sauer", 
        "Keller", "Konig", "Schubert", "Winter", "Graf", "Ritter", "Schumann", "Lorenz", "Wolff", "Seifert", "Berger", 
        "Paul", "Kuhn", "Kraus", "Ziegler"
    ]
    
    # Kombiniere Vor- und Nachnamen
    name = random.choice(first_names).lower() + random.choice(last_names).lower()
    
    # Füge Zahlen hinzu
    number = ''.join(random.choices(string.digits, k=random.randint(2, 4)))
    
    # Füge zufällig einige zusätzliche Buchstaben am Ende hinzu
    extra_letters = ''.join(random.choices(string.ascii_letters, k=random.randint(2, 4)))
    
    # Mische Groß- und Kleinbuchstaben in Name, Zahl und Zusatzbuchstaben
    username = ''.join(random.choice([char.upper(), char.lower()]) for char in name + number + extra_letters)
    
    # Stelle sicher, dass die Länge zwischen 12 und 16 Zeichen liegt
    return username[:random.randint(12, 16)]



def generate_random_email():
    local_part = get_random_name()
    domain = random.choice(DOMAIN_CONFIG["domains"])
    email_address = f"{local_part}@{domain}"
    print(f"Generated random email: {email_address}")
    return email_address

def generate_random_password():
    uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lowercase = 'abcdefghijklmnopqrstuvwxyz'
    numbers = '0123456789'
    special_chars = '#!'
    password = random.choice(uppercase) + random.choice(lowercase) + random.choice(numbers) + random.choice(special_chars)
    all_chars = uppercase + lowercase + numbers + special_chars
    remaining_length = random.randint(6, 10)
    for _ in range(remaining_length):
        password += random.choice(all_chars)
    password = ''.join(random.sample(password, len(password)))
    print(f"Generated random password: {password}")
    return password
def handle_username_error(driver, username_input, password_input, random_username, random_password, attempts=3):
    error_message = "Username is already used by someone else."
    
    for attempt in range(attempts):
        print(f"Versuch {attempt + 1}: Prüfen, ob der Benutzername {random_username} verfügbar ist.")
        
        try:
            # Überprüfen, ob die Fehlermeldung angezeigt wird
            error_element = driver.find_element(By.CSS_SELECTOR, "p#error-text[data-testid='Username-text-input-error']")
            if error_message in error_element.text:
                print(f"Benutzername {random_username} ist bereits vergeben. Neuer Benutzername wird generiert.")
                
                # Neuer Benutzername
                random_username = get_random_name()

                # Löschen und Eingeben des neuen Benutzernamens
                username_input.clear()
                human_like_mouse_move(driver, username_input)
                username_input.send_keys(random_username)
                time.sleep(2)

                # Passwort erneut eingeben
                password_input.clear()
                human_like_mouse_move(driver, password_input)
                password_input.send_keys(random_password)
                time.sleep(2)
            else:
                print(f"Benutzername {random_username} ist verfügbar.")
                return random_username  # Username ist erfolgreich
        except:
            print(f"Kein Fehler für den Benutzernamen {random_username} erkannt.")
            return random_username  # Username ist erfolgreich
        
    print(f"Nach {attempts} Versuchen konnte kein verfügbarer Benutzername gefunden werden. Abbruch.")
    return None  # Kein gültiger Username nach mehreren Versuchen


# Proxy Statistiken initialisieren oder laden
def load_proxy_stats():
    stats = {}
    if os.path.exists(PROXY_STATS_FILE):
        with open(PROXY_STATS_FILE, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Überspringe den Header
            for row in reader:
                stats[row[0]] = {'bans': int(row[1]), 'successes': int(row[2])}
    return stats

def update_proxy_stats(proxy, success=False):
    stats = load_proxy_stats()
    
    if proxy not in stats:
        stats[proxy] = {'bans': 0, 'successes': 0}
    
    if success:
        stats[proxy]['successes'] += 1
    else:
        stats[proxy]['bans'] += 1
    
    with open(PROXY_STATS_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Proxy', 'Bans', 'Successes'])
        for proxy, stat in stats.items():
            writer.writerow([proxy, stat['bans'], stat['successes']])

def load_blocked_proxies():
    blocked_proxies = {}
    if os.path.exists(BLOCKED_PROXIES_FILE):
        with open(BLOCKED_PROXIES_FILE, 'r') as file:
            for line in file:
                proxy, timestamp = line.strip().split(',')
                blocked_time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                if datetime.now() < blocked_time:
                    blocked_proxies[proxy] = blocked_time
    return blocked_proxies

def save_blocked_proxies(blocked_proxies):
    with open(BLOCKED_PROXIES_FILE, 'w') as file:
        for proxy, timestamp in blocked_proxies.items():
            file.write(f"{proxy},{timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n")

def block_proxy(proxy, blocked_proxies, block_duration_minutes, success=False):
    if success:
        print(f"Proxy {proxy} erfolgreich. Sperren für {block_duration_minutes} Minuten.")
    else:
        print(f"Proxy {proxy} gescheitert. Sperren für {block_duration_minutes} Minuten.")
    
    blocked_proxies[proxy] = datetime.now() + timedelta(minutes=block_duration_minutes)
    save_blocked_proxies(blocked_proxies)
    update_proxy_stats(proxy, success=success)

def get_proxy():
    proxies = []
    blocked_proxies = load_blocked_proxies()
    
    if os.path.exists(PROXY_FILE):
        with open(PROXY_FILE, 'r') as file:
            proxies = [line.strip() for line in file.readlines()]

        # Mische die Proxy-Liste nach jedem Lauf
        random.shuffle(proxies)

        for proxy in proxies:
            if proxy not in blocked_proxies or datetime.now() > blocked_proxies[proxy]:
                print(f"Verwende Proxy: {proxy}")
                with open(LAST_PROXY_FILE, 'w') as last_file:
                    last_file.write(proxy)
                return proxy, blocked_proxies

    print("Keine verfügbaren Proxys gefunden.")
    return None, blocked_proxies

def setup_selenium(headless=False):
    chrome_options = uc.ChromeOptions()

    # Standardoptionen
    chrome_options.add_argument("--lang=en-US")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-webrtc")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-features=OptimizationHints")
    prefs = {
        "profile.managed_default_content_settings.images": 2,  # Bilder blockieren
        "profile.default_content_setting_values.notifications": 2,  # Benachrichtigungen blockieren
    }
    chrome_options.add_experimental_option("prefs", prefs)

    proxy, blocked_proxies = get_proxy()
    if proxy:
        chrome_options.add_argument(f'--proxy-server={proxy}')

    if headless:
        chrome_options.add_argument("--headless")

    driver = uc.Chrome(options=chrome_options)
    bypass_selenium_detection(driver)
    return driver, proxy, blocked_proxies

def bypass_selenium_detection(driver):
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_script("window.navigator.chrome = { runtime: {} };")
    driver.execute_script("""
    Object.defineProperty(navigator, 'languages', {
      get: function() {
        return ['en-US', 'en'];
      }
    });
    """)
    driver.execute_script("""
    Object.defineProperty(navigator, 'plugins', {
      get: function() {
        return [1, 2, 3];
      }
    });
    """)

def human_like_mouse_move(driver, element):
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    time.sleep(random.uniform(1.5, 5))

def get_confirmation_email(generated_email, retry_attempts=3, retry_delay=30):
    imap = None
    try:
        email_user = EMAIL_CONFIG["user"]
        email_password = EMAIL_CONFIG["password"]
        imap_host = EMAIL_CONFIG["imap_host"]
        target_sender = EMAIL_CONFIG["target_sender"]

        for attempt in range(retry_attempts):
            print(f"Attempt {attempt + 1} to get confirmation email for {generated_email}...")

            imap = imaplib.IMAP4_SSL(imap_host)
            imap.login(email_user, email_password)

            folder_mappings = {
                "inbox": "INBOX",
                "spam": "[Gmail]/Spam",
                "all_mail": "[Gmail]/All Mail"
            }

            for folder_name, folder_path in folder_mappings.items():
                print(f"Searching in folder: {folder_name}")
                status, _ = imap.select(f'"{folder_path}"')

                if status != "OK":
                    print(f"Could not select folder: {folder_name}. Status: {status}")
                    continue

                status, messages = imap.search(None, f'(FROM "{target_sender}" TO "{generated_email}")')
                if status != "OK":
                    print(f"No emails found in {folder_name}. Status: {status}")
                    continue

                messages = messages[0].split()
                if not messages:
                    print(f"No messages found from {target_sender} in {folder_name}.")
                    continue

                print(f"Found {len(messages)} emails from {target_sender} in folder {folder_name}.")

                for email_id in messages:
                    status, msg_data = imap.fetch(email_id, '(RFC822)')
                    if status != "OK":
                        print(f"Error fetching email with ID: {email_id}. Status: {status}")
                        continue

                    for response_part in msg_data:
                        if isinstance(response_part, tuple):
                            full_msg = email.message_from_bytes(response_part[1])

                            if full_msg.is_multipart():
                                for part in full_msg.walk():
                                    if part.get_content_type() == "text/html":
                                        body = part.get_payload(decode=True).decode('utf-8')
                                    elif part.get_content_type() == "text/plain":
                                        body = part.get_payload(decode=True).decode('utf-8')
                            else:
                                body = full_msg.get_payload(decode=True).decode('utf-8')

                            regex = r'<br><br><center><h2>(\d{6})<\/h2><\/center>'
                            match = re.search(regex, body)
                            if match:
                                confirmation_code = match.group(1)
                                print(f"Confirmation Code Found: {confirmation_code}")
                                return confirmation_code
                            else:
                                print("No confirmation code found in this email.")

            print(f"No confirmation email found for {generated_email}. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)

        print("No confirmation email found after retries.")
        return None

    except Exception as e:
        print(f"Error while fetching email: {e}")
        traceback.print_exc()
        return None

    finally:
        if imap:
            imap.logout()

def run_steps(driver, proxy, blocked_proxies):
    try:
        year, month, day = generate_random_birthdate()
        random_email = generate_random_email()
        random_password = generate_random_password()
        random_username = get_random_name()

        print("Navigating to https://join.pokemon.com/")
        driver.get("https://join.pokemon.com/")
        WebDriverWait(driver, 30).until(EC.url_contains("pokemon"))
        time.sleep(2)

        if "Access denied" in driver.page_source or "Error 16" in driver.page_source:
            print("Website not loading. Blocking proxy for 24 hours.")
            block_proxy(proxy, blocked_proxies, block_duration_minutes=1440)  # 24 hours
            driver.quit()
            driver, proxy, blocked_proxies = setup_selenium()
            run_steps(driver, proxy, blocked_proxies)
            return

        print("Clearing cookies.")
        driver.delete_all_cookies()
        time.sleep(2)

        print("Refreshing the page.")
        driver.refresh()
        time.sleep(5)

        print("Waiting for 5 seconds.")
        time.sleep(5)

        print("Selecting country: Germany.")
        country_select = driver.find_element(By.CSS_SELECTOR, "select#country-select")
        human_like_mouse_move(driver, country_select)
        country_select.send_keys("Germany")
        time.sleep(1)

        print(f"Selecting birth year: {year}.")
        year_select = driver.find_element(By.CSS_SELECTOR, "select#year-select")
        human_like_mouse_move(driver, year_select)
        year_select.send_keys(str(year))
        time.sleep(1)

        print(f"Selecting birth month: {month}.")
        month_select = driver.find_element(By.CSS_SELECTOR, "select#month-select")
        human_like_mouse_move(driver, month_select)
        month_select.send_keys(month)
        time.sleep(1)

        print(f"Selecting birth day: {day}.")
        day_select = driver.find_element(By.CSS_SELECTOR, "select#day-select")
        human_like_mouse_move(driver, day_select)
        day_select.send_keys(str(day))
        time.sleep(1)

        print("Clicking continue button.")
        submit_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button#ageGateSubmit")))
        human_like_mouse_move(driver, submit_button)
        submit_button.click()
        time.sleep(2)

        print("Clicking the I AM Sure button.")
        button_6 = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.basic-button:nth-child(6)")))
        human_like_mouse_move(driver, button_6)
        button_6.click()
        time.sleep(3)

        print(f"Entering email: {random_email}")
        email_input = driver.find_element(By.CSS_SELECTOR, "input#email-text-input")
        human_like_mouse_move(driver, email_input)
        email_input.send_keys(random_email)
        time.sleep(2)

        print(f"Confirming email: {random_email}")
        confirm_input = driver.find_element(By.CSS_SELECTOR, "input#confirm-text-input")
        human_like_mouse_move(driver, confirm_input)
        confirm_input.send_keys(random_email)
        time.sleep(2)

        print("Clicking marketing checkbox.")
        marketing_checkbox = driver.find_element(By.CSS_SELECTOR, "input#marketing")
        human_like_mouse_move(driver, marketing_checkbox)
        marketing_checkbox.click()
        time.sleep(2)

        print("Clicking basic button to continue.")
        basic_button = driver.find_element(By.CSS_SELECTOR, "button.basic-button")
        human_like_mouse_move(driver, basic_button)
        basic_button.click()
        time.sleep(15)

        if "Oops! There Was an Error" in driver.page_source:
            print("Bot detection encountered. Blocking proxy for 12 hours.")
            block_proxy(proxy, blocked_proxies, block_duration_minutes=720)  # 12 hours
            driver.quit()
            driver, proxy, blocked_proxies = setup_selenium()
            run_steps(driver, proxy, blocked_proxies)
            return

        print("Clicking MuiButton-contained button.")
        mui_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.MuiButton-contained")))
        human_like_mouse_move(driver, mui_button)
        mui_button.click()
        time.sleep(3)
        mui_button.click()
        time.sleep(10)
        
        if "Oops! There Was an Error" in driver.page_source:
            print("Bot detection encountered. Blocking proxy for 12 hours.")
            block_proxy(proxy, blocked_proxies, block_duration_minutes=720)  # 12 hours
            driver.quit()
            driver, proxy, blocked_proxies = setup_selenium()
            run_steps(driver, proxy, blocked_proxies)
            return

        print(f"Clicking to skip screenname setup with username: {random_username}.")
        screenname_skip = driver.find_element(By.CSS_SELECTOR, "button#screennameSkip")
        human_like_mouse_move(driver, screenname_skip)
        screenname_skip.click()
        time.sleep(3)

        # Verwende die Funktion in der Hauptlogik nach der Passworteingabe
        print(f"Benutzername eingeben: {random_username}")
        username_input = driver.find_element(By.CSS_SELECTOR, "input#Username-text-input")
        human_like_mouse_move(driver, username_input)
        username_input.send_keys(random_username)
        time.sleep(2)

        print(f"Passwort eingeben: {random_password}")
        password_input = driver.find_element(By.CSS_SELECTOR, "input#password-text-input-test")
        human_like_mouse_move(driver, password_input)
        password_input.send_keys(random_password)
        time.sleep(2)

        # Überprüfen, ob ein Username-Fehler vorliegt, und bis zu 3 Versuche unternehmen
        random_username = handle_username_error(driver, username_input, password_input, random_username, random_password)

        if not random_username:
            print("Prozess wird nach mehreren fehlgeschlagenen Versuchen abgebrochen.")
            driver.quit()
            return

        print("Clicking on Create Account.")
        create_account_button = driver.find_element(By.XPATH, "//*[text()='Create Account']")
        human_like_mouse_move(driver, create_account_button)
        time.sleep(1)
        create_account_button.click()
        time.sleep(1)

        print("Clicking 'I Am Sure' button.")
        i_am_sure_button = driver.find_element(By.XPATH, "//*[text()='I Am Sure']")
        human_like_mouse_move(driver, i_am_sure_button)
        time.sleep(1)
        i_am_sure_button.click()
        time.sleep(12)

        if "Oops! It looks like something went wrong." in driver.page_source:
            print("Bot detection encountered. Blocking proxy for 12 hours.")
            block_proxy(proxy, blocked_proxies, block_duration_minutes=720)  # 12 hours
            driver.quit()
            driver, proxy, blocked_proxies = setup_selenium()
            run_steps(driver, proxy, blocked_proxies)
            return
            
        if "Oops! There Was an Error" in driver.page_source:
            print("Bot detection encountered. Blocking proxy for 12 hours.")
            block_proxy(proxy, blocked_proxies, block_duration_minutes=720)  # 12 hours
            driver.quit()
            driver, proxy, blocked_proxies = setup_selenium()
            run_steps(driver, proxy, blocked_proxies)
            return

        print("Getting confirmation email.")
        pin = get_confirmation_email(generated_email=random_email, retry_attempts=3, retry_delay=30)
        if pin:
            print(f"Entering PIN: {pin}.")
            pin_input = driver.find_element(By.CSS_SELECTOR, "input#code-text-input")
            human_like_mouse_move(driver, pin_input)
            pin_input.send_keys(pin)
        else:
            print("PIN not found. Exiting.")
            driver.quit()
            return

        time.sleep(20)
        
        print("Clicking on Continue.")
        continue_button = driver.find_element(By.XPATH, "//*[text()='Continue']")
        human_like_mouse_move(driver, continue_button)
        time.sleep(1)
        continue_button.click()

        print("Waiting for account activation confirmation.")
        WebDriverWait(driver, 30).until(EC.text_to_be_present_in_element((By.XPATH, "//*[text()='Thank you for activating your account!']"), "Thank you for activating your account!"))

        save_account_to_csv(random_email, random_username, random_password, pin)

        print("Account successfully created. Blocking the current proxy for 10 minutes and starting the process for a new account...")

        block_proxy(proxy, blocked_proxies, block_duration_minutes=10, success=True)

        driver.quit()
        driver, proxy, blocked_proxies = setup_selenium()
        run_steps(driver, proxy, blocked_proxies)

    except Exception as e:
        print(f"Error occurred: {e}")
        traceback.print_exc()
        block_proxy(proxy, blocked_proxies, block_duration_minutes=720)  # 12 hours in case of general errors
        driver.quit()
        driver, proxy, blocked_proxies = setup_selenium()
        run_steps(driver, proxy, blocked_proxies)

if __name__ == "__main__":
    while True:  # To automatically restart the process on crash
        try:
            headless = False
            driver, proxy, blocked_proxies = setup_selenium(headless=headless)
            run_steps(driver, proxy, blocked_proxies)
            driver.quit()
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            traceback.print_exc()
            # In case of an error, sleep for a while before restarting
            time.sleep(30)
