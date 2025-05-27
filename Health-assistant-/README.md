# Hostel Health Assistant

A Streamlit-based health assistant application designed specifically for hostel students. The app provides symptom analysis, health tracking, and information about common seasonal diseases.

## Features

- 🟢 Basic Features
  - Symptom input and analysis
  - Home remedy suggestions
  - Clear session output

- 🟡 Medium Features
  - Symptom matching with predefined keywords
  - Health log storage
  - Serious symptom alerts
  - Input validation

- 🔴 Advanced Features
  - Daily health tracking
  - Personalized advice based on symptom patterns
  - Research component for seasonal diseases

## Setup

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory and add your Google API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

## Running the Application

1. Activate the virtual environment if not already activated
2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
3. The application will open in your default web browser

## Usage

1. Use the sidebar to navigate between different sections
2. In "Log Symptoms":
   - Enter your symptoms in the text area
   - Click "Analyze Symptoms" to get AI-powered analysis
3. In "View Health Log":
   - View your symptom history
   - Check symptom trends through visualizations
4. In "Seasonal Disease Info":
   - Learn about common seasonal diseases
   - Access first aid tips and precautionary measures

## Note

This application is for educational purposes only and should not replace professional medical advice. Always consult a healthcare provider for proper medical diagnosis and treatment.

# Hospital Health Assistant Android App

This is the Android version of the Hospital Health Assistant application, built using Kivy framework.

## Features

- User Authentication (Login/Register)
- Symptom Logging
- Health Log Viewing
- Personalized Health Advice
- Seasonal Disease Information
- First Aid Guidelines

## Prerequisites

- Python 3.7 or higher
- Buildozer
- Android SDK
- Java JDK

## Installation

1. Install Buildozer:
```bash
pip install buildozer
```

2. Install required system dependencies (on Ubuntu/Debian):
```bash
sudo apt-get install python3-pip build-essential git python3 python3-dev ffmpeg libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev zlib1g-dev
```

3. Install Android SDK and Java JDK:
```bash
sudo apt-get install openjdk-11-jdk
```

## Building the Android App

1. Navigate to the project directory:
```bash
cd Health-assistant-
```

2. Initialize Buildozer:
```bash
buildozer init
```

3. Build the Android APK:
```bash
buildozer android debug deploy run
```

The first build may take a while as it downloads and sets up the Android SDK and other dependencies.

## Running the App

1. Connect your Android device via USB
2. Enable USB debugging on your device
3. Run the build command above
4. The app will be installed and launched on your device

## Project Structure

- `android_app.py`: Main application file
- `buildozer.spec`: Buildozer configuration file
- `health_logs.csv`: Database for storing health logs
- `users.csv`: Database for storing user information

## Notes

- Make sure your Android device is running Android 5.0 or higher
- The app requires internet connection for AI-powered health advice
- All data is stored locally on the device
- The app requires storage permissions to save health logs

## Troubleshooting

If you encounter any issues during the build process:

1. Make sure all dependencies are properly installed
2. Check if your Android device is properly connected and USB debugging is enabled
3. Try cleaning the build:
```bash
buildozer android clean
```

4. Check the buildozer logs for specific error messages

## License

This project is licensed under the MIT License - see the LICENSE file for details. 