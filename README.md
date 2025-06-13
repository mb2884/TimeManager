# TimeManager 📅

> **Academic Workload Management Platform for Princeton Students**

A comprehensive web application designed to help Princeton students efficiently organize their academic workload by intelligently distributing assignments across available time slots while accounting for existing commitments.

[![Live Demo](https://img.shields.io/badge/🌐_Live_Demo-Visit_App-blue?style=for-the-badge)](https://timemanager-moig.onrender.com)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/mb2884/TimeManager)

---

## 🎯 Project Overview

TimeManager transforms the overwhelming task of academic scheduling into a streamlined, automated process. Students can input their recurring commitments and assignment deadlines, and our intelligent algorithm automatically breaks down large tasks into manageable time blocks distributed optimally across their available schedule.

### ✨ Key Features

- **🔐 Secure Authentication**: Princeton CAS integration for seamless university login
- **📊 Intelligent Task Distribution**: Automated algorithm distributes work sessions based on user preferences and available time
- **🎨 Interactive Calendar Interface**: Drag-and-drop functionality with multiple view modes (monthly, weekly, daily)
- **⚙️ Customizable Settings**: Personalized work session duration, padding time, and preferred working hours
- **📱 Responsive Design**: Optimized for desktop and mobile devices
- **🔄 Real-time Updates**: Live calendar synchronization with instant feedback

---

## 🛠️ Tech Stack

### **Backend**
- **Framework**: Flask (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: Princeton CAS (Central Authentication Service)
- **Deployment**: Render Cloud Platform

### **Frontend**
- **Languages**: JavaScript (ES6+), HTML5, CSS3
- **Libraries**: FullCalendar.js, jQuery, AJAX
- **UI/UX**: Responsive design with custom CSS animations

### **Database Schema**
- **Users**: Stores authentication and user preferences
- **Events**: Manages recurring and one-time calendar events
- **Tasks**: Handles assignment data and scheduling parameters

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL
- Node.js (for frontend dependencies)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/mb2884/TimeManager.git
   cd TimeManager
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database**
   ```bash
   # Set up PostgreSQL database
   # Update connection string in config.py
   ```

5. **Run the application**
   ```bash
   python timemanager.py
   ```

6. **Access the application**
   - Navigate to `http://localhost:5000`
   - Login with Princeton CAS credentials

---

## 📈 Core Algorithm

Our **intelligent task scheduling algorithm** analyzes:
- User's available time slots
- Existing calendar commitments  
- Preferred work session duration
- Padding time between activities
- Assignment deadlines and estimated completion time

The system then optimally distributes work sessions to maximize productivity while respecting user preferences and time constraints.

---

## 🧪 Testing & Quality Assurance

- **Unit Testing**: Comprehensive test suite with 72% code coverage
- **Integration Testing**: Full end-to-end workflow validation
- **User Acceptance Testing**: Validated with Princeton student focus groups
- **Boundary Testing**: Extensive edge case validation
- **Performance Testing**: Optimized for concurrent user loads

---

## 👥 Team & Contributions

**Development Team:**
- **Matthew Barrett** (mb2884@princeton.edu) - *Full-Stack Developer & Database Architect*
- **Shelby Fulton** (sf5381@princeton.edu) - *Project Lead & Frontend Developer*  
- **Jessica Lin** (jl0274@princeton.edu) - *Frontend Developer & UI/UX Designer*
- **Alfred Ripoll** (ar7987@princeton.edu) - *Backend Developer & Testing Engineer*

### My Key Contributions:
- **Database Architecture**: Designed and implemented PostgreSQL schema with optimized indexing
- **Backend API Development**: Built RESTful endpoints using Flask and SQLAlchemy
- **Algorithm Implementation**: Developed core task scheduling and time allocation algorithms
- **Code Quality**: Implemented comprehensive testing framework and error handling

---

## 🔮 Future Enhancements

- **Google Calendar Integration**: Bidirectional sync with external calendar systems
- **Mobile Application**: Native iOS and Android applications
- **AI-Powered Recommendations**: Machine learning for personalized productivity insights
- **Multi-University Support**: Expand beyond Princeton to other educational institutions

---

## 📝 License

This project is part of academic coursework at Princeton University (COS 333 - Advanced Programming Techniques).

---

## 🤝 Connect

- **LinkedIn**: [matthew-w-barrett](https://linkedin.com/in/matthew-w-barrett)
- **Email**: mb2884@alumni.princeton.edu
- **Portfolio**: [View More Projects](https://github.com/mb2884)

---

*Built with ❤️ at Princeton University | Spring 2024*
