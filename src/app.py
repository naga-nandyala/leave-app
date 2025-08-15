from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
import json
import os
import calendar
import holidays

app = Flask(__name__)
app.secret_key = "your-secret-key-change-this"

# Data storage (in production, use a proper database)
DATA_DIR = "data"
CONFIG_DIR = "config"
HOLIDAYS_FILE = os.path.join(DATA_DIR, "holidays.json")
MEMBERS_FILE = os.path.join(DATA_DIR, "members.json")
OOO_FILE = os.path.join(DATA_DIR, "ooo.json")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")
COUNTRIES_CONFIG_FILE = os.path.join(CONFIG_DIR, "countries.json")

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(CONFIG_DIR, exist_ok=True)


def load_countries_config():
    """Load countries configuration from JSON file"""
    try:
        with open(COUNTRIES_CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
            return config["countries"]
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        print(f"Error loading countries config: {e}")
        # Return default config if file is missing or corrupted
        return {
            "AU": {"name": "Australia", "code": "AU"},
            "CN": {"name": "China", "code": "CN"},
            "US": {"name": "United States", "code": "US"},
        }


def get_supported_regions(country_code):
    """Get supported regions/states for a country from the holidays library"""
    try:
        # Get country holidays object
        country_holidays = holidays.country_holidays(country_code)

        # Check if the country has subdivisions/states
        if hasattr(country_holidays, "subdivisions") and country_holidays.subdivisions:
            # Check if there are subdivision aliases (full names)
            if hasattr(country_holidays, "subdivisions_aliases") and country_holidays.subdivisions_aliases:
                aliases = country_holidays.subdivisions_aliases
                # Return list of full names (keys from aliases dict), sorted
                return sorted(list(aliases.keys()))
            else:
                # Return subdivision codes if no aliases available, sorted
                return sorted(list(country_holidays.subdivisions))
        else:
            return []
    except Exception as e:
        print(f"Could not get regions for {country_code}: {e}")
        return []


def generate_regions_map():
    """Generate regions map dynamically from holidays library"""
    regions_map = {}

    for country_data in COUNTRIES_CONFIG.values():
        country_name = country_data["name"]
        country_code = country_data["code"]

        # Get regions from holidays library
        regions = get_supported_regions(country_code)

        regions_map[country_name] = sorted(regions)

    return regions_map


# Load countries configuration
COUNTRIES_CONFIG = load_countries_config()

# Create backwards compatible dictionaries
TOP_10_ECONOMIES = {code: country_data["name"] for code, country_data in COUNTRIES_CONFIG.items()}
COUNTRY_CODE_MAP = {country_data["name"]: country_data["code"] for country_data in COUNTRIES_CONFIG.values()}

# Generate regions map dynamically from holidays library
REGIONS_MAP = generate_regions_map()


def populate_holidays_for_country(country, region=None, year=2025):
    """Populate holidays for a given country and region using the holidays library"""
    holidays_data = get_holidays()

    # Initialize structure if needed
    if "national" not in holidays_data:
        holidays_data["national"] = {}
    if "regional" not in holidays_data:
        holidays_data["regional"] = {}

    # Get country code for holidays library
    country_code = COUNTRY_CODE_MAP.get(country)
    if not country_code:
        return holidays_data

    try:
        # Get national holidays
        if country not in holidays_data["national"]:
            holidays_data["national"][country] = {}

        country_holidays = holidays.country_holidays(country_code, years=year)
        for date, name in country_holidays.items():
            date_str = date.strftime("%Y-%m-%d")
            holidays_data["national"][country][date_str] = name

        # Get regional holidays if region is provided and supported
        if region:
            if country not in holidays_data["regional"]:
                holidays_data["regional"][country] = {}
            if region not in holidays_data["regional"][country]:
                holidays_data["regional"][country][region] = {}

            # Try to get state/province specific holidays
            try:
                # For some countries, the holidays library supports state/province codes
                if country_code == "US":
                    # Map full state names to abbreviations for US states
                    state_abbrev_map = {
                        "Alabama": "AL",
                        "Alaska": "AK",
                        "Arizona": "AZ",
                        "Arkansas": "AR",
                        "California": "CA",
                        "Colorado": "CO",
                        "Connecticut": "CT",
                        "Delaware": "DE",
                        "Florida": "FL",
                        "Georgia": "GA",
                        "Hawaii": "HI",
                        "Idaho": "ID",
                        "Illinois": "IL",
                        "Indiana": "IN",
                        "Iowa": "IA",
                        "Kansas": "KS",
                        "Kentucky": "KY",
                        "Louisiana": "LA",
                        "Maine": "ME",
                        "Maryland": "MD",
                        "Massachusetts": "MA",
                        "Michigan": "MI",
                        "Minnesota": "MN",
                        "Mississippi": "MS",
                        "Missouri": "MO",
                        "Montana": "MT",
                        "Nebraska": "NE",
                        "Nevada": "NV",
                        "New Hampshire": "NH",
                        "New Jersey": "NJ",
                        "New Mexico": "NM",
                        "New York": "NY",
                        "North Carolina": "NC",
                        "North Dakota": "ND",
                        "Ohio": "OH",
                        "Oklahoma": "OK",
                        "Oregon": "OR",
                        "Pennsylvania": "PA",
                        "Rhode Island": "RI",
                        "South Carolina": "SC",
                        "South Dakota": "SD",
                        "Tennessee": "TN",
                        "Texas": "TX",
                        "Utah": "UT",
                        "Vermont": "VT",
                        "Virginia": "VA",
                        "Washington": "WA",
                        "West Virginia": "WV",
                        "Wisconsin": "WI",
                        "Wyoming": "WY",
                    }
                    state_code = state_abbrev_map.get(region)
                    if state_code:
                        regional_holidays = holidays.country_holidays(country_code, state=state_code, years=year)
                        for date, name in regional_holidays.items():
                            date_str = date.strftime("%Y-%m-%d")
                            # Only add if it's not already a national holiday
                            if date_str not in holidays_data["national"][country]:
                                holidays_data["regional"][country][region][date_str] = name

                elif country_code == "AU":
                    # Map full state names to abbreviations for Australian states
                    state_abbrev_map = {
                        "Australian Capital Territory": "ACT",
                        "New South Wales": "NSW",
                        "Northern Territory": "NT",
                        "Queensland": "QLD",
                        "South Australia": "SA",
                        "Tasmania": "TAS",
                        "Victoria": "VIC",
                        "Western Australia": "WA",
                    }
                    state_code = state_abbrev_map.get(region)
                    if state_code:
                        regional_holidays = holidays.country_holidays(country_code, state=state_code, years=year)
                        for date, name in regional_holidays.items():
                            date_str = date.strftime("%Y-%m-%d")
                            # Only add if it's not already a national holiday
                            if date_str not in holidays_data["national"][country]:
                                holidays_data["regional"][country][region][date_str] = name

                elif country_code == "CA":
                    # Map full province names to abbreviations for Canadian provinces
                    province_abbrev_map = {
                        "Alberta": "AB",
                        "British Columbia": "BC",
                        "Manitoba": "MB",
                        "New Brunswick": "NB",
                        "Newfoundland and Labrador": "NL",
                        "Northwest Territories": "NT",
                        "Nova Scotia": "NS",
                        "Nunavut": "NU",
                        "Ontario": "ON",
                        "Prince Edward Island": "PE",
                        "Quebec": "QC",
                        "Saskatchewan": "SK",
                        "Yukon": "YT",
                    }
                    province_code = province_abbrev_map.get(region)
                    if province_code:
                        regional_holidays = holidays.country_holidays(country_code, prov=province_code, years=year)
                        for date, name in regional_holidays.items():
                            date_str = date.strftime("%Y-%m-%d")
                            # Only add if it's not already a national holiday
                            if date_str not in holidays_data["national"][country]:
                                holidays_data["regional"][country][region][date_str] = name

            except Exception as e:
                print(f"Could not get regional holidays for {region}, {country}: {e}")

    except Exception as e:
        print(f"Could not get holidays for {country}: {e}")

    return holidays_data


def load_data(filename, default=None):
    """Load data from JSON file"""
    if default is None:
        default = {}
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return default


def save_data(filename, data):
    """Save data to JSON file"""
    with open(filename, "w") as f:
        json.dump(data, f, indent=2, default=str)


def get_holidays():
    """Get all holidays"""
    return load_data(HOLIDAYS_FILE, {})


def get_members():
    """Get all team members"""
    return load_data(MEMBERS_FILE, {})


def get_ooo():
    """Get all out of office entries"""
    return load_data(OOO_FILE, {})


def get_history():
    """Get all history entries"""
    return load_data(HISTORY_FILE, [])


def save_holidays(holidays_data):
    """Save holidays data"""
    save_data(HOLIDAYS_FILE, holidays_data)


def save_members(members):
    """Save members data"""
    save_data(MEMBERS_FILE, members)


def save_ooo(ooo):
    """Save OOO data"""
    save_data(OOO_FILE, ooo)


def save_history(history):
    """Save history data"""
    save_data(HISTORY_FILE, history)


def get_sorted_holidays():
    """Get holidays sorted by year, then national/regional, then country, then date"""
    holidays_data = get_holidays()
    sorted_holidays = []

    # Process national holidays
    if "national" in holidays_data:
        for country, country_holidays in holidays_data["national"].items():
            for date_str, name in country_holidays.items():
                sorted_holidays.append(
                    {
                        "type": "national",
                        "country": country,
                        "region": None,
                        "date": date_str,
                        "name": name,
                        "year": int(date_str.split("-")[0]),
                    }
                )

    # Process regional holidays
    if "regional" in holidays_data:
        for country, regions in holidays_data["regional"].items():
            for region, region_holidays in regions.items():
                for date_str, name in region_holidays.items():
                    sorted_holidays.append(
                        {
                            "type": "regional",
                            "country": country,
                            "region": region,
                            "date": date_str,
                            "name": name,
                            "year": int(date_str.split("-")[0]),
                        }
                    )

    # Sort by: year (ascending), type (national first), country (ascending), date (ascending)
    sorted_holidays.sort(key=lambda x: (x["year"], x["type"], x["country"], x["date"]))

    return sorted_holidays


def log_operation(operation_type, member_id, details, member_name=None):
    """Log an operation to the history"""
    history = get_history()

    # Get member name if not provided
    if not member_name and member_id:
        members = get_members()
        member_name = members.get(member_id, {}).get("name", "Unknown")

    history_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "operation_type": operation_type,
        "member_id": member_id,
        "member_name": member_name,
        "details": details,
    }

    history.append(history_entry)
    save_history(history)


def is_holiday(date_str, country, region=None):
    """Check if a date is a holiday for given country/region"""
    holidays_data = get_holidays()

    # Check national holidays
    if country in holidays_data.get("national", {}):
        if date_str in holidays_data["national"][country]:
            return True

    # Check regional holidays
    if region and country in holidays_data.get("regional", {}):
        if region in holidays_data["regional"][country]:
            if date_str in holidays_data["regional"][country][region]:
                return True

    return False


def get_holiday_name(date_str, country, region=None):
    """Get the name of the holiday for a given date and location"""
    holidays_data = get_holidays()

    # Check regional holidays first (more specific)
    if region and country in holidays_data.get("regional", {}):
        if region in holidays_data["regional"][country]:
            if date_str in holidays_data["regional"][country][region]:
                return holidays_data["regional"][country][region][date_str]

    # Check national holidays
    if country in holidays_data.get("national", {}):
        if date_str in holidays_data["national"][country]:
            return holidays_data["national"][country][date_str]

    return None


def is_member_ooo(member_id, date_str):
    """Check if a member is out of office on a given date"""
    ooo_data = get_ooo()

    if member_id in ooo_data:
        for ooo_entry in ooo_data[member_id]:
            start_date = datetime.strptime(ooo_entry["start_date"], "%Y-%m-%d").date()
            end_date = datetime.strptime(ooo_entry["end_date"], "%Y-%m-%d").date()
            check_date = datetime.strptime(date_str, "%Y-%m-%d").date()

            if start_date <= check_date <= end_date:
                return True

    return False


@app.route("/")
def index():
    """Main calendar view"""
    # Get current month or requested month
    year = request.args.get("year", datetime.now().year, type=int)
    month = request.args.get("month", datetime.now().month, type=int)

    # Get calendar data
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]

    # Get members and their availability
    members = get_members()
    availability = {}

    # Calculate availability for each day of the month
    for week in cal:
        for day in week:
            if day == 0:  # Empty day
                continue

            date_str = f"{year}-{month:02d}-{day:02d}"
            availability[date_str] = {}

            for member_id, member_info in members.items():
                country = member_info["country"]
                region = member_info.get("region")

                # Check if member is available
                is_available = True
                reason = None

                # Check holidays
                if is_holiday(date_str, country, region):
                    is_available = False
                    holiday_name = get_holiday_name(date_str, country, region)
                    reason = f"Holiday: {holiday_name}"

                # Check OOO
                elif is_member_ooo(member_id, date_str):
                    is_available = False
                    # Get specific OOO reason
                    ooo_data = get_ooo()
                    reason = "OOO"  # default
                    if member_id in ooo_data:
                        for ooo_entry in ooo_data[member_id]:
                            start_date = datetime.strptime(ooo_entry["start_date"], "%Y-%m-%d").date()
                            end_date = datetime.strptime(ooo_entry["end_date"], "%Y-%m-%d").date()
                            check_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                            if start_date <= check_date <= end_date:
                                reason = f"OOO: {ooo_entry['reason']}"
                                break

                availability[date_str][member_id] = {"available": is_available, "reason": reason}

    return render_template(
        "calendar.html",
        calendar_data=cal,
        year=year,
        month=month,
        month_name=month_name,
        members=members,
        availability=availability,
    )


@app.route("/members")
def members():
    """Manage team members"""
    members_data = get_members()
    return render_template(
        "members.html", members=members_data, top_economies=TOP_10_ECONOMIES, regions_map=REGIONS_MAP
    )


@app.route("/api/regions/<country>")
def get_regions(country):
    """Get regions/states for a specific country"""
    regions = REGIONS_MAP.get(country, [])
    return jsonify(regions)


@app.route("/api/member_locations")
def get_member_locations():
    """Get unique countries and regions from member data"""
    try:
        members_data = get_members()

        countries = set()
        regions = []

        for member_id, member in members_data.items():
            country = member.get("country")
            region = member.get("region")

            if country:
                countries.add(country)
                if region:  # Only add regions that are not empty
                    regions.append(f"{region} ({country})")

        return jsonify({"countries": sorted(list(countries)), "regions": sorted(regions)})

    except Exception as e:
        print(f"Error getting member locations: {e}")
        return jsonify({"error": "Failed to get member locations"}), 500


@app.route("/api/generate_holidays", methods=["POST"])
def generate_holidays_api():
    """Generate holidays for all countries and regions in the member list for the next 2 years"""
    try:
        from datetime import datetime

        # Always generate for current year and next year
        current_year = datetime.now().year
        years = [current_year, current_year + 1]

        # Get all members to extract countries and regions
        members_data = get_members()

        if not members_data:
            return jsonify({"error": "No members found. Add team members first."}), 400

        # Extract unique countries and regions from member data
        countries_in_use = set()
        regions_in_use = []

        for member_id, member in members_data.items():
            country = member.get("country")
            region = member.get("region")

            if country:
                countries_in_use.add(country)
                if region:  # Only add regions that are not empty
                    regions_in_use.append({"country": country, "region": region})

        if not countries_in_use:
            return jsonify({"error": "No countries found in member data"}), 400

        # Clear all existing holidays and start fresh
        holidays_data = {"national": {}, "regional": {}}

        holiday_count = 0

        # Generate national holidays for each country used by members for all years
        for country in countries_in_use:
            country_code = COUNTRY_CODE_MAP.get(country)
            if not country_code:
                continue

            holidays_data["national"][country] = {}

            for year in years:
                try:
                    # Get holidays for the country for this year
                    country_holidays = holidays.country_holidays(country_code, years=year)

                    # Add holidays to our data
                    for date, name in country_holidays.items():
                        date_str = date.strftime("%Y-%m-%d")
                        holidays_data["national"][country][date_str] = name
                        holiday_count += 1

                except Exception as e:
                    print(f"Error generating holidays for {country} in {year}: {e}")

        # Generate regional holidays for regions used by members for all years
        for region_data in regions_in_use:
            region = region_data.get("region")
            country = region_data.get("country")
            country_code = COUNTRY_CODE_MAP.get(country)

            if not country_code or not region:
                continue

            if country not in holidays_data["regional"]:
                holidays_data["regional"][country] = {}
            holidays_data["regional"][country][region] = {}

            for year in years:
                try:
                    # Get holidays for the region for this year
                    region_holidays = holidays.country_holidays(country_code, state=region, years=year)

                    # Add regional holidays to our data
                    for date, name in region_holidays.items():
                        date_str = date.strftime("%Y-%m-%d")
                        # Only add if it's not already in national holidays
                        if date_str not in holidays_data["national"].get(country, {}):
                            holidays_data["regional"][country][region][date_str] = name
                            holiday_count += 1

                except Exception as e:
                    print(f"Error generating holidays for {region}, {country} in {year}: {e}")

        # Save the updated holidays
        save_holidays(holidays_data)

        # Log the operation
        countries_list = list(countries_in_use)
        regions_list = [f"{r['region']} ({r['country']})" for r in regions_in_use]
        log_operation(
            "GENERATE_HOLIDAYS",
            None,  # No specific member_id for this system operation
            f"Generated {holiday_count} holidays for {len(years)} years ({', '.join(map(str, years))}) - Countries: {', '.join(countries_list)} and regions: {', '.join(regions_list)}",
            "System",
        )

        return jsonify(
            {
                "success": True,
                "count": holiday_count,
                "years": years,
                "countries": countries_list,
                "regions": regions_list,
                "message": f"Generated {holiday_count} holidays for {len(years)} years ({', '.join(map(str, years))}) covering {len(countries_list)} countries and {len(regions_list)} regions",
            }
        )

    except Exception as e:
        print(f"Error in generate_holidays_api: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/add_member", methods=["POST"])
def add_member():
    """Add a new team member"""
    name = request.form["name"]
    country = request.form["country"]
    region = request.form.get("region", "")

    members_data = get_members()
    member_id = str(len(members_data) + 1)

    members_data[member_id] = {"name": name, "country": country, "region": region}

    save_members(members_data)

    # Populate holidays for the new member's country and region
    holidays_data = populate_holidays_for_country(country, region)
    save_holidays(holidays_data)

    # Log the operation
    log_operation("ADD_MEMBER", member_id, f"Added member: {name} from {country}, {region}", name)

    flash(
        f"Member added successfully! Holidays for {country}"
        + (f", {region}" if region else "")
        + " have been populated.",
        "success",
    )
    return redirect(url_for("members"))


@app.route("/holidays")
def holidays_page():
    """Manage holidays"""
    holidays_data = get_holidays()
    # Sort countries alphabetically for display
    sorted_countries = sorted(COUNTRIES_CONFIG.values(), key=lambda x: x["name"])
    return render_template("holidays.html", holidays=holidays_data, countries=sorted_countries)


@app.route("/history")
def history():
    """View operation history"""
    history_data = get_history()
    # Sort by timestamp (newest first)
    history_data.sort(key=lambda x: x["timestamp"], reverse=True)
    return render_template("history.html", history=history_data)


@app.route("/add_holiday", methods=["POST"])
def add_holiday():
    """Add a new holiday"""
    name = request.form["name"]
    date_str = request.form["date"]
    country = request.form["country"]
    region = request.form.get("region", "")
    holiday_type = "regional" if region else "national"

    holidays_data = get_holidays()

    # Initialize structure if needed
    if holiday_type not in holidays_data:
        holidays_data[holiday_type] = {}

    if country not in holidays_data[holiday_type]:
        holidays_data[holiday_type][country] = {}

    if holiday_type == "regional":
        if region not in holidays_data[holiday_type][country]:
            holidays_data[holiday_type][country][region] = {}
        holidays_data[holiday_type][country][region][date_str] = name
    else:
        holidays_data[holiday_type][country][date_str] = name

    save_holidays(holidays_data)

    # Log the operation
    location = f"{country}, {region}" if region else country
    log_operation("ADD_HOLIDAY", None, f"Added holiday: {name} on {date_str} for {location}", "System")

    flash("Holiday added successfully!", "success")
    return redirect(url_for("holidays_page"))


@app.route("/add_ooo", methods=["POST"])
def add_ooo():
    """Add a new out of office entry"""
    member_id = request.form["member_id"]
    start_date = request.form["start_date"]
    end_date = request.form["end_date"]
    reason = request.form.get("reason", "Vacation")

    ooo_data = get_ooo()

    if member_id not in ooo_data:
        ooo_data[member_id] = []

    ooo_data[member_id].append({"start_date": start_date, "end_date": end_date, "reason": reason})

    save_ooo(ooo_data)

    # Log the operation
    members = get_members()
    member_name = members.get(member_id, {}).get("name", "Unknown")
    if start_date == end_date:
        details = f"Added OOO ({reason}) for {start_date}"
    else:
        details = f"Added OOO ({reason}) from {start_date} to {end_date}"
    log_operation("ADD_OOO", member_id, details, member_name)

    # Always return JSON response for AJAX calls from calendar
    return jsonify({"success": True, "message": "Out of office entry added successfully!"})


@app.route("/delete_ooo", methods=["POST"])
def delete_ooo():
    """Delete an out of office entry"""
    data = request.get_json()
    member_id = data["member_id"]
    target_date = data["date"]

    ooo_data = get_ooo()
    deleted_entry = None

    if member_id in ooo_data:
        # Find and remove the OOO entry that contains the target date
        from datetime import datetime

        target_date_obj = datetime.strptime(target_date, "%Y-%m-%d").date()

        for i, entry in enumerate(ooo_data[member_id]):
            start_date = datetime.strptime(entry["start_date"], "%Y-%m-%d").date()
            end_date = datetime.strptime(entry["end_date"], "%Y-%m-%d").date()

            if start_date <= target_date_obj <= end_date:
                deleted_entry = ooo_data[member_id][i]
                del ooo_data[member_id][i]
                break

        # Remove member entirely if no more OOO entries
        if not ooo_data[member_id]:
            del ooo_data[member_id]

    save_ooo(ooo_data)

    # Log the operation
    if deleted_entry:
        members = get_members()
        member_name = members.get(member_id, {}).get("name", "Unknown")
        log_operation(
            "DELETE_OOO", member_id, f"Deleted OOO entry for {target_date} (was {deleted_entry['reason']})", member_name
        )

    return jsonify({"success": True, "message": "Out of office entry deleted successfully!"})


@app.route("/api/ooo_details/<member_id>/<date>")
def get_ooo_details(member_id, date):
    """Get detailed OOO information for a specific member and date"""
    from datetime import datetime

    ooo_data = get_ooo()
    members_data = get_members()

    if member_id not in ooo_data:
        return jsonify({"success": False, "error": "No OOO data found for this member"})

    target_date_obj = datetime.strptime(date, "%Y-%m-%d").date()

    for entry in ooo_data[member_id]:
        start_date = datetime.strptime(entry["start_date"], "%Y-%m-%d").date()
        end_date = datetime.strptime(entry["end_date"], "%Y-%m-%d").date()

        if start_date <= target_date_obj <= end_date:
            duration = (end_date - start_date).days + 1
            return jsonify(
                {
                    "success": True,
                    "entry": entry,
                    "member_name": members_data.get(member_id, {}).get("name", "Unknown"),
                    "duration": duration,
                }
            )

    return jsonify({"success": False, "error": "No OOO entry found for this date"})


@app.route("/cancel_vacation", methods=["POST"])
def cancel_vacation():
    """Cancel an entire vacation/OOO period"""
    from datetime import datetime

    data = request.get_json()
    member_id = data["member_id"]
    start_date_str = data["start_date"]
    end_date_str = data["end_date"]

    ooo_data = get_ooo()
    canceled_entry = None

    if member_id in ooo_data:
        start_date_obj = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date_obj = datetime.strptime(end_date_str, "%Y-%m-%d").date()

        # Find and remove the matching vacation entry
        for i, entry in enumerate(ooo_data[member_id]):
            entry_start = datetime.strptime(entry["start_date"], "%Y-%m-%d").date()
            entry_end = datetime.strptime(entry["end_date"], "%Y-%m-%d").date()

            if entry_start == start_date_obj and entry_end == end_date_obj:
                canceled_entry = ooo_data[member_id][i]
                del ooo_data[member_id][i]
                break

        # Remove member entirely if no more OOO entries
        if not ooo_data[member_id]:
            del ooo_data[member_id]

    save_ooo(ooo_data)

    # Log the operation
    if canceled_entry:
        members = get_members()
        member_name = members.get(member_id, {}).get("name", "Unknown")
        if start_date_str == end_date_str:
            details = f"Canceled vacation ({canceled_entry['reason']}) for {start_date_str}"
        else:
            details = f"Canceled vacation ({canceled_entry['reason']}) from {start_date_str} to {end_date_str}"
        log_operation("CANCEL_VACATION", member_id, details, member_name)

    return jsonify({"success": True, "message": "Vacation canceled successfully!"})


@app.route("/api/availability/<date>")
def api_availability(date):
    """API endpoint to get availability for a specific date"""
    members = get_members()
    result = {}

    for member_id, member_info in members.items():
        country = member_info["country"]
        region = member_info.get("region")

        is_available = True
        reason = None

        if is_holiday(date, country, region):
            is_available = False
            reason = "Holiday"
        elif is_member_ooo(member_id, date):
            is_available = False
            reason = "OOO"

        result[member_id] = {"name": member_info["name"], "available": is_available, "reason": reason}

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
