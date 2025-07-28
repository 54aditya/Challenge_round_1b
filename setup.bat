@echo off

REM Challenge 1B Setup Script for Windows
REM This script sets up the necessary directory structure for the project

echo Setting up Challenge 1B directory structure...

REM Create necessary directories
mkdir input\PDFs 2>nul
mkdir output 2>nul
mkdir desired 2>nul

REM Create .gitkeep files to ensure folders are tracked by Git
echo # This file ensures the input directory is tracked by Git > input\.gitkeep
echo # This file ensures the PDFs directory is tracked by Git > input\PDFs\.gitkeep
echo # This file ensures the output directory is tracked by Git > output\.gitkeep
echo # This file ensures the desired directory is tracked by Git > desired\.gitkeep

echo Directory structure created successfully!
echo.
echo Next steps:
echo 1. Place your input JSON file in the 'input' directory
echo 2. Place your PDF documents in the 'input\PDFs' directory
echo 3. Run: python main.py "input\your_input.json" "output\your_output.json"
echo.
echo For Docker usage:
echo 1. Build: docker build --platform linux/amd64 -t challenge1b:latest .
echo 2. Run: docker run --rm -v %cd%\input:/app/input -v %cd%\output:/app/output --network none challenge1b:latest "your_input.json" "your_output.json"
pause 