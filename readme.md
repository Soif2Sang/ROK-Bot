# RokBot (NO LONGER MAINTAINED)

## Installation

1. Clone the repository: `git clone <repository_url>`
2. Navigate to the project directory: `cd <project_directory>`
3. Install the required Python packages: `pip install -r requirements.txt`
4. Setup your Supabase URL:
   - Open the `utils/constants.py` file.
   - Set the `SUPABASE_URL` variable to your Supabase URL.
   - Set the `SUPABASE_KEY` variable to your Supabase Key.
   - Save and close the file.
5. Import the dump schema.sql into your supabase database.

## Packaging the Application

We use Nuitka to package the application as an executable. Run the following command:

```powershell
nuitka --clang --mingw64 --onefile --follow-imports --windows-icon-from-ico=.\Item_Gem.ico --remove-output --output-filename=Bot --windows-company-name=Unknown --windows-product-version=1.0 --onefile-tempdir-spec=C:\Users\Default\AppData\Local\Temp\bot_unknown .\app.py
```

## Import Verification

Before packaging the application, we need to ensure all imports are correct. To do this, run the following command:

```powershell
py -3.11 import_verification.py
```

This command runs a script that checks all file imports in the project.

## Automation Script

We also provide a PowerShell script (compile_bot.ps1) that automates the process of activating the virtual environment, verifying imports, packaging the application with Nuitka, and moving the resulting executable to a new directory with the current date.
