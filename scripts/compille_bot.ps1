# Activate the virtual environment
& .\venv\Scripts\activate.ps1

# Define the command to run import_verification.py
$verify_command = "py -3.11 ..\src\utils\publish\import_verification.py"

# Execute the import verification script and capture the exit code
$verification_status = (Invoke-Expression $verify_command)

# Check the exit code (error level) of the verification script
if ($verification_status -ne 0) {
    Write-Host $verification_status
    Write-Host "Import verification failed. Do you want to continue? (Press Enter to continue or Ctrl+C to abort)"
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

# Define the nuitka command
$nuitka_command = "nuitka --clang --mingw64 --onefile --follow-imports --windows-icon-from-ico=.\Item_Gem.ico --remove-output --output-filename=Bot --windows-company-name=Unknown --windows-product-version=1.0 --onefile-tempdir-spec=C:\Users\Default\AppData\Local\Temp\bot_unknown ..\app.py"

# Execute the nuitka command
Invoke-Expression $nuitka_command

# Set the current date
$current_date = Get-Date -Format "yyyy-MM-dd"

# Set the new filename
$new_filename = ".\\output\\bot_executable_$($current_date)\\bot-$($current_date).exe"

# Create the new directory
New-Item -ItemType Directory -Force -Path ".\\output\\bot_executable_$($current_date)"

# Move the bot.exe file
Move-Item -Force -Path ".\\bot.exe" -Destination $new_filename

# Copy the resources directory
Copy-Item -Recurse -Force -Path ".\\resources" -Destination ".\\output\\bot_executable_$($current_date)\\resources"

# SIG # Begin signature block
# MIIFkQYJKoZIhvcNAQcCoIIFgjCCBX4CAQExCzAJBgUrDgMCGgUAMGkGCisGAQQB
# gjcCAQSgWzBZMDQGCisGAQQBgjcCAR4wJgIDAQAABBAfzDtgWUsITrck0sYpfvNR
# AgEAAgEAAgEAAgEAAgEAMCEwCQYFKw4DAhoFAAQUCUp4BrW5xTZM3AQXeNHoGbHe
# Q8ugggMqMIIDJjCCAg6gAwIBAgIQeGuKWXJDj7lOKwmg16J10DANBgkqhkiG9w0B
# AQsFADAcMRowGAYDVQQDDBFQb3dlclNoZWxsU2NyaXB0czAeFw0yNDAzMDIxMzQ2
# NDRaFw0yNTAzMDIxNDA2NDRaMBwxGjAYBgNVBAMMEVBvd2VyU2hlbGxTY3JpcHRz
# MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAx4fvditFZiFUYbydgh+n
# poae/1D9FuUteg4PAbipAKfNGvkB+I91YqJc68t/lqfI0UPhcBkx7gG3OQduVrr1
# kv6Fhv3TuaF3kVRGZORaDFRxolYIb7esrKzBqwAmtzGbR1T5Yd23zCLbwo55R+ah
# WXQxI/Cmw1h1dZFq4cMhMRpYbhYn0yRPLeL9+nqkWC+QPqOBaPW1eRYeJEmvFhwf
# PzhE72NsXOYfUFgbia+bJjJgEVzB7YWw2RZHSfMQMX1BrvBTR13DjjLj5G+S32k8
# askmHacqJT6tEviwsEAAyg9Q6CnF+jafKT/dbJX+4rv5EnGwjBUSnPxs1/7CkD2l
# lQIDAQABo2QwYjAOBgNVHQ8BAf8EBAMCB4AwEwYDVR0lBAwwCgYIKwYBBQUHAwMw
# HAYDVR0RBBUwE4IRUG93ZXJTaGVsbFNjcmlwdHMwHQYDVR0OBBYEFO/HJ5LowD2k
# MiLS9z5uB8b7eKRyMA0GCSqGSIb3DQEBCwUAA4IBAQCLhfJA/k3KOaa6VKLoBkys
# cEujzFC7wl3LWkukqs3m4aLQ3k5js5dWmZOBZugAalcI3psuJTF2YBR/cXYxeb8B
# Pi2ki/VEgGDgRllnLkIH/WRokmJpI2c72gA0HY3U7XK19biYPRArMcTXFG0z8esr
# 3pLmLv2GW9d2W7CLocMW+YsZDWTIEQhQwrNsCEWs+7tXVq3Z40bueS4QmEk3YmBA
# XygFtz0sK0gTS4KF66NrdZG1O778cGDeLvs2kFkyoPAJWZJcAb2xz696GZE4WBlU
# p4CSAsgJCNhwakRUVwWKjTtGqfea0gET2wpY7UX7SHScOdr21XcTXbVHZ0NwTYcw
# MYIB0TCCAc0CAQEwMDAcMRowGAYDVQQDDBFQb3dlclNoZWxsU2NyaXB0cwIQeGuK
# WXJDj7lOKwmg16J10DAJBgUrDgMCGgUAoHgwGAYKKwYBBAGCNwIBDDEKMAigAoAA
# oQKAADAZBgkqhkiG9w0BCQMxDAYKKwYBBAGCNwIBBDAcBgorBgEEAYI3AgELMQ4w
# DAYKKwYBBAGCNwIBFTAjBgkqhkiG9w0BCQQxFgQUxSHxrsb6ijkGVQU1WIXGgH2r
# uQ0wDQYJKoZIhvcNAQEBBQAEggEAeW0Ua2UOIDRl7fLXjPBZub0tK7oqIqvPJe9Z
# fQ+eGZ0+Li9sMq4nuqmbQxaTGpST/+wmGLHRXnHWmjMQQ0/H7Y15E3fF1bRmR9IE
# jcPkwIK8WISHzmFmR8+9mEdNrxjkzVY6O/z1VfMaUMkoQ3wt3bIogCNuX8bxPnap
# 4e1U1y0U8BQFalN6P8hzROy+BfSBteYflDppgc4TkEmZRNqkZvjMNRy9FeeqImoy
# OKman0MjMefbJX+V7Rmr6RgeC7mofIyKop5L/QZVZ+gE1oBv4C4886bYujoF4T4j
# FC5OnDqaSpxmDjKKdajJxn4LAvRvrBPs0SOpVtyeGVoep2wX1Q==
# SIG # End signature block
