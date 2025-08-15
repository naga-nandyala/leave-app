# Team Availability App

A Flask-based web application to track team member availability across multiple countries and regions, including holidays and out-of-office periods.

## Features

1. **Holiday Management**: Store and manage national and regional/state holidays
2. **Team Member Management**: Track team members and their locations (country/region)
3. **Out of Office Tracking**: Allow team members to add vacation and other OOO dates
4. **Calendar View**: Display a monthly calendar showing team member availability

## Installation

1. Navigate to the app directory:
   ```bash
   cd app
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Initialize with sample data:
   ```bash
   python init_sample_data.py
   ```

## Running the Application

1. Start the Flask development server:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

### 1. Managing Team Members
- Go to the "Members" tab
- Add team members with their name, country, and region/state
- View all current team members

### 2. Managing Holidays
- Go to the "Holidays" tab
- Add national holidays (apply to entire country)
- Add regional holidays (apply to specific states/regions)
- View all current holidays organized by country and region

### 3. Managing Out of Office
- Go to the "Out of Office" tab
- Add OOO entries for team members with start/end dates and reason
- View all current OOO entries organized by team member

### 4. Viewing Availability Calendar
- The main "Calendar" tab shows a monthly view
- Each day shows team member availability status
- Green indicates available, red indicates unavailable (holiday or OOO)
- Navigate between months using the Previous/Next buttons

## Data Storage

The application uses JSON files for data storage in the `data/` directory:
- `members.json`: Team member information
- `holidays.json`: Holiday data organized by country and region
- `ooo.json`: Out of office entries for each team member

## API Endpoints

The application also provides a REST API endpoint:
- `GET /api/availability/<date>`: Returns availability data for all team members on a specific date (YYYY-MM-DD format)

## Sample Data

Run `python init_sample_data.py` to populate the application with sample data including:
- 5 team members from Australia, China, and USA
- National and regional holidays for 2025
- Sample out of office entries

## Customization

You can customize the application by:
- Adding more countries and regions in the dropdown menus (edit templates)
- Modifying the calendar view styling (edit `static/css/style.css`)
- Adding more OOO reason types (edit the OOO template)
- Implementing additional features like email notifications or export functionality

## Production Deployment

For production use, consider:
- Using a proper database (PostgreSQL, MySQL) instead of JSON files
- Adding user authentication and authorization
- Implementing proper error handling and logging
- Using environment variables for configuration
- Setting up proper WSGI server (Gunicorn, uWSGI)
- Adding data validation and sanitization

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, Bootstrap 5
- **Data Storage**: JSON files (for development)
- **Styling**: Bootstrap 5 + Custom CSS
