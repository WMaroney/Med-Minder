# MedMinder
An medication reminding application that uses your device camera to scan a Rx Label and create the reminders automatically
## Requirements
- Python3
	- Tesseract
	- pytesseract
	- OpenCV
	- Flask
		-Flask Forms
		-Flask WTF
	- pymySQL
	- SQLite

## Description
This project uses the device camera to scan Rx label and automatically populate a google calendar with reminders of dosage and refills
### Where I am in development?
- [x] Hosted 
- [x] Able to login
- [x] Able to open device camera and obtain ".jpg" of label
- [x] Able to scan image with text and output text to ".txt" file
- [x] Able to add rx automatic--Populates text block for user to copy and paste atm--*
- [x] Able to add rx manual
- [x] Able to remove rx
- [x] Display the calendar--Displays my calendar--not quite right yet--*
- [ ] Interface with Google Calendar API--calendar.py written but not tested or debugged yet--*

## File & Folder Organization
-Folder Organization
	-Templates folder holds html templates
	-SQL folder holds database schema
-Files
	-main.py (main program)
	-ocr_simple.py (Object Character Recognition)
	-README.md
	-rqs.txt (requirements)
	-calendar.py (NOT INCLUDED/FINISHED)
