$ErrorActionPreference = "Stop"

Write-Host "Validator"
python tests/validate_skill.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Python tests"
python -m unittest discover -s tests -p "test_*.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Installer dry run"
python install.py --target project --dry-run
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "OK"
