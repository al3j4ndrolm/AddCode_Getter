# Add Code Requester Automation Script


**Add Code Requester Automation (ACRA)** is a Python automation tool that helps students at De Anza College
find professors with good ratings and automatically send them email requests (e.g. for
add codes). It uses Selenium to scrape the De Anza College course schedule for a given
class, checks each professor's rating via RateMyProfessor, and emails those professors
who meet a specified rating threshold.
---
## Key Features
- Search De Anza College course listings by department & class number
- Filter professors by overall rating (default: 3.0+)
- Send personalized emails via Gmail (using `yagmail`)
- Uses RateMyProfessor data to evaluate professors
- Easily customizable rating threshold & email template
---
## Getting Started
1. Install dependencies:
```
```
pip install selenium webdriver-manager yagmail requests
2. Set up Gmail SMTP access:
Use your Gmail and an App Password for yagmail:
```python
yag = yagmail.SMTP("your_email@gmail.com", "your_app_password")
```
3. Run the script:
```
python professors_finder.py
```
When prompted, enter the class code (e.g., `MATH`) and class number (e.g., `1A`).
---
## Email Criteria & Customization
- Rating Threshold:
Default is `rating > 3.0`. To change it, modify this line:
```python
if rating > 3:
```
- Custom Email Template:
Located inside `send_email()` function. Here's the default template:
```
Subject: Add code request - {class_name} ({class_code})
Good morning, Professor {professor_last_name},
I hope this message finds you well. My name is [Your Name], and I'm writing to kindly
request an add code for your {class_name} ({class_code}) class this quarter.
This course is very important for my plan to transfer in the coming fall. I've
reviewed the syllabus and am genuinely excited to learn from you. If there's any
possibility to receive an add code, I would be truly grateful.
Thank you so much for your time and consideration.
Warm regards,
[Your Name]
SID: [Your Student ID]
```
---
## Requirements
- Python 3.6+
- Chrome browser installed
- Pip packages:
- selenium
- webdriver-manager
- yagmail
- requests
---
## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what
you'd like to change.
Steps:
1. Fork this repo
2. Create a new branch: `git checkout -b feature/my-feature`
3. Commit your changes
4. Push to your fork and submit a PR
---
## License
This project is licensed under the MIT License - see the LICENSE file for details.
