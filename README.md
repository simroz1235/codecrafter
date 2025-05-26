# Code Crafters

## SDG Goal: 3 - Good Health and Well-being

### Problem Statement:
The **Medicine Availability Tracker** project aims to address the challenges faced by rural pharmacies in managing their inventory, tracking stock levels, and ensuring medicine availability. Many rural pharmacies struggle with maintaining an organized stock system, leading to issues like expired medicines and stock shortages. This project seeks to solve these problems by providing a simple and user-friendly application that helps pharmacists monitor inventory, track stock levels, and receive timely notifications for low stock and expiry dates.

### Approach:
To tackle this problem, we developed a **Medicine Availability Tracker** with the following key features:

1. **Database Integration**: 
   - We integrated a local **SQLite** database to store critical information about the medicines, including name, quantity, expiry date, and price.

2. **Medicine Management**: 
   - The app enables pharmacists to add new medicines, view existing inventory, and search for specific medicines. Alerts are triggered when stock is low or when medicines are nearing their expiry date.

3. **OTP-Based Authentication**: 
   - For secure access, the application uses an **OTP (One-Time Password)** system. An OTP is sent via email to the user, ensuring that only authorized individuals can access the system.

4. **User Interface**: 
   - Built with **Flet**, the app offers a responsive and intuitive interface, making inventory management easy for pharmacists. Key features include:
     - Adding new medicines
     - Searching for medicines
     - Viewing the inventory with stock and expiry status
     - OTP-based secure login

5. **Email Notifications**: 
   - OTPs are sent through email to ensure secure login and protect user access.

### Tools Used:
- **Flet**: Used for developing the front-end interface, providing an interactive and responsive user experience.
- **SQLite**: A lightweight database for storing and managing medicine data locally.
- **Python (smtplib)**: Used for sending OTPs via email to authenticate users.
- **SSL**: Ensures secure communication during OTP email transmission.

### Note: This project was built *without using any AI help*. The focus is on building a practical, functional solution to manage pharmacy inventories with secure user authentication.

### How the App Solves the Problem:
This application directly addresses the challenges faced by rural pharmacies by providing the following solutions:
- **Inventory Tracking**: Easily manage the stock of medicines, including quantity, expiry dates, and prices.
- **Timely Alerts**: Get notifications for low stock or expiring medicines, allowing pharmacists to take proactive actions.
- **Secure Login**: OTP authentication ensures that only authorized users can access the system.
- **User-Friendly Interface**: The intuitive interface simplifies inventory management, even in rural areas where advanced systems may not be available.

### Conclusion:
The **Medicine Availability Tracker** app is a practical and effective solution for rural pharmacies. It simplifies inventory management, provides essential alerts for stock levels and expiry dates, and ensures secure login for authorized users. This helps improve pharmacy management, reduce medicine wastage, and guarantee timely availability of medicines for patients in rural areas.

---

### Instructions to Run the Application:

1. Ensure **Python** is installed on your machine.
2. Install the required libraries by running the following command:
   ```bash
   pip install smtplib ssl flet sqlite3
