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
from selenium.common.exceptions import NoSuchElementException
import traceback
from datetime import datetime, timedelta
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from webdriver_manager.chrome import ChromeDriverManager
import threading
import queue
from concurrent.futures import ThreadPoolExecutor
import queue
from datetime import datetime, timedelta
import os
import signal
import psutil


# List of required packages
required_packages = [
    'random', 'time', 'undetected_chromedriver', 'selenium', 'os', 
    're', 'imaplib', 'email', 'csv', 'datetime', 'traceback', 'requests',
    'webdriver_manager'
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
    "password": "xxx xxx xx xx",
    "imap_host": "imap.gmail.com",
    "target_sender": "no-reply@tmi.pokemon.com"
}

DOMAIN_CONFIG = {
    "domains": ["xxx.eu", "xx.de", "xx.de", "xx.de", "xx.de", "xxx.de", "xx.de"]
}

PROXY_STATS_FILE = 'proxy_stats.csv'
PROXY_FILE = 'proxies.txt'
BLOCKED_PROXIES_FILE = 'blocked_proxies.txt'
LAST_PROXY_FILE = 'last_proxy.txt'


# Global queues for proxy management
proxy_queue_1 = queue.PriorityQueue()
proxy_queue_2 = queue.PriorityQueue()

def load_proxy_stats():
    stats = {}
    if os.path.exists(PROXY_STATS_FILE):
        with open(PROXY_STATS_FILE, mode='r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                stats[row[0]] = {
                    'bans': int(row[1]), 
                    'successes': int(row[2]), 
                    'last_used': datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S') if row[3] else None
                }
    return stats

def initialize_proxy_queues():
    proxies = []
    if os.path.exists(PROXY_FILE):
        with open(PROXY_FILE, 'r') as file:
            proxies = [line.strip() for line in file.readlines()]
    
    stats = load_proxy_stats()
    
    # Sortiere Proxies basierend auf Erfolgsrate (Erfolge, und wann sie zuletzt genutzt wurden)
    sorted_proxies = sorted(proxies, key=lambda p: (-stats.get(p, {}).get('successes', 0), stats.get(p, {}).get('last_used', datetime.min)))
    
    # Verteile die sortierten Proxies gleichmäßig auf beide Queues
    for i, proxy in enumerate(sorted_proxies):
        priority = (-stats.get(proxy, {}).get('successes', 0), stats.get(proxy, {}).get('last_used', datetime.min))
        if i % 2 == 0:
            proxy_queue_1.put((priority, proxy))
        else:
            proxy_queue_2.put((priority, proxy))


def get_proxy_for_thread(thread_id):
    if thread_id == 1:
        return proxy_queue_1.get()[1]
    else:
        return proxy_queue_2.get()[1]

def return_proxy_to_queue(proxy, thread_id, success=False):
    stats = load_proxy_stats()
    if proxy not in stats:
        stats[proxy] = {'bans': 0, 'successes': 0, 'last_used': None}
    
    if success:
        stats[proxy]['successes'] += 1
    stats[proxy]['last_used'] = datetime.now()
    
    priority = (-stats[proxy]['successes'], stats[proxy]['last_used'])
    
    if thread_id == 1:
        proxy_queue_1.put((priority, proxy))
    else:
        proxy_queue_2.put((priority, proxy))
        
def save_account_to_csv(email, username, password, pin):
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    csv_file = 'accounts.csv'
    
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            # Schreibe die Kopfzeile nur, wenn die Datei leer ist
            writer.writerow(['Email', 'Username', 'Password', 'PIN', 'Date', 'Time'])
        # Schreibe die Daten ohne Proxy in die CSV
        writer.writerow([email, username, password, pin, date_time.split()[0], date_time.split()[1]])
    
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
     
    name_format = random.choice([
        "{first}{last}", 
        "{first}{last}{number}"
    ])
    
    first = random.choice(first_names).lower()
    last = random.choice(last_names).lower()
    number = ''.join(random.choices(string.digits, k=random.randint(2, 4)))

    name = name_format.format(first=first, last=last, number=number)
    
    extra_letters = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(2, 4)))
    
    username = ''.join(random.choice([char.upper(), char.lower()]) for char in name + extra_letters)
    return username[:random.randint(12, 17)]

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

def handle_username_error(driver, username_input, password_input, random_username, random_password, max_retries=5):
    for attempt in range(max_retries):
        try:
            error_element = driver.find_element(By.CSS_SELECTOR, "p#error-text[data-testid='Username-text-input-error']")
            if error_element.is_displayed():
                print(f"Fehler bei der Benutzernameneingabe: {error_element.text}. Versuch {attempt + 1} von {max_retries}.")
                
                random_username = get_random_name()
                
                username_input.clear()
                human_like_mouse_move(driver, username_input)
                username_input.send_keys(random_username)
                time.sleep(2)
                
                password_input.clear()
                human_like_mouse_move(driver, password_input)
                password_input.send_keys(random_password)
                time.sleep(2)
                
            else:
                break
            
        except NoSuchElementException:
            print("Kein Fehler gefunden, weiter mit dem Prozess.")
            break
    
    if attempt == max_retries - 1 and error_element.is_displayed():
        print("Maximale Anzahl an Versuchen erreicht. Abbruch.")
        return None
    
    return random_username
    
def load_proxy_stats():
    stats = {}
    if os.path.exists(PROXY_STATS_FILE):
        with open(PROXY_STATS_FILE, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if len(row) < 4:
                    print(f"Skipping invalid row in proxy stats: {row}")
                    continue
                try:
                    stats[row[0]] = {
                        'bans': int(row[1]),
                        'successes': int(row[2]),
                        'last_used': datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S') if row[3] else None
                    }
                except Exception as e:
                    print(f"Error processing row {row}: {e}")
    return stats

    
def update_proxy_stats(proxy, success=False):
    stats = load_proxy_stats()

    if proxy not in stats:
        stats[proxy] = {'bans': 0, 'successes': 0, 'last_used': None}

    if success:
        stats[proxy]['successes'] += 1
        stats[proxy]['last_used'] = datetime.now()
    else:
        stats[proxy]['bans'] += 1
        stats[proxy]['last_used'] = datetime.now()

    with open(PROXY_STATS_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Proxy', 'Bans', 'Successes', 'Last_Used'])
        for proxy, stat in stats.items():
            last_used_str = stat['last_used'].strftime('%Y-%m-%d %H:%M:%S') if stat['last_used'] else ''
            writer.writerow([proxy, stat['bans'], stat['successes'], last_used_str])

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


def setup_selenium_for_thread(thread_id, headless=False):
    chrome_options = uc.ChromeOptions()

    # Standard-Optionen setzen
    chrome_options.add_argument("--lang=en-US")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-webrtc")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-features=OptimizationHints")
    chrome_options.add_argument("--window-size=412,850")
    chrome_options.add_argument("--disable-search-engine-choice-screen")

    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.default_content_setting_values.notifications": 2,
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # Hole den Proxy für den jeweiligen Thread
    proxy = get_proxy_for_thread(thread_id)
    if proxy:
        chrome_options.add_argument(f'--proxy-server={proxy}')

    if headless:
        chrome_options.add_argument("--headless")


    driver = uc.Chrome(driver_executable_path=ChromeDriverManager().install(), options=chrome_options)
    driver.set_window_position(0, 0)
    driver.set_window_size(412, 850)

    bypass_selenium_detection(driver)
    
    # Store both the driver and the PID
    browser_pid = driver.service.process.pid
    print(f"Thread {thread_id}: Browser started with PID {browser_pid}")

    return driver, proxy, browser_pid

def kill_browser_process(pid):
    try:
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        for child in children:
            child.terminate()
        parent.terminate()
        gone, alive = psutil.wait_procs([parent] + children, timeout=3)
        for p in alive:
            p.kill()
        print(f"Browser process with PID {pid} and its children have been terminated.")
    except psutil.NoSuchProcess:
        print(f"Process with PID {pid} not found.")
    except Exception as e:
        print(f"Error killing process {pid}: {e}")


def block_proxy(proxy, thread_id, block_duration_minutes, success=False, driver=None):
    stats = load_proxy_stats()

    if proxy not in stats:
        stats[proxy] = {'bans': 0, 'successes': 0, 'last_used': None}

    if success:
        print(f"Thread {thread_id}: Proxy {proxy} erfolgreich. Sperren für {block_duration_minutes} Minuten.")
        stats[proxy]['successes'] += 1
    else:
        block_duration_minutes = 15 * (stats[proxy]['bans'] + 1)
        print(f"Thread {thread_id}: Proxy {proxy} gescheitert. Sperren für {block_duration_minutes} Minuten.")
        stats[proxy]['bans'] += 1

    blocked_until = datetime.now() + timedelta(minutes=block_duration_minutes)
    print(f"Thread {thread_id}: Proxy {proxy} gesperrt bis {blocked_until}")

    stats[proxy]['last_used'] = blocked_until
    update_proxy_stats(proxy, success=success)

    # Close the current browser, if a driver exists
    if driver:
        try:
            driver.quit()
            print(f"Thread {thread_id}: Browser für Proxy {proxy} geschlossen.")
        except Exception as e:
            print(f"Thread {thread_id}: Fehler beim Schließen des Browsers: {e}")

    # Return the proxy to the queue
    return_proxy_to_queue(proxy, thread_id, success)

    # Get the next proxy and start a new browser
    print(f"Thread {thread_id}: Wähle den nächsten Proxy und starte einen neuen Browser...")
    
    # Unpack all three values from setup_selenium_for_thread
    new_driver, new_proxy, browser_pid = setup_selenium_for_thread(thread_id)
    
    # Start the process again with the new proxy and driver
    run_steps(new_driver, new_proxy, thread_id, browser_pid)
   
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
    time.sleep(random.uniform(0.5, 1.5))

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

def print_success_message(message):
    print(f"\033[92m{message}\033[0m")

def fill_form_via_javascript(driver, year, month, day):
    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "select#country-select"))
        )

        script = f"""
        var countrySelect = document.querySelector('select#country-select');
        var yearSelect = document.querySelector('select#year-select');
        var monthSelect = document.querySelector('select#month-select');
        var daySelect = document.querySelector('select#day-select');
        
        countrySelect.value = 'Germany';
        yearSelect.value = '{year}';
        monthSelect.value = '{month}';
        daySelect.value = '{day}';

        var event = new Event('change', {{ bubbles: true }});
        countrySelect.dispatchEvent(event);
        yearSelect.dispatchEvent(event);
        monthSelect.dispatchEvent(event);
        daySelect.dispatchEvent(event);
        """
        driver.execute_script(script)
        print(f"Formularwerte gesetzt und change-Events ausgelöst: Land=Germany, Jahr={year}, Monat={month}, Tag={day}")

        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button#ageGateSubmit"))
        )
        human_like_mouse_move(driver, continue_button)
        continue_button.click()
    except Exception as e:
        print(f"Fehler beim Setzen der Formularwerte: {e}")
        traceback.print_exc()

def send_data_to_api(username, password):
    url = "http://ccc.cc.cc.cc:5006/webhook"
    data = {
        "username": username,
        "password": password
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print(f"Data sent successfully: {data}")
        else:
            print(f"Failed to send data. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending data to API: {e}")
def check_for_errors_and_restart(driver, proxy, thread_id):
    """
    Diese Funktion überprüft, ob Fehler wie 'Oops! There Was an Error' oder der 'Contact Customer Support'-Button
    angezeigt werden. Falls ja, wird der Proxy für 12 Stunden blockiert, der Browser geschlossen und ein neuer
    Browser gestartet.
    """
    try:
        # Warte, bis das <h1> Element mit dem Text 'Oops! There Was an Error' erscheint (bis zu 10 Sekunden)
        try:
            error_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h1[text()='Oops! There Was an Error']"))
            )
            print("Error message detected: 'Oops! There Was an Error'")
        except:
            error_element = None

        # Warte, bis der 'Contact Customer Support' Button verfügbar ist
        try:
            contact_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#root > div > div.App > div > div > span:nth-child(2) > a.basic-button.link-button.primary"))
            )
            print("Contact Customer Support button detected.")
        except:
            contact_button = None

        # Wenn eines der Elemente gefunden wurde
        if error_element or contact_button:
            print("Error or support button encountered. Blocking proxy for 12 hours.")
            
            # Proxy für 12 Stunden blockieren
            block_proxy(proxy, thread_id, block_duration_minutes=720)  # 12 Stunden
            
            # Browser ordnungsgemäß schließen
            driver.quit()

            # Starte einen neuen Browser mit neuem Proxy
            driver, new_proxy, browser_pid = setup_selenium_for_thread(thread_id)
            run_steps(driver, new_proxy, thread_id, browser_pid)

            return True  # Signalisiert, dass ein Fehler gefunden wurde und der Prozess neu gestartet wurde

        # Falls kein Fehler gefunden wurde, warte kurz (optional)
        time.sleep(15)
        return False  # Kein Fehler gefunden, weiter im Prozess

    except Exception as e:
        print(f"An error occurred in check_for_errors_and_restart: {e}")
        traceback.print_exc()
        return False  # Im Fehlerfall auch kein Neustart, weiter im Prozess

def run_steps(driver, proxy, thread_id, browser_pid):
    try:
        year, month, day = generate_random_birthdate()
        random_email = generate_random_email()
        random_password = generate_random_password()
        random_username = get_random_name()

        print(f"Thread {thread_id}: Navigating to https://join.pokemon.com/")
        driver.get("https://join.pokemon.com/")

        WebDriverWait(driver, 30).until(EC.url_contains("pokemon"))
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        try:
            error_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h1[text()='Error 16']"))
            )
            print(f"Thread {thread_id}: Error message detected: 'Error 16'")
        except:
            error_element = None

        try:
            blocked_message = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'This request was blocked by our security service')]"))
            )
            print(f"Thread {thread_id}: Security block message detected.")
        except:
            blocked_message = None

        if error_element or blocked_message:
            print(f"Thread {thread_id}: Error 16 or security block detected. Blocking proxy for 12 hours.")
            block_proxy(proxy, thread_id, block_duration_minutes=720)
            return  # Frühzeitiger Abbruch ohne weiteren Prozess

        fill_form_via_javascript(driver, year, month, day)

        print(f"Thread {thread_id}: Clicking the I AM Sure button.")
        button_6 = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.basic-button:nth-child(6)")))
        human_like_mouse_move(driver, button_6)
        button_6.click()
        time.sleep(1)

        if check_for_errors_and_restart(driver, proxy, thread_id):
            return  # Frühzeitiger Abbruch, da der Browser neu gestartet wurde

        print(f"Thread {thread_id}: Entering email: {random_email}")
        email_input = driver.find_element(By.CSS_SELECTOR, "input#email-text-input")
        human_like_mouse_move(driver, email_input)
        email_input.send_keys(random_email)

        print(f"Thread {thread_id}: Confirming email: {random_email}")
        confirm_input = driver.find_element(By.CSS_SELECTOR, "input#confirm-text-input")
        human_like_mouse_move(driver, confirm_input)
        confirm_input.send_keys(random_email)

        print(f"Thread {thread_id}: Clicking marketing checkbox.")
        marketing_checkbox = driver.find_element(By.CSS_SELECTOR, "input#marketing")
        human_like_mouse_move(driver, marketing_checkbox)
        marketing_checkbox.click()

        print(f"Thread {thread_id}: Clicking basic button to continue.")
        basic_button = driver.find_element(By.CSS_SELECTOR, "button.basic-button")
        human_like_mouse_move(driver, basic_button)
        basic_button.click()
        time.sleep(3)

        if check_for_errors_and_restart(driver, proxy, thread_id):
            return  # Frühzeitiger Abbruch, da der Browser neu gestartet wurde


        print(f"Thread {thread_id}: Clicking MuiButton-contained button.")
        mui_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.MuiButton-contained")))
        human_like_mouse_move(driver, mui_button)
        mui_button.click()
        time.sleep(1)
        mui_button.click()
        time.sleep(1)
        
        if check_for_errors_and_restart(driver, proxy, thread_id):
            return  # Frühzeitiger Abbruch, da der Browser neu gestartet wurde


        print(f"Thread {thread_id}: Clicking to skip screenname setup with username: {random_username}.")
        screenname_skip = driver.find_element(By.CSS_SELECTOR, "button#screennameSkip")
        human_like_mouse_move(driver, screenname_skip)
        screenname_skip.click()

        print(f"Thread {thread_id}: Entering username: {random_username}")
        username_input = driver.find_element(By.CSS_SELECTOR, "input#Username-text-input")
        human_like_mouse_move(driver, username_input)
        username_input.send_keys(random_username)

        print(f"Thread {thread_id}: Entering password: {random_password}")
        password_input = driver.find_element(By.CSS_SELECTOR, "input#password-text-input-test")
        human_like_mouse_move(driver, password_input)
        password_input.send_keys(random_password)


        print(f"Thread {thread_id}: Clicking on Create Account.")
        create_account_button = driver.find_element(By.XPATH, "//*[text()='Create Account']")
        human_like_mouse_move(driver, create_account_button)
        time.sleep(1)
        create_account_button.click()
        time.sleep(1)

        print(f"Thread {thread_id}: Clicking 'I Am Sure' button.")
        i_am_sure_button = driver.find_element(By.XPATH, "//*[text()='I Am Sure']")
        human_like_mouse_move(driver, i_am_sure_button)
        time.sleep(1)
        i_am_sure_button.click()
        time.sleep(5)
        
        # **NEU: Überprüfen auf "Username is already in use"**
        random_username = handle_username_error(driver, username_input, password_input, random_username, random_password)

        if not random_username:
            print(f"Thread {thread_id}: Process aborted after multiple failed attempts.")
            return

        if check_for_errors_and_restart(driver, proxy, thread_id):
            return  # Frühzeitiger Abbruch, da der Browser neu gestartet wurde


        time.sleep(15)
        
        if check_for_errors_and_restart(driver, proxy, thread_id):
            return  # Frühzeitiger Abbruch, da der Browser neu gestartet wurde

        print(f"Thread {thread_id}: Getting confirmation email.")
        pin = get_confirmation_email(generated_email=random_email, retry_attempts=3, retry_delay=30)
        if pin:
            print(f"Thread {thread_id}: Entering PIN: {pin}.")
            pin_input = driver.find_element(By.CSS_SELECTOR, "input#code-text-input")
            human_like_mouse_move(driver, pin_input)
            pin_input.send_keys(pin)
        else:
            print(f"Thread {thread_id}: PIN not found. Exiting.")
            return

        time.sleep(1)

        print(f"Thread {thread_id}: Clicking on Continue.")
        continue_button = driver.find_element(By.XPATH, "//*[text()='Continue']")
        human_like_mouse_move(driver, continue_button)
        time.sleep(1)
        continue_button.click()
        if check_for_errors_and_restart(driver, proxy, thread_id):
            return  # Frühzeitiger Abbruch, da der Browser neu gestartet wurde

        print(f"Thread {thread_id}: Waiting for account activation confirmation.")
        WebDriverWait(driver, 30).until(
            EC.text_to_be_present_in_element((By.XPATH, "//*[text()='Thank you for activating your account!']"), 
                                             "Thank you for activating your account!")
        )

          # Erfolgreicher Durchlauf, Konto erstellt
        save_account_to_csv(random_email, random_username, random_password, pin)
        send_data_to_api(random_username, random_password)

        print_success_message(f"Thread {thread_id}: Account successfully created. Blocking the current proxy for 31 minutes and starting the process for a new account...")
        
        # **Browser hier schließen, bevor Proxy blockiert wird**
        driver.quit()  # Sicherstellen, dass der Browser geschlossen wird
        
        # Blockiere Proxy und starte neuen Prozess
        block_proxy(proxy, thread_id, block_duration_minutes=31, success=True)
        
    except Exception as e:
        print(f"Thread {thread_id} encountered an error: {e}")
        traceback.print_exc()
    finally:
        try:
            driver.quit()
            print(f"Thread {thread_id}: Browser closed via driver.quit().")
        except Exception as e:
            print(f"Thread {thread_id}: Error closing browser via driver.quit(): {e}")
        finally:
            kill_browser_process(browser_pid)
            time.sleep(2)

def run_steps_for_thread(thread_id):
    while True:
        driver = None
        browser_pid = None
        try:
            driver, proxy, browser_pid = setup_selenium_for_thread(thread_id)
            run_steps(driver, proxy, thread_id, browser_pid)
        except Exception as e:
            print(f"Thread {thread_id} encountered an error: {e}")
            traceback.print_exc()
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
            if browser_pid:
                kill_browser_process(browser_pid)
            time.sleep(3)  # Wait before starting the next iteration

if __name__ == "__main__":
    initialize_proxy_queues()

    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(run_steps_for_thread, 1)
        executor.submit(run_steps_for_thread, 2)
