# Team Availability App - Complete Instructions (Updated)

## Overview
A Flask-based web application for tracking team member availability across multiple countries and regions, including holidays and out-of-office periods. The app provides an interactive calendar view showing only employees who are out of office with comprehensive history tracking.

## Core Requirements

### Framework & Structure
- **Backend**: Python Flask
- **Frontend**: HTML, CSS, Bootstrap 5, JavaScript
- **Data Storage**: JSON files (for development)
- **Code Location**: All code must be inside `src/` folder

### Key Features

#### 1. Holiday Management
- Store national and regional/state holidays
- Support for multiple countries (Australia, China, USA)
- Regional holidays for specific states/provinces (NSW, VIC, WA, Shanghai, California)
- Holidays appear automatically on calendar for team members in those locations
- Automatic holiday name detection and display

#### 2. Team Member Management
- Store team member information with country and region
- Support for multi-continental teams
- Link members to their specific holidays based on location
- **Specific Team Members Supported:**
  - Naga | Australia, NSW
  - Anuj | Australia, VIC  
  - Teresa | Australia, WA
  - Xing | China, Shanghai
  - Hang | China, Shanghai
  - Jeffery | USA, California

#### 3. Out of Office (OOO) Management
- Team members can add vacation dates, sick leave, personal time, etc.
- Interactive calendar-based OOO management (no separate tab needed)
- Ability to cancel/remove OOO entries
- Support for single-day and multi-day vacation periods

#### 4. Interactive Calendar Display
- **Primary View**: Monthly calendar showing ONLY employees who are out of office
- **Navigation**: Previous/Next month buttons
- **Interactive Features**: Add/remove OOO directly from calendar
- **Clean Display Format**: Simplified member status display
- **Visual Design**: Clean, professional interface with color coding

#### 5. History & Audit Trail (NEW)
- Complete operation tracking and audit trail
- Records all add/delete/cancel operations
- Timestamped entries with member attribution
- Operation summary and statistics
- Professional history display with categorized badges

## Detailed Feature Specifications

### Calendar View Features

#### Display Rules
- **Show Only OOO Employees**: Calendar displays only team members who are away
- **Empty Days**: Days with no OOO employees appear empty (clean view)
- **Color Coding**: Red background for unavailable employees
- **Simplified Display Format**: Clean member status display
  - **OOO Entries**: `Member Name | OOO`
  - **Public Holidays**: `Member Name | Country, Region (public holiday)`

#### Interactive Elements
1. **Add OOO Button (+)**
   - Small "+" button in top-right corner of each calendar day
   - Click to open modal dialog for adding OOO entry
   - Pre-fills the selected date as start date

2. **View/Edit Button (✎)**
   - Blue edit icon on each OOO entry
   - Opens detailed modal showing:
     - Employee name
     - Full vacation period (start to end dates)
     - Reason for absence
     - Total duration in days
     - "Cancel Entire Vacation" button

3. **Quick Delete Button (×)**
   - Red X button on each OOO entry
   - Quick removal of OOO for specific day
   - Confirmation dialog before deletion

#### Modal Dialogs
1. **Add OOO Modal**
   - Team member dropdown (all available members)
   - End date field (defaults to selected date)
   - Reason dropdown: Vacation, Sick Leave, Personal, Conference, Training, Other
   - Save/Cancel buttons

2. **OOO Details Modal**
   - Display complete vacation information
   - Option to cancel entire vacation period
   - Professional card-based layout

### Navigation Structure
- **Calendar Tab**: Main interactive calendar view
- **Members Tab**: Add/manage team members
- **Holidays Tab**: Add/manage national and regional holidays
- **History Tab**: View complete audit trail of all operations
- **No OOO Tab**: All OOO management happens in calendar

### Data Models

#### Team Members
```json
{
  "member_id": {
    "name": "Employee Name",
    "country": "Country Name",
    "region": "State/Region" // optional
  }
}
```

#### Holidays
```json
{
  "national": {
    "Country": {
      "YYYY-MM-DD": "Holiday Name"
    }
  },
  "regional": {
    "Country": {
      "Region": {
        "YYYY-MM-DD": "Regional Holiday Name"
      }
    }
  }
}
```

#### Out of Office
```json
{
  "member_id": [
    {
      "start_date": "YYYY-MM-DD",
      "end_date": "YYYY-MM-DD",
      "reason": "Vacation/Sick Leave/etc"
    }
  ]
}
```

#### History (NEW)
```json
[
  {
    "timestamp": "YYYY-MM-DD HH:MM:SS",
    "operation_type": "ADD_OOO|DELETE_OOO|CANCEL_VACATION|ADD_MEMBER|ADD_HOLIDAY",
    "member_id": "member_id_or_null",
    "member_name": "Member Name or System",
    "details": "Detailed description of operation"
  }
]
```

### Backend API Endpoints

#### Pages
- `GET /` - Main calendar view
- `GET /members` - Team member management
- `GET /holidays` - Holiday management
- `GET /history` - Operation history and audit trail

#### OOO Management APIs
- `POST /add_ooo` - Add new OOO entry (AJAX + form support)
- `POST /delete_ooo` - Remove single day OOO entry
- `POST /cancel_vacation` - Cancel entire vacation period
- `GET /api/ooo_details/<member_id>/<date>` - Get detailed OOO info

#### Other APIs
- `POST /add_member` - Add new team member
- `POST /add_holiday` - Add new holiday
- `GET /api/availability/<date>` - Get availability data for specific date

### Technical Implementation Details

#### Calendar Logic
- Display monthly calendar grid
- Calculate availability for each day considering:
  - National holidays for member's country
  - Regional holidays for member's region
  - OOO entries for date ranges
- Format reasons as "Holiday: [Name]" or "OOO: [Reason]"
- Show only unavailable employees (available = False)

#### Interactive JavaScript Features
- AJAX calls for seamless OOO management
- Modal dialog management with Bootstrap
- Event handlers for add/edit/delete buttons
- Real-time page updates without full refresh
- Error handling with user-friendly messages

#### CSS Styling
- Calendar grid with fixed height cells (150px)
- Hover effects on interactive elements
- Color-coded member status (red for unavailable)
- Responsive design for different screen sizes
- Professional button styling for calendar controls

### File Structure
```
src/
├── app.py                 # Main Flask application
├── templates/
│   ├── base.html         # Base template with navigation
│   ├── calendar.html     # Interactive calendar view
│   ├── members.html      # Team member management
│   ├── holidays.html     # Holiday management
│   └── history.html      # Operation history and audit trail
├── static/css/
│   └── style.css         # Custom styling
├── data/                 # JSON data storage
│   ├── members.json      # Team member data
│   ├── holidays.json     # Holiday data
│   ├── ooo.json          # Out of office data
│   └── history.json      # Operation history data
├── init_sample_data.py   # Sample data generator
├── requirements.txt      # Python dependencies
└── README.md            # Documentation
```

### Dependencies
```
Flask==2.3.3
Werkzeug==2.3.7
```

### Sample Data
Include sample data for:
- 6 specific team members: Naga (Australia, NSW), Anuj (Australia, VIC), Teresa (Australia, WA), Xing (China, Shanghai), Hang (China, Shanghai), Jeffery (USA, California)
- National and regional holidays for 2025 (Australia, China, USA with state/region specific holidays)
- Sample OOO entries with different date ranges
- Empty history.json file (will be populated as operations are performed)

### Visual Design Requirements
- **Bootstrap 5** for responsive design
- **Color Scheme**: 
  - Available: Green (#d4edda)
  - Unavailable: Red (#f8d7da)
  - Interactive elements: Blue (#0d6efd)
- **Typography**: Clean, professional fonts
- **Layout**: Card-based design with proper spacing
- **Icons**: Unicode symbols for buttons (×, ✎, +)

### Key Business Logic
1. **Holiday Detection**: Check national first, then regional holidays
2. **OOO Detection**: Check date ranges for overlapping periods
3. **Display Priority**: Only show employees who are unavailable
4. **Date Handling**: Proper datetime parsing and comparison
5. **Vacation Management**: Support both single-day and multi-day removal

### User Experience Requirements
- **Intuitive Navigation**: Clear tab structure
- **Quick Actions**: One-click add/remove from calendar
- **Visual Feedback**: Hover effects and color coding
- **Confirmation Dialogs**: Prevent accidental deletions
- **Responsive Design**: Works on desktop and mobile
- **Professional Appearance**: Clean, business-appropriate interface

## Implementation Notes
- Use JSON files for development (can be upgraded to database later)
- Implement proper error handling for all API endpoints
- Ensure AJAX calls have fallback error messages
- Use Flask's flash messaging for user feedback
- Maintain consistent date format (YYYY-MM-DD) throughout
- Handle timezone considerations for multi-continental teams

This application serves as a comprehensive team availability tracking system focused on absence management rather than general availability tracking.

## Latest Updates & New Features (2025)

### 1. History & Audit Trail System
- **Complete Operation Logging**: All user actions are automatically tracked
- **Timestamped Entries**: Every operation includes precise timestamp
- **Operation Categories**: ADD_OOO, DELETE_OOO, CANCEL_VACATION, ADD_MEMBER, ADD_HOLIDAY
- **Professional Display**: Color-coded badges and summary statistics
- **Full Traceability**: Who did what and when for complete audit compliance

### 2. Enhanced Calendar Display
- **Simplified Format**: Clean pipe-separated display
  - OOO entries: `Member Name | OOO`
  - Public holidays: `Member Name | Country, Region (public holiday)`
- **Location Context**: Holiday entries show member's specific location
- **Streamlined Interface**: Removed unnecessary details for cleaner view

### 3. Improved Team Member Support
- **Specific Team Configuration**: Pre-configured for actual team members
- **Regional Holiday Support**: Comprehensive holiday coverage for NSW, VIC, WA, Shanghai, California
- **Location-Aware Features**: Automatic holiday detection based on member location

### 4. Technical Improvements
- **Fixed Add OOO Issue**: Resolved JSON response compatibility for AJAX calls
- **Enhanced Holiday Detection**: Includes specific holiday names in backend logic
- **Better Error Handling**: Improved user feedback and error messages
- **Consistent Data Format**: Standardized date handling throughout application

### 5. Navigation Enhancement
- **Four-Tab Structure**: Calendar, Members, Holidays, History
- **Integrated OOO Management**: No separate OOO tab needed
- **Contextual Actions**: All vacation management happens directly in calendar
- **Professional Layout**: Clean, business-appropriate interface design

This updated version provides enterprise-level functionality with complete audit trails, making it suitable for professional team management and compliance requirements.
