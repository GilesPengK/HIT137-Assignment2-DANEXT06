# Question 2 - Temperature Analysis

import os
import csv
import math

# Folder where all temperature csv files are stored
DATA_FOLDER = "temperatures"

# Month names used in the csv files
MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# Australian seasons
SEASONS = {
    "Summer": ["December", "January", "February"],
    "Autumn": ["March", "April", "May"],
    "Winter": ["June", "July", "August"],
    "Spring": ["September", "October", "November"]
}


# Read all csv files and collect temperature data
def read_temperature_data():
    season_temperatures = {
        "Summer": [],
        "Autumn": [],
        "Winter": [],
        "Spring": []
    }

    station_temperatures = {}

    # Go through all files in temperatures folder
    for file_name in os.listdir(DATA_FOLDER):
        if file_name.endswith(".csv"):
            file_path = os.path.join(DATA_FOLDER, file_name)

            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)

                for row in reader:
                    station = row["STATION_NAME"]

                    # Create list for station if not exists
                    if station not in station_temperatures:
                        station_temperatures[station] = []

                    # Read each month temperature
                    for month in MONTHS:
                        value = row[month]

                        # Skip missing values
                        if value == "" or value == "NaN":
                            continue

                        temperature = float(value)

                        station_temperatures[station].append(temperature)

                        # Put temperature into correct season
                        for season in SEASONS:
                            if month in SEASONS[season]:
                                season_temperatures[season].append(temperature)

    return season_temperatures, station_temperatures


# Calculate average temperature for each season
def calculate_season_average(season_temperatures):
    with open("average_temp.txt", "w") as f:
        for season in season_temperatures:
            temps = season_temperatures[season]
            average = sum(temps) / len(temps)
            f.write(f"{season}: {average:.2f}°C\n")


# Find station(s) with the largest temperature range
def calculate_largest_range(station_temperatures):
    max_range = -1
    result = []

    for station in station_temperatures:
        temps = station_temperatures[station]
        temp_range = max(temps) - min(temps)

        if temp_range > max_range:
            max_range = temp_range
            result = [(station, max(temps), min(temps))]
        elif temp_range == max_range:
            result.append((station, max(temps), min(temps)))

    with open("largest_temp_range_station.txt", "w") as f:
        for station, t_max, t_min in result:
            f.write(
                f"Station {station}: Range {t_max - t_min:.2f}°C "
                f"(Max: {t_max:.2f}°C, Min: {t_min:.2f}°C)\n"
            )


# Calculate standard deviation (basic formula)
def standard_deviation(values):
    mean = sum(values) / len(values)
    total = 0

    for v in values:
        total += (v - mean) ** 2

    return math.sqrt(total / len(values))


# Find most stable and most variable stations
def calculate_temperature_stability(station_temperatures):
    min_std = float("inf")
    max_std = -1

    most_stable = []
    most_variable = []

    for station in station_temperatures:
        std = standard_deviation(station_temperatures[station])

        if std < min_std:
            min_std = std
            most_stable = [(station, std)]
        elif std == min_std:
            most_stable.append((station, std))

        if std > max_std:
            max_std = std
            most_variable = [(station, std)]
        elif std == max_std:
            most_variable.append((station, std))

    with open("temperature_stability_stations.txt", "w") as f:
        for s, std in most_stable:
            f.write(f"Most Stable: Station {s}: StdDev {std:.2f}°C\n")

        for s, std in most_variable:
            f.write(f"Most Variable: Station {s}: StdDev {std:.2f}°C\n")


# ===============================
# Main Program
# ===============================

season_data, station_data = read_temperature_data()

calculate_season_average(season_data)
calculate_largest_range(station_data)
calculate_temperature_stability(station_data)

print("Question 2 completed successfully.")
