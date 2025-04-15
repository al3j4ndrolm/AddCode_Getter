from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time
import yagmail

# Setup Chrome
options = Options()
options.add_argument('--headless')  # hide browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

user_email =  input("[@] Gmail that is going to be used to send emails: ")
user_app_password = input("[!] Paste your Gmail App Password (Find it in your Account settings: )")
class_code = input("[!] Choose class (ex. Math, Cis... etc): ")
class_number = input("[#] Class number (1A, 22C... etc): ")
base_url = f"https://www.deanza.edu/schedule/listings.html?dept={class_code}&t=S2025"

driver.get(base_url)
wait = WebDriverWait(driver, 5)

def open_professor_page(driver, link_element):

	main_window = driver.current_window_handle

	driver.execute_script("window.open(arguments[0]);", link_element)
	time.sleep(0.5)
	driver.switch_to.window(driver.window_handles[-1])

	email = None
	try:
		mailto_link = WebDriverWait(driver, 5).until(
			EC.presence_of_element_located((By.XPATH, "//a[starts-with(@href, 'mailto:')]"))
		)
		email = mailto_link.text
		print(f"Email: {email}")
	except TimeoutException:
		print("Email not found")

	driver.close()
	driver.switch_to.window(main_window)
	return email

def send_email(user_email, user_app_password ,class_name, class_code, professor_name, professor_email):
	yag = yagmail.SMTP(user_email, user_app_password) 
	yag.send(
		to=professor_email,
		subject=f"Add code request - {class_name} ({class_code})",
		contents=f"""Good morning, Professor {professor_name},

I hope this message finds you well. My name is [PUT YOUR NAME HERE], and I’m writing to kindly request an add code for your {class_name} ({class_code}) class this quarter.

This course is very important for plan to transfer in the coming fall. I’ve reviewed the syllabus and am genuinely excited to learn from you. If there’s any possibility to receive an add code, I would be truly grateful.

Thank you so much for your time and consideration.

Warm regards,  
[NAME HERE]
SID: [SID HERE]"""
	)
	print(f"[!] Email sent to {professor_email}!\n")

try:
	element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
except TimeoutException:
	print("Could not find the class table")
	driver.quit()
	exit()

professors = element.find_elements(By.TAG_NAME, "tr")[1:]
appeared = []

for professor in professors:

	professor_data = professor.find_elements(By.TAG_NAME, "td")

	if len(professor_data) >= 8:
		name = professor_data[7].text
		
		if name and name not in appeared and class_number in professor_data[1].text:
			appeared.append(name)

			page_link = professor_data[7].find_element(By.TAG_NAME, "a").get_attribute("href")
			print(f"\n{name} - {professor_data[8].text} - [{professor_data[3].text}]")

			response = requests.get(f"https://myprofessor-get-ratings-api.onrender.com/professor?name={name}")
			rating_data = response.json()

			rating = float(rating_data["overall_rating"])
			difficulty = rating_data["difficulty"]
			would_take_again = rating_data["would_take_again"]
			qty = rating_data["ratings_quantity"]

			if rating > 3:
				print(f"[GOOD] {rating} - Difficulty: {difficulty} - Would take again: {would_take_again}% ({qty})")

				email = open_professor_page(driver, page_link)

				if email:
					send_email(professor_data[1].text, professor_data[0].text, name.split(" ")[-1], email)
					pass
			else:
				print(f"[NOT GOOD] {rating} - Difficulty: {difficulty} - Would take again: {would_take_again}% ({qty})")

print("\nDone scanning all professors.")
driver.quit()
