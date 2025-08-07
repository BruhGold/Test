# Test

# Prep and activate env
python -m venv venv
source venv/bin/activate # for Linux/MacOS
.\venv\Scripts\activate.bat # for Windows command line
.\venv\Scripts\Activate.ps1 # for Windows PowerShell

# Download requirements
pip install -r requirements.txt

# Updating .env
update the .env file to match your moodle database for testing