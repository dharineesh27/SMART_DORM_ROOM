# Sensor Dashboard

## Overview
The Sensor Dashboard is a web-based application that displays real-time sensor data, including temperature, humidity, and light intensity. It also provides an LED control switch to toggle an LED on or off remotely. The project utilizes Firebase Realtime Database for data storage and retrieval.

## Features
- **Real-time sensor data visualization** using Chart.js
- **Temperature, Humidity, and Light Intensity Gauges**
- **Firebase Integration** for live updates
- **LED Control Switch** to turn the LED on/off remotely
- **Responsive UI Design** for easy accessibility

## Technologies Used
- HTML, CSS, JavaScript
- Chart.js (for data visualization)
- Firebase Realtime Database

## Setup Instructions
### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/sensor-dashboard.git
cd sensor-dashboard
```

### 2. Configure Firebase
- Create a Firebase project in the [Firebase Console](https://console.firebase.google.com/).
- Enable Realtime Database and set up security rules as needed.
- Replace the Firebase configuration in the JavaScript file with your own credentials:
```javascript
const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_AUTH_DOMAIN",
    databaseURL: "YOUR_DATABASE_URL",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_STORAGE_BUCKET",
    messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
    appId: "YOUR_APP_ID",
    measurementId: "YOUR_MEASUREMENT_ID"
};
```

### 3. Open in Browser
Simply open `index.html` in your preferred web browser.

## Firebase Database Structure
```
{
  "devices": {
    "light": false,
    "led_status": 0
  },
  "rfid_access": {
    "status": "Granted",
    "timestamp": 1738102204.4162657
  },
  "sensor_data": {
    "humidity": 41,
    "light_level": 187.5,
    "rfid_access": "Granted",
    "temperature": 31.6,
    "timestamp": 1740817230.4553773
  },
  "test": "Connection successful"
}
```

## How It Works
1. Sensor data is continuously updated in the Firebase Realtime Database.
2. The dashboard listens for changes and updates the UI in real time.
3. Users can toggle the LED using the switch, and the status is updated in Firebase.
4. A Raspberry Pi or microcontroller reads the LED status from Firebase and controls the LED accordingly.

## Contributing
Feel free to fork the repository and submit pull requests to improve the project!


