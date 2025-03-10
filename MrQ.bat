@echo off
REM Set CONDA_FORCE_32BIT environment variable
set CONDA_FORCE_32BIT=1

REM Change directory to the specified path
cd C:\Users\coron\OneDrive\Mr.Q

REM Activate the conda environment
call conda activate pyqt5-py38-32bit

REM Run the Python script
python main.py

REM Pause to keep the command line window open
pause