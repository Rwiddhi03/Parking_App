 # Smart Parking Management System (Web-Based)
 # Overview

The Smart Parking Management System is a web-based application designed to efficiently manage parking space allocation across multiple parking lots. The system automates the process of booking, assigning, and releasing parking spots while maintaining a record of past transactions.
It eliminates manual tracking and ensures optimal utilization of parking resources through dynamic allocation and real-time availability updates.

# Key Features
## Authentication & User Handling
Generates unique user IDs automatically based on session data
Ensures each booking is associated with a specific user
Maintains controlled interaction with the system
## Frontend (User Interface)
Responsive UI built using HTML, CSS, and Jinja2
Displays:
Available parking slots
Booking details
Parking history
Simple and intuitive navigation for seamless user experience
## Backend Logic
Built using Flask (Python)
Implements:
Dynamic parking slot allocation
Booking and release workflows
Routing for different system operations
Ensures efficient handling of requests and data flow
## Database Management
Uses SQLite3 for persistent data storage
Stores:
Parking lot details (28 lots × 25 spots)
Spot availability
Active bookings
Released ticket history
Supports efficient querying and updates
## System Workflow
User enters vehicle number
System automatically:
Assigns parking lot
Allocates available spot
Generates unique user ID
Booking is stored in the database
On release:
Spot becomes available again
Booking moves to history (released tickets)
