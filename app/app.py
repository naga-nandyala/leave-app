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
HOLIDAYS_FILE = os.path.join(DATA_DIR, "holidays.json")
MEMBERS_FILE = os.path.join(DATA_DIR, "members.json")
OOO_FILE = os.path.join(DATA_DIR, "ooo.json")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Top 10 world economies plus Australia
TOP_10_ECONOMIES = {
    "US": "United States",
    "CN": "China",
    "JP": "Japan",
    "DE": "Germany",
    "IN": "India",
    "GB": "United Kingdom",
    "FR": "France",
    "IT": "Italy",
    "BR": "Brazil",
    "CA": "Canada",
    "AU": "Australia",
}

# Mapping from country names to country codes for holidays library
COUNTRY_CODE_MAP = {
    "United States": "US",
    "China": "CN",
    "Japan": "JP",
    "Germany": "DE",
    "India": "IN",
    "United Kingdom": "GB",
    "France": "FR",
    "Italy": "IT",
    "Brazil": "BR",
    "Canada": "CA",
    "Australia": "AU",  # Adding Australia as it's in the existing data
}

# State/Province mappings for major countries
REGIONS_MAP = {
    "United States": [
        "Alabama",
        "Alaska",
        "Arizona",
        "Arkansas",
        "California",
        "Colorado",
        "Connecticut",
        "Delaware",
        "Florida",
        "Georgia",
        "Hawaii",
        "Idaho",
        "Illinois",
        "Indiana",
        "Iowa",
        "Kansas",
        "Kentucky",
        "Louisiana",
        "Maine",
        "Maryland",
        "Massachusetts",
        "Michigan",
        "Minnesota",
        "Mississippi",
        "Missouri",
        "Montana",
        "Nebraska",
        "Nevada",
        "New Hampshire",
        "New Jersey",
        "New Mexico",
        "New York",
        "North Carolina",
        "North Dakota",
        "Ohio",
        "Oklahoma",
        "Oregon",
        "Pennsylvania",
        "Rhode Island",
        "South Carolina",
        "South Dakota",
        "Tennessee",
        "Texas",
        "Utah",
        "Vermont",
        "Virginia",
        "Washington",
        "West Virginia",
        "Wisconsin",
        "Wyoming",
    ],
    "Canada": [
        "Alberta",
        "British Columbia",
        "Manitoba",
        "New Brunswick",
        "Newfoundland and Labrador",
        "Northwest Territories",
        "Nova Scotia",
        "Nunavut",
        "Ontario",
        "Prince Edward Island",
        "Quebec",
        "Saskatchewan",
        "Yukon",
    ],
    "Australia": [
        "Australian Capital Territory",
        "New South Wales",
        "Northern Territory",
        "Queensland",
        "South Australia",
        "Tasmania",
        "Victoria",
        "Western Australia",
    ],
    "India": [
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
        "West Bengal",
    ],
    "Germany": [
        "Baden-Württemberg",
        "Bavaria",
        "Berlin",
        "Brandenburg",
        "Bremen",
        "Hamburg",
        "Hesse",
        "Lower Saxony",
        "Mecklenburg-Vorpommern",
        "North Rhine-Westphalia",
        "Rhineland-Palatinate",
        "Saarland",
        "Saxony",
        "Saxony-Anhalt",
        "Schleswig-Holstein",
        "Thuringia",
    ],
    "United Kingdom": ["England", "Scotland", "Wales", "Northern Ireland"],
    "China": [
        "Beijing",
        "Shanghai",
        "Tianjin",
        "Chongqing",
        "Guangdong",
        "Jiangsu",
        "Shandong",
        "Zhejiang",
        "Henan",
        "Sichuan",
        "Hubei",
        "Hunan",
        "Anhui",
        "Hebei",
        "Jiangxi",
        "Shanxi",
        "Liaoning",
        "Fujian",
        "Yunnan",
        "Guangxi",
        "Jilin",
        "Guizhou",
        "Gansu",
        "Inner Mongolia",
        "Shaanxi",
        "Heilongjiang",
        "Xinjiang",
        "Tibet",
        "Qinghai",
        "Hainan",
        "Ningxia",
    ],
    "Japan": [
        "Hokkaido",
        "Aomori",
        "Iwate",
        "Miyagi",
        "Akita",
        "Yamagata",
        "Fukushima",
        "Ibaraki",
        "Tochigi",
        "Gunma",
        "Saitama",
        "Chiba",
        "Tokyo",
        "Kanagawa",
        "Niigata",
        "Toyama",
        "Ishikawa",
        "Fukui",
        "Yamanashi",
        "Nagano",
        "Gifu",
        "Shizuoka",
        "Aichi",
        "Mie",
        "Shiga",
        "Kyoto",
        "Osaka",
        "Hyogo",
        "Nara",
        "Wakayama",
        "Tottori",
        "Shimane",
        "Okayama",
        "Hiroshima",
        "Yamaguchi",
        "Tokushima",
        "Kagawa",
        "Ehime",
        "Kochi",
        "Fukuoka",
        "Saga",
        "Nagasaki",
        "Kumamoto",
        "Oita",
        "Miyazaki",
        "Kagoshima",
        "Okinawa",
    ],
    "France": [
        "Auvergne-Rhône-Alpes",
        "Bourgogne-Franche-Comté",
        "Brittany",
        "Centre-Val de Loire",
        "Corsica",
        "Grand Est",
        "Hauts-de-France",
        "Île-de-France",
        "Normandy",
        "Nouvelle-Aquitaine",
        "Occitanie",
        "Pays de la Loire",
        "Provence-Alpes-Côte d'Azur",
    ],
    "Italy": [
        "Abruzzo",
        "Basilicata",
        "Calabria",
        "Campania",
        "Emilia-Romagna",
        "Friuli-Venezia Giulia",
        "Lazio",
        "Liguria",
        "Lombardy",
        "Marche",
        "Molise",
        "Piedmont",
        "Apulia",
        "Sardinia",
        "Sicily",
        "Tuscany",
        "Trentino-Alto Adige/Südtirol",
        "Umbria",
        "Aosta Valley",
        "Veneto",
    ],
    "Brazil": [
        "Acre",
        "Alagoas",
        "Amapá",
        "Amazonas",
        "Bahia",
        "Ceará",
        "Distrito Federal",
        "Espírito Santo",
        "Goiás",
        "Maranhão",
        "Mato Grosso",
        "Mato Grosso do Sul",
        "Minas Gerais",
        "Pará",
        "Paraíba",
        "Paraná",
        "Pernambuco",
        "Piauí",
        "Rio de Janeiro",
        "Rio Grande do Norte",
        "Rio Grande do Sul",
        "Rondônia",
        "Roraima",
        "Santa Catarina",
        "São Paulo",
        "Sergipe",
        "Tocantins",
    ],
}


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
    return render_template("holidays.html", holidays=holidays_data)


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
