@echo off
REM Windows helper script to run codeinspector in Docker

REM Check if image exists, if not build it
docker image inspect codeinspector >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Building Docker image...
    docker build -t codeinspector .
)

REM Run the container with current directory mounted to /workspace
REM And mount the codeinspector code to /app (so it works from anywhere)
REM We need to find the directory where this script is located
set SCRIPT_DIR=%~dp0
REM Remove trailing backslash
set SCRIPT_DIR=%SCRIPT_DIR:~0,-1%

docker run --rm -it ^
  -v "%cd%":/workspace ^
  -v "%SCRIPT_DIR%":/app ^
  -w /workspace ^
  -e GOOGLE_API_KEY="%GOOGLE_API_KEY%" ^
  -e GITHUB_TOKEN="%GITHUB_TOKEN%" ^
  -e PYTHONPATH=/app ^
  codeinspector %*
