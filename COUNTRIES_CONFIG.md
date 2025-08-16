# Countries Configuration Guide

## How to Add New Countries

The application now uses a configuration file to manage countries instead of hardcoded values in the source code.

### Configuration File Location
`src/config/countries.json`

### Adding a New Country

1. Open `src/config/countries.json`
2. Add a new country entry following this format:

```json
{
    "countries": {
        "COUNTRY_CODE": {
            "name": "Country Name",
            "code": "COUNTRY_CODE", 
            "regions": [
                "Region 1",
                "Region 2",
                "Region 3"
            ]
        }
    }
}
```

### Example: Adding India

```json
{
    "countries": {
        "AU": {
            "name": "Australia",
            "code": "AU",
            "regions": ["Australian Capital Territory", "New South Wales", ...]
        },
        "CN": {
            "name": "China", 
            "code": "CN",
            "regions": ["Beijing", "Shanghai", ...]
        },
        "US": {
            "name": "United States",
            "code": "US", 
            "regions": ["Alabama", "Alaska", ...]
        },
        "IN": {
            "name": "India",
            "code": "IN",
            "regions": [
                "Andhra Pradesh",
                "Arunachal Pradesh", 
                "Assam",
                "Bihar",
                "Chhattisgarh",
                "Goa",
                "Gujarat",
                "Haryana",
                "Himachal Pradesh",
                "Jharkhand",
                "Karnataka",
                "Kerala",
                "Madhya Pradesh",
                "Maharashtra",
                "Manipur",
                "Meghalaya",
                "Mizoram",
                "Nagaland",
                "Odisha",
                "Punjab",
                "Rajasthan",
                "Sikkim",
                "Tamil Nadu",
                "Telangana",
                "Tripura",
                "Uttar Pradesh",
                "Uttarakhand",
                "West Bengal"
            ]
        }
    }
}
```

### Important Notes

1. **Country Code**: Use the standard 2-letter ISO country codes (e.g., "US", "AU", "CN", "IN")
2. **Regions**: Include all states, provinces, or territories for that country
3. **Holidays Library**: Make sure the country code is supported by the Python `holidays` library
4. **Restart Required**: After adding new countries, restart the Flask application
5. **Backup**: Always backup the configuration file before making changes

### Supported Country Codes for Holidays

The application uses the Python `holidays` library. Some commonly supported country codes:
- US (United States)
- CA (Canada) 
- AU (Australia)
- CN (China)
- IN (India)
- GB (United Kingdom)
- DE (Germany)
- FR (France)
- JP (Japan)
- BR (Brazil)

For a complete list, check the [holidays library documentation](https://python-holidays.readthedocs.io/).

### Fallback Behavior

If the configuration file is missing or corrupted, the application will fall back to a default configuration with:
- Australia
- China  
- United States

This ensures the application continues to work even if there are configuration issues.
