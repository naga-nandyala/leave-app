# Team Availability App

A comprehensive Flask-based web application for managing team member availability, holidays, and out-of-office (OOO) schedules across multiple countries and regions. The app provides a visual calendar interface to track team availability and automatically handles national and regional holidays.

## 🌟 Features

- **Multi-country Support**: Track team members across different countries with region-specific holiday support
- **Automatic Holiday Generation**: Automatically generates national and regional holidays using the `holidays` Python library
- **Calendar View**: Interactive monthly calendar showing team availability at a glance
- **Out-of-Office Management**: Track vacation, sick leave, conferences, and personal time off
- **Activity History**: Complete audit trail of all operations performed in the system
- **Real-time Availability**: Check availability for specific dates with detailed reasons for unavailability

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd leave_app
   ```

2. **Set up virtual environment**

   ```bash
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   cd src
   pip install -r requirements.txt
   ```

4. **Run the application**

   ```bash
   python app.py
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## 📋 How to Use

### Adding New Countries

The application supports adding new countries to the system for holiday tracking:

1. **Edit the countries configuration file**:
   - Navigate to `src/config/countries.json`
   - Add new countries in the following format:

   ```json
   {
     "countries": {
       "AU": {"name": "Australia", "code": "AU"},
       "US": {"name": "United States", "code": "US"},
       "UK": {"name": "United Kingdom", "code": "GB"},
       "DE": {"name": "Germany", "code": "DE"}
     }
   }
   ```

2. **Country codes must follow ISO 3166-1 alpha-2 standard** (e.g., US, GB, DE, FR, JP)

3. **Restart the application** after making changes to the configuration file

4. **Supported countries** include any country supported by the Python `holidays` library (100+ countries)

### Adding New Team Members

1. **Navigate to the Members page** (`/members`)

2. **Fill out the "Add New Member" form**:
   - **Name**: Full name of the team member
   - **Country**: Select from the dropdown of configured countries
   - **Region/State**: Select the appropriate region (automatically populated based on country)

3. **Click "Add Member"**

4. **The system will automatically**:
   - Generate holidays for the member's country and region
   - Log the addition in the activity history
   - Make the member available for OOO tracking

### Managing Team Members

- **View all members**: Visit the Members page to see all team members and their locations
- **Delete members**: Use the delete button next to each member (includes confirmation)
- **Member locations**: The system tracks unique countries and regions through the API

### Generating Holidays

The application automatically generates holidays, but you can manually trigger holiday generation:

1. **Automatic generation occurs when**:
   - A new team member is added
   - The system detects missing holiday data for current/next year

2. **Manual generation**:
   - Visit the Holidays page (`/holidays`)
   - Click "Generate Holidays" button
   - System generates holidays for:
     - Current year and next year
     - All countries where team members are located
     - All regions/states where team members are located

3. **Holiday data includes**:
   - **National holidays**: Country-wide holidays
   - **Regional holidays**: State/province-specific holidays
   - **Holiday names**: Official names in local language
   - **Weekday information**: Shows which day of the week holidays fall on

### Managing Out-of-Office (OOO) Schedules

1. **Adding OOO from Calendar**:
   - Click on any date in the calendar view
   - Select team member from dropdown
   - Choose start and end dates
   - Select reason (Vacation, Sick Leave, Conference, Personal)
   - Click "Add OOO"

2. **Adding OOO from Members page**:
   - Use the OOO form at the bottom of the Members page
   - Select member, dates, and reason

3. **Managing existing OOO**:
   - Click on unavailable dates in the calendar to view details
   - Cancel entire vacation periods
   - Delete specific OOO entries

4. **OOO Types supported**:
   - Vacation
   - Sick Leave
   - Conference
   - Personal
   - Custom reasons

### Viewing Activity History

1. **Navigate to History page** (`/history`)

2. **View complete audit trail** including:
   - **Member additions/deletions**: Track team changes
   - **Holiday generation**: See when holidays were updated
   - **OOO activities**: All vacation and leave entries
   - **Timestamps**: Exact date and time of each operation
   - **Details**: Comprehensive information about each action

3. **History includes**:
   - Operation type (ADD_MEMBER, DELETE_MEMBER, ADD_OOO, etc.)
   - Member information
   - Detailed descriptions
   - System-generated activities

## 🗂️ File Structure

```text
leave_app/
├── src/
│   ├── app.py                 # Main Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── config/
│   │   └── countries.json     # Country configuration
│   ├── data/                  # JSON data storage
│   │   ├── members.json       # Team member data
│   │   ├── holidays.json      # Holiday data
│   │   ├── ooo.json          # Out-of-office data
│   │   └── history.json      # Activity history
│   ├── static/css/
│   │   └── style.css         # Application styling
│   └── templates/            # HTML templates
│       ├── base.html         # Base template
│       ├── calendar.html     # Calendar view
│       ├── members.html      # Members management
│       ├── holidays.html     # Holiday management
│       └── history.html      # Activity history
└── tests/                    # Test files
```

## 🌍 Supported Countries and Regions

The application supports 100+ countries through the Python `holidays` library, including:

- **United States**: All 50 states + DC
- **Canada**: All provinces and territories
- **Australia**: All states and territories
- **Germany**: All federal states
- **United Kingdom**: England, Scotland, Wales, Northern Ireland
- **And many more...**

### Region Support Examples

- **US States**: California, New York, Texas, Florida, etc.
- **Australian States**: New South Wales, Victoria, Queensland, etc.
- **Canadian Provinces**: Ontario, British Columbia, Quebec, etc.
- **German States**: Bavaria, Berlin, Hamburg, etc.

## 🔧 API Endpoints

The application provides several API endpoints for integration:

- `GET /api/regions/<country>` - Get regions for a country
- `GET /api/member_locations` - Get all member countries and regions
- `POST /api/generate_holidays` - Generate holidays for all locations
- `GET /api/availability/<date>` - Get team availability for a specific date
- `GET /api/ooo_details/<member_id>/<date>` - Get OOO details for a member

## 🛠️ Technical Details

- **Framework**: Flask (Python web framework)
- **Holiday Data**: Python `holidays` library (automatically updated)
- **Data Storage**: JSON files (easily portable, no database required)
- **Frontend**: HTML5, CSS3, JavaScript (vanilla)
- **Responsive Design**: Works on desktop and mobile devices

## 📝 Data Management

- **Automatic backups**: Consider implementing regular backups of the `data/` directory
- **Data migration**: JSON format makes it easy to migrate to a database later
- **Holiday updates**: The holidays library is regularly updated with new holiday data

## 🔍 Troubleshooting

1. **Missing holidays**: Run holiday generation from the Holidays page
2. **Region not found**: Check if the country code is correct in `countries.json`
3. **Application won't start**: Ensure virtual environment is activated and dependencies are installed
4. **Calendar not loading**: Check that member data exists and is valid JSON

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).