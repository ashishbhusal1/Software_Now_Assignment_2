import os
import pandas as pd
import glob
import numpy as np
from pathlib import Path


def get_australian_season(month):
    """
    Determining the Australian season based on the given month using the function.
    Summer:-- Dec-Feb, Autumn:-- Mar-May, Winter:-- Jun-Aug, Spring:-- Sep-Nov
    """
    # Check if the month is corresponds to Summer
    if month in [12, 1, 2]:
        return "Summer"
    # Check if the month is corresponds to Autumn
    elif month in [3, 4, 5]:
        return "Autumn"
    # Check if the month is corresponds to Winter
    elif month in [6, 7, 8]:
        return "Winter"
    # Check if the month is corresponds to Spring
    elif month in [9, 10, 11]:
        return "Spring"
    else:
        # Invalid month input, if the month number is wrong
        return "Unknown"


def analyze_temperature_data():
    """
    This is the main function to analyze the temperature data going through all the CSV files given in the temperatures folder.
    Save and print results after collecting all the data from all stations and  calculating its seasonal average, temperature ranges, and temperature stability.

    """

    # Temperature folder path is defined
    temperatures_folder = "Question2/temperatures"

    # Checking if the temperatures folder defined above exists
    if not os.path.exists(temperatures_folder):
        print(f"Error: '{temperatures_folder}' folder is not found")
        return

    # Fetching all CSV files in the temperatures folder
    csv_files = glob.glob(os.path.join(temperatures_folder, "*.csv"))

    # If no CSV files in the folder, print the message below and stop the function there
    if not csv_files:
        print(f"No CSV files is found in '{temperatures_folder}' folder")
        return

    print(f"Found {len(csv_files)} CSV files to process...")

    # Here, I have created a dictionary to keep all the temperature data structured by season
    seasonal_temps = {"Summer": [], "Autumn": [], "Winter": [], "Spring": []}

    # Dictionary is used to keep temperature data for each station for the range and stability analysis
    station_temps = {}

    # Lets go through all the CSV file in the folder
    for csv_file in csv_files:
        try:
            print(f"Processing: {os.path.basename(csv_file)}")

            # Data is been read from the CSV file
            df = pd.read_csv(csv_file)

            # Get month columns (January through December), so we can loop through them
            month_columns = [
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December",
            ]

            # Processing each station's data , which represents a weather station
            for _, row in df.iterrows():
                station_name = row["STATION_NAME"]

                # Initializing station data if not exists
                if station_name not in station_temps:
                    station_temps[station_name] = []

                # Processing the temperature of each month's and get the temperature
                for i, month in enumerate(month_columns, 1):
                    temp = row[month]

                    # Skip if there is no temperature data for this month
                    if pd.isna(temp):
                        continue

                    # Identifying that which season does this month belongs to
                    season = get_australian_season(i)

                    # Adding the temperature to the appropriate season
                    if season in seasonal_temps:
                        seasonal_temps[season].append(temp)

                    # Store the temperature to the station for the later analysis
                    station_temps[station_name].append(temp)

        except Exception as e:
            # Print an error, if something goes wrong with this file and continue with the next file
            print(f"Error processing {csv_file}: {e}")
            continue

    # Calculating the seasonal averages for each season
    seasonal_averages = {}
    for season, temps in seasonal_temps.items():
        if temps:
            avg_temp = sum(temps) / len(temps)
            seasonal_averages[season] = round(avg_temp, 1)
            print(f"{season}: {len(temps)} temperature readings")
        else:
            seasonal_averages[season] = 0
            print(f"{season}: No temperature readings")

    # Analyze the temperature ranges for each station
    temperature_ranges = analyze_temperature_ranges(station_temps)

    # Identify station with extreme ranges (highest and lowest)
    extreme_ranges = get_extreme_ranges(temperature_ranges)

    # Temperature stability analyze at each station
    temperature_stability = analyze_temperature_stability(station_temps)

    # Save all the results to files
    save_results(seasonal_averages, temperature_ranges, temperature_stability)

    # Display seasonal average results nicely
    print("\n" + "=" * 50)
    print("SEASONAL AVERAGE TEMPERATURES")
    print("=" * 50)
    for season, avg_temp in seasonal_averages.items():
        if avg_temp > 0:
            print(f"{season}: {avg_temp}°C")
        else:
            print(f"{season}: No data available")

    # Print temperature range analysis
    print("\n" + "=" * 50)
    print("TEMPERATURE RANGE ANALYSIS")
    print("=" * 50)

    # Debug: Show the actual ranges found
    if extreme_ranges["highest"]:
        highest_range_value = extreme_ranges["highest"][0][1]["range"]
        print(f"Highest Temperature Range: {highest_range_value}°C")
        print("Stations with this range:")
        for station, data in extreme_ranges["highest"]:
            print(
                f"  {station}: Range {data['range']}°C (Max: {data['max']}°C, Min: {data['min']}°C)"
            )

    if extreme_ranges["lowest"]:
        lowest_range_value = extreme_ranges["lowest"][0][1]["range"]
        print(f"\nLowest Temperature Range: {lowest_range_value}°C")
        print("Stations with this range:")
        for station, data in extreme_ranges["lowest"]:
            print(
                f"  {station}: Range {data['range']}°C (Max: {data['max']}°C, Min: {data['min']}°C)"
            )

    # Print temperature stability analysis
    print("\n" + "=" * 50)
    print("TEMPERATURE STABILITY ANALYSIS")
    print("=" * 50)
    print("Most Stable:")
    for station, stddev in temperature_stability["most_stable"]:
        print(f"  {station}: StdDev {stddev}°C")
    print("Most Variable:")
    for station, stddev in temperature_stability["most_variable"]:
        print(f"  {station}: StdDev {stddev}°C")


# Function to calculate temperature range for each station
def analyze_temperature_ranges(station_temps):
    """
    Analyze temperature ranges for each station.
    Returns a dictionary with station names and their temperature range data.
    """
    station_ranges = {}

    for station_name, temps in station_temps.items():
        if temps:
            max_temp = max(temps)
            min_temp = min(temps)
            temp_range = round(max_temp - min_temp, 1)

            station_ranges[station_name] = {
                "max": round(max_temp, 1),
                "min": round(min_temp, 1),
                "range": temp_range,
            }

    return station_ranges


# Function to find stations with extreme temperature ranges
def get_extreme_ranges(temperature_ranges):
    """
    Find the stations with the highest and lowest temperature ranges.
    Returns a dictionary with highest and lowest range stations.
    """
    if not temperature_ranges:
        return {"highest": [], "lowest": []}

    # Sort stations by temperature range
    sorted_ranges = sorted(temperature_ranges.items(), key=lambda x: x[1]["range"])

    # Get the minimum and maximum ranges
    min_range = sorted_ranges[0][1]["range"]
    max_range = sorted_ranges[-1][1]["range"]

    # Find all stations with the same minimum and maximum ranges
    lowest_range_stations = [
        (station, data) for station, data in sorted_ranges if data["range"] == min_range
    ]
    highest_range_stations = [
        (station, data) for station, data in sorted_ranges if data["range"] == max_range
    ]

    return {"highest": highest_range_stations, "lowest": lowest_range_stations}


def analyze_temperature_stability(station_temps):
    """
    Analyze temperature stability (standard deviation) for each station.
    Returns a dictionary with most stable and most variable stations.
    """
    station_stability = {}

    # Calculate standard deviation for each station
    for station_name, temps in station_temps.items():
        if len(temps) > 1:  # Need at least 2 values for std dev
            stddev = np.std(temps)
            station_stability[station_name] = round(stddev, 1)

    # Find most stable and most variable stations
    if station_stability:
        # Sort by standard deviation (ascending for stable, descending for variable)
        sorted_stable = sorted(station_stability.items(), key=lambda x: x[1])
        sorted_variable = sorted(
            station_stability.items(), key=lambda x: x[1], reverse=True
        )

        # Find all stations with the same minimum and maximum std dev
        min_stddev = sorted_stable[0][1]
        max_stddev = sorted_variable[0][1]

        most_stable = [
            (station, stddev)
            for station, stddev in sorted_stable
            if stddev == min_stddev
        ]
        most_variable = [
            (station, stddev)
            for station, stddev in sorted_variable
            if stddev == max_stddev
        ]

        return {"most_stable": most_stable, "most_variable": most_variable}
    else:
        return {"most_stable": [], "most_variable": []}


def save_results(seasonal_averages, temperature_ranges, temperature_stability):
    """
    Save all analysis results to separate files.
    """
    # Save seasonal averages
    try:
        with open("Question2/average_temp.txt", "w", encoding="utf-8") as f:
            f.write("AUSTRALIAN SEASONAL AVERAGE TEMPERATURES\n")
            f.write("=" * 40 + "\n")
            f.write("Based on data from multiple weather stations across all years\n\n")

            for season, avg_temp in seasonal_averages.items():
                if avg_temp > 0:
                    f.write(f"{season}: {avg_temp}°C\n")
                else:
                    f.write(f"{season}: No data available\n")

        print(f"\nSeasonal averages saved to 'average_temp.txt'")

    except Exception as e:
        print(f"Error saving seasonal averages: {e}")

    # Save temperature ranges (only extreme ranges)
    try:
        with open("Question2/largest_temp_range_station.txt", "w", encoding="utf-8") as f:
            f.write("TEMPERATURE RANGE ANALYSIS\n")
            f.write("=" * 30 + "\n")
            f.write("Stations with extreme temperature ranges\n\n")

            # Get extreme ranges
            extreme_ranges = get_extreme_ranges(temperature_ranges)

            
            for station, data in extreme_ranges["highest"]:
                f.write(
                    f"{station}: Range {data['range']}°C (Max: {data['max']}°C, Min: {data['min']}°C)\n"
                )

    

        print(f"Temperature ranges saved to 'largest_temp_range_station.txt'")

    except Exception as e:
        print(f"Error saving temperature ranges: {e}")

    # Save temperature stability
    try:
        with open("Question2/temperature_stability_stations.txt", "w", encoding="utf-8") as f:
            f.write("TEMPERATURE STABILITY ANALYSIS\n")
            f.write("=" * 35 + "\n")
            f.write("Stations with most stable and variable temperatures\n\n")

            f.write("MOST STABLE STATIONS:\n")
            f.write("-" * 20 + "\n")
            for station, stddev in temperature_stability["most_stable"]:
                f.write(f"{station}: StdDev {stddev}°C\n")

            f.write("\nMOST VARIABLE STATIONS:\n")
            f.write("-" * 22 + "\n")
            for station, stddev in temperature_stability["most_variable"]:
                f.write(f"{station}: StdDev {stddev}°C\n")

        print(f"Temperature stability saved to 'temperature_stability_stations.txt'")

    except Exception as e:
        print(f"Error saving temperature stability: {e}")


def main():
    """
    Main entry point of the program
    """
    print("AUSTRALIAN WEATHER STATION TEMPERATURE ANALYZER")
    print("=" * 55)
    print("Analyzing temperature data from multiple weather stations...")
    print("Processing all CSV files in the 'temperatures' folder...")
    print("Analyzing seasonal averages, temperature ranges, and stability...")
    print()

    # Run the analysis
    analyze_temperature_data()

    print("\nAnalysis complete!")


if __name__ == "__main__":
    main()
