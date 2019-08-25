# MedMinder
An medication reminding application that uses your device camera to scan a Rx Label and create the reminders automatically
## Requirements
- Python3
	- Tesseract
	- pytesseract
	- OpenCV
	- Flask
		- Flask Forms
		- Flask WTF
	- pymySQL
	- SQLite
## Description
This project uses the device camera to scan Rx label and automatically populate a google calendar with reminders of dosage and refills
### Where I am in development?
- [x] Hosted 
- [x] Able to login
- [x] Able to open device camera and obtain ".jpg" of label
- [x] Able to scan image with text
- [x] Able to add rx automatic--Populates text block for user to copy and paste atm--*
- [x] Able to add rx manually
- [x] Able to remove rx
- [x] Email Reminder to User when Rx is added
- [x] Display Meds on Index
- [x] Display the calendar--Displays my calendar--not quite right yet--*
- [ ] Interface with Google Calendar API--calendar.py written but not tested or debugged yet--*
## File & Folder Organization
- File & Folder Organization
	- Folders
		- Templates folder holds html templates
		- SQL folder holds database schema
	- Files
		- main.py (main program)
		- ocr_simple.py (Object Character Recognition)
		- README.md
		- rqs.txt (requirements)
		- calendar.py (INCLUDED BUT NOT FINISHED)
		
## To Run the Application while Hosted
- Go to http://35.237.157.161:8080/ 

## To Run the Application if not Hosted
- Clone or download repo to desktop
- Open terminal and navigate to Med-Minder Folder
- Install rqs.txt from the terminal "pip3 install -r rqs.txt"
- Run "python3 main.py" in the terminal
- Open Firefox/Chrome or any other internet Browser and Input "http://localhost:8080" to view the web application
