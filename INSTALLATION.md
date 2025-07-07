# Installation Guide

This guide will help you install everything needed to run the Closed Curve Generator, even if you're new to Python.

## 🐍 What is Python?

Python is a programming language that's great for beginners. It's like giving instructions to your computer in a language that's close to English.

## 📋 Prerequisites

Before we start, you need:
- A computer (Windows, Mac, or Linux)
- Internet connection
- Basic computer skills (downloading files, using a web browser)

## 🖥️ Installing Python

### Windows

1. **Download Python**:
   - Go to [python.org](https://www.python.org/downloads/)
   - Click the big yellow "Download Python" button
   - Choose the latest version (like Python 3.11 or 3.12)

2. **Install Python**:
   - Run the downloaded file (it will be named something like `python-3.11.0-amd64.exe`)
   - **IMPORTANT**: Check the box that says "Add Python to PATH"
   - Click "Install Now"
   - Wait for installation to complete

3. **Verify Installation**:
   - Open Command Prompt (search for "cmd" in the Start menu)
   - Type: `python --version`
   - You should see something like "Python 3.11.0"

### macOS

1. **Option 1 - Using Homebrew (Recommended)**:
   - Open Terminal (search for "Terminal" in Spotlight)
   - Install Homebrew first (if you don't have it):
     ```bash
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```
   - Install Python:
     ```bash
     brew install python
     ```

2. **Option 2 - Download from python.org**:
   - Go to [python.org](https://www.python.org/downloads/)
   - Download the macOS installer
   - Run the installer and follow the instructions

3. **Verify Installation**:
   - Open Terminal
   - Type: `python3 --version`
   - You should see the Python version

### Linux (Ubuntu/Debian)

1. **Install Python**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```

2. **Verify Installation**:
   ```bash
   python3 --version
   ```

## 📦 Installing Required Packages

Once Python is installed, you need to install the libraries our application uses.

### What are Packages/Libraries?

Think of packages as "add-ons" that give Python extra abilities. Our app needs:
- **Streamlit**: Creates the web interface
- **Pillow**: Handles image creation and saving

### Installation Steps

1. **Open Terminal/Command Prompt**:
   - Windows: Search for "cmd" or "PowerShell"
   - Mac: Search for "Terminal"
   - Linux: Open Terminal

2. **Navigate to the project folder**:
   ```bash
   cd /path/to/your/closed_curve/folder
   ```
   
   For example, if your project is on the Desktop:
   ```bash
   cd ~/Desktop/closed_curve
   ```

3. **Install the required packages**:
   ```bash
   pip install streamlit pillow
   ```
   
   On Mac/Linux, you might need:
   ```bash
   pip3 install streamlit pillow
   ```

4. **Verify Installation**:
   ```bash
   python -c "import streamlit, PIL; print('All packages installed successfully!')"
   ```

## 🚀 Running the Application

1. **Make sure you're in the project directory**:
   ```bash
   cd /path/to/closed_curve
   ```

2. **Start the application**:
   ```bash
   streamlit run step6_final_version.py
   ```

3. **Open your web browser**:
   - The app will automatically open at `http://localhost:8501`
   - If it doesn't open automatically, manually go to that address

## 🔧 Troubleshooting

### "Python is not recognized" (Windows)
- Make sure you checked "Add Python to PATH" during installation
- Try restarting your computer
- Or reinstall Python and check the PATH option

### "Permission denied" (Mac/Linux)
- Try using `sudo`:
  ```bash
  sudo pip3 install streamlit pillow
  ```

### "pip not found"
- Try using `pip3` instead of `pip`
- Or install pip separately:
  ```bash
  python -m ensurepip --upgrade
  ```

### "Port already in use"
- The app might already be running
- Try a different port:
  ```bash
  streamlit run step6_final_version.py --server.port 8502
  ```

### "Module not found"
- Make sure you installed the packages:
  ```bash
  pip install streamlit pillow
  ```

## 📚 Next Steps

Once everything is installed:
1. Read the [USAGE_GUIDE.md](USAGE_GUIDE.md) to learn how to use the app
2. Check out [EXAMPLES.md](EXAMPLES.md) for example parameters
3. Experiment with different settings!

## 🆘 Getting Help

If you're stuck:
1. Check the error message carefully
2. Make sure Python and packages are installed correctly
3. Try restarting your terminal/command prompt
4. Search online for the specific error message

## 🎯 Quick Test

To make sure everything works, try this:
```bash
python -c "print('Hello, Python is working!')"
```

If you see "Hello, Python is working!", you're ready to run the Closed Curve Generator! 