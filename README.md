# Team Availability & Leave Management App

A comprehensive Flask-based web application for managing team member availability, tracking holidays, and handling out-of-office (OOO) requests across multiple countries and regions.

## Features Overview

### 🗓️ **Calendar View**
- Interactive monthly calendar displaying team availability
- Visual indicators for holidays and out-of-office periods
- Quick OOO entry directly from calendar dates

### 👥 **Team Member Management**
- Add/remove team members with location information
- Support for multiple countries and regions/states
- Robust delete functionality with automatic OOO cleanup
- Data attribute-based UI interactions for improved reliability

### 🏖️ **Holiday Management**
- Automatic holiday generation using the Python `holidays` library
- Support for national and regional/state holidays
- Multi-country holiday support (AU, CN, US, and expandable)
- Manual holiday addition for custom company holidays

### 📝 **Out-of-Office (OOO) Tracking**
- Add OOO entries with date ranges and reasons
- View and cancel existing OOO entries

### 📊 **Activity History**
- Complete audit trail of all operations
- Timestamped logs for member additions/deletions

## How to Use

### Initial Setup

1. **Install Dependencies**
   ```bash
   # Activate virtual environment
   & .venv\Scripts\Activate.ps1
   
   # Install required packages
   pip install -r requirements.txt
   ```

2. **Initialize Data Files**
   ```bash
   cd src
   python init_sample_data.py
   ```

3. **Run the Application**
   ```bash
   python app.py
   ```

4. **Access the App**
   Open your browser to `http://localhost:5000`

### Adding Team Members

1. Navigate to the **Members** page
2. Click "Add Member" 
3. Fill in:
   - **Name**: Team member's full name
   - **Country**: Select from supported countries (Australia, China, United States)
   - **Region/State**: Automatically populated based on country selection
4. Click "Add Member"

### Removing Team Members

1. Navigate to the **Members** page
2. Locate the member in the Current Members table
3. Click the "×" button in the Actions column
4. Confirm deletion in the popup dialog
5. The member and all associated OOO entries will be removed automatically

**Supported Regions:**
- **Australia**: NSW, VIC, QLD, WA, SA, TAS, NT, ACT
- **United States**: All 50 states + DC, territories
- **China**: National holidays only

### Generating Holidays

After adding team members:

1. Go to the **Holidays** page
2. Click "Generate Holidays for Team"
3. The system automatically:
   - Generates holidays for current year + next year
   - Includes national holidays for all member countries
   - Includes regional holidays for member states/regions
   - Creates 500+ holiday entries covering all locations

### Managing Out-of-Office

#### Adding OOO from Calendar:
1. Go to the **Calendar** page
2. Click the "+" button on any date
3. Select:
   - **Team Member**
   - **End Date** (for multi-day periods)
   - **Reason** (Vacation, Sick Leave, Personal, etc.)
4. Click "Add OOO"

#### Viewing/Canceling OOO:
1. On the calendar, click the "✕" button next to an OOO entry
2. View details including:
   - Date range
   - Reason
   - Duration in days
3. Click "Cancel Entry" to remove the entire vacation period

### Understanding the Calendar

**Color Coding:**
- 🔴 **Red background**: Out-of-office (personal leave)
- 🔵 **Blue background**: Public holidays
- ⚪ **No highlight**: Available for work

**Information Displayed:**
- **Holiday entries**: Show holiday name and location
- **OOO entries**: Show reason and have management options
- **Interactive elements**: Plus button to add OOO, X button to manage existing entries

### Viewing Activity History

The **History** page provides a complete audit trail:
- Member additions and deletions
- Holiday generation activities
- OOO entries and cancellations
- Timestamped chronological order
- Detailed operation descriptions

### Adding Custom Holidays

For company-specific holidays:

1. Go to **Holidays** page
2. Scroll to "Add Custom Holiday"
3. Enter:
   - **Holiday Name**
   - **Date**
   - **Country**
   - **Region** (optional, for regional holidays)
4. Click "Add Holiday"

## Configuration

### Supported Countries

The app comes pre-configured with major economies, defined in `src/config/countries.json`:

```json
{
  "countries": {
    "AU": {"name": "Australia", "code": "AU"},
    "CN": {"name": "China", "code": "CN"},
    "US": {"name": "United States", "code": "US"}
  }
}
```

### Adding New Countries

1. Edit `src/config/countries.json`
2. Add new country with ISO code:
   ```json
   "CA": {"name": "Canada", "code": "CA"}
   ```
3. Restart the application
4. The holidays library will automatically support the new country

### Data Storage

All data is stored in JSON files under `src/data/`:
- `members.json`: Team member information
- `holidays.json`: Holiday data organized by country/region
- `ooo.json`: Out-of-office entries by member
- `history.json`: Activity audit trail

## Technical Features

### Recent Improvements (v1.1)

- **Enhanced Member Management**: Improved delete functionality with robust error handling
- **Better JavaScript Architecture**: Replaced inline event handlers with data attributes and proper event listeners
- **Automatic Cleanup**: Member deletion now automatically removes associated OOO entries
- **Improved User Experience**: Better error messages and confirmation dialogs
- **Enhanced Security**: More secure JavaScript implementation without inline event handlers

### Holiday Generation Engine
- Uses Python `holidays` library for accurate, up-to-date holiday data
- Supports 100+ countries and their subdivisions
- Automatically handles complex holiday rules and date calculations
- Generates holidays for current and next year
- No version pinning to ensure latest holiday updates

### Smart Region Detection
- Dynamically discovers available regions per country
- Handles different subdivision types (states, provinces, territories)
- Country-specific parameter mapping (e.g., 'prov' for Canada, 'state' for others)

### API Endpoints
- `/api/regions/<country>`: Get regions for a country
- `/api/member_locations`: Get unique countries/regions from members
- `/api/generate_holidays`: Bulk holiday generation
- `/api/availability/<date>`: Get team availability for specific date
- `/api/ooo_details/<member_id>/<date>`: Detailed OOO information

### Mobile Responsive
- Bootstrap 5 responsive framework
- Touch-friendly interface for mobile devices
- Optimized calendar view for small screens
- Collapsible navigation for mobile

## Deployment

### Local Development
```bash
cd src
python app.py
```

### Azure Deployment
See `AZURE_DEPLOYMENT.md` for complete Azure deployment instructions including:
- PowerShell and Bash deployment scripts
- Manual Azure CLI commands
- Troubleshooting guide
- Configuration options

### Docker (Future Enhancement)
The app structure supports containerization with proper requirements.txt and static file organization.

## Use Cases

### Small Teams (5-15 people)
- Track vacation periods
- Avoid scheduling conflicts
- Respect cultural holidays

### International Teams
- Multi-timezone holiday awareness
- Regional holiday compliance
- Cultural sensitivity planning

### Project Management
- Resource availability planning
- Meeting scheduling optimization
- Deadline planning around holidays

### HR Management
- Leave request visualization
- Holiday calendar maintenance
- Team coverage planning

## Best Practices

1. **Regular Holiday Updates**: Generate holidays at least annually
2. **Advance Planning**: Add OOO requests well in advance
3. **Team Communication**: Use the calendar as a team reference
4. **History Review**: Monitor usage patterns via history logs
5. **Data Backup**: Regularly backup the `data/` directory

## Future Enhancements

Potential features for expansion:
- Email notifications for OOO requests
- Team coverage recommendations
- Export to popular calendar formats
- Integration with HR systems
- Multi-year calendar views
- Approval workflows for OOO requests

## Troubleshooting

### Common Issues

**Empty Calendar**: Add team members first, then generate holidays

**Missing Holidays**: Click "Generate Holidays for Team" after adding members

**OOO Not Showing**: Ensure the date range is correct and member is selected

**Regional Holidays Missing**: Verify the member's region is correctly set

**Delete Member Not Working**: Ensure JavaScript is enabled; check browser console for errors. Recent improvements have resolved most delete functionality issues.

**Member Names with Special Characters**: The app now properly handles names with apostrophes, quotes, and special characters in the delete functionality.

### Getting Help

1. Check the **History** page for operation logs
2. Verify team members have correct location information
3. Ensure holidays have been generated for your team's locations
4. Check browser console for JavaScript errors

---

**Version**: 1.1  
**Last Updated**: August 2025  
**Technology Stack**: Flask, Python, Bootstrap 5, JavaScript  
**License**: MIT  
**Author**: Team Availability Management System

**Recent Updates**: 
- Fixed delete member functionality with improved JavaScript architecture
- Enhanced error handling and user experience
- Automatic cleanup of related data when deleting members
