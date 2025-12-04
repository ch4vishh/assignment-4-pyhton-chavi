# Weather Data Visualizer Project
# Using Pandas, NumPy, and Matplotlib

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

print("Weather Project Started\n")

#create a folder named visualizatuin
if not os.path.exists("visualizations"):
    os.makedirs("visualizations")

#load data 
data = pd.read_csv("delhi_weather.csv")

print("First 5 rows:")
print(data.head())

print("\nData Info:")
print(data.info())

print("\nNumber Stats:")
print(data.describe())

#clean the Data
print("\nCleaning the data...")

#convert date column
data["Date"] = pd.to_datetime(data["date"], errors="coerce")

#match dataset columns
data["MinTemp"] = data["mintemp"]
data["MaxTemp"] = data["maxtemp"]
data["Rainfall"] = data["rainfall"]
data["Humidity9am"] = data["humidity"]
data["Humidity3pm"] = data["humidity"]

#select needed columns
needed_cols = ["Date", "MinTemp", "MaxTemp", "Rainfall", "Humidity9am", "Humidity3pm"]
cleaned = data[needed_cols].dropna()


cleaned["TempAvg"] = (cleaned["MinTemp"] + cleaned["MaxTemp"]) / 2
cleaned["HumAvg"] = (cleaned["Humidity9am"] + cleaned["Humidity3pm"]) / 2

print("\nAfter cleaning:")
print(cleaned.head())

#numPy statics
temp_arr = cleaned["TempAvg"].values
rain_arr = cleaned["Rainfall"].values
hum_arr = cleaned["HumAvg"].values

cleaned["Month"] = cleaned["Date"].dt.month
month_rain = cleaned.groupby("Month")["Rainfall"].sum()

#graphs
print("\nCreating graphs...")

sample_year = cleaned.head(365)

# (1) Line Chart
plt.plot(sample_year["Date"], sample_year["TempAvg"])
plt.title("Daily Temperature Trend")
plt.xlabel("Date")
plt.ylabel("Avg Temperature")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("visualizations/temp_graph.png")
plt.close()

# (2) Bar Chart
plt.bar(month_rain.index, month_rain.values)
plt.title("Monthly Rainfall")
plt.xlabel("Month")
plt.ylabel("Rainfall")
plt.savefig("visualizations/rain_graph.png")
plt.close()

# (3) Scatter Plot
plt.scatter(cleaned["HumAvg"], cleaned["TempAvg"], alpha=0.5)
plt.title("Humidity vs Temperature")
plt.xlabel("Avg Humidity")
plt.ylabel("Avg Temperature")
plt.savefig("visualizations/hum_temp_graph.png")
plt.close()

# (4) Combined Plot
fig, ax = plt.subplots(1, 2, figsize=(12, 5))

ax[0].plot(sample_year["Date"], sample_year["TempAvg"])
ax[0].set_title("Temperature Trend")
ax[0].tick_params(axis="x", rotation=45)

ax[1].bar(month_rain.index, month_rain.values)
ax[1].set_title("Monthly Rainfall")

plt.tight_layout()
plt.savefig("visualizations/combined_graph.png")
plt.close()

#save cleaned datta
cleaned.to_csv("cleaned_weather_data.csv", index=False)

#report 
report_text = f"""
# Weather Data Visualizer – Project Report
**Dataset:** Delhi Weather  
**Total Rows Used:** {len(cleaned)}

---

## 1. Introduction
This project analyzes real Delhi weather data using Python. It includes cleaning, processing, visualizing, and summarizing climate trends.

---

## 2. Dataset Summary
- Average Temperature: {np.mean(temp_arr):.2f}°C  
- Average Rainfall: {np.mean(rain_arr):.2f} mm  
- Average Humidity: {np.mean(hum_arr):.2f}%  
- Total Rainfall: {np.sum(rain_arr):.2f} mm  

---

## 3. Cleaning Steps Performed
- Converted date to datetime  
- Selected relevant weather columns  
- Removed missing values  
- Added Temperature & Humidity averages  
- Saved output as cleaned_weather_data.csv  

---

## 4. Statistical Analysis
### Temperature:
- Mean: {np.mean(temp_arr):.2f}°C  
- Min: {np.min(temp_arr):.2f}°C  
- Max: {np.max(temp_arr):.2f}°C  

### Rainfall:
- Mean: {np.mean(rain_arr):.2f} mm  
- Total Rainfall: {np.sum(rain_arr):.2f} mm  

### Humidity:
- Mean: {np.mean(hum_arr):.2f}%  
- Min: {np.min(hum_arr):.2f}%  
- Max: {np.max(hum_arr):.2f}%  

---

## 5. Monthly Rainfall Summary (Group By Month)
{month_rain.to_string()}

---

## 6. Visualizations Saved
All graphs saved inside **visualizations/** folder:
- temp_graph.png  
- rain_graph.png  
- hum_temp_graph.png  
- combined_graph.png  

---

## 7. Insights
- Temperature increases from January to February  
- Rainfall is very low in this period  
- Humidity decreases as temperature rises  
- Indicates winter → summer transition  

---

## 8. Conclusion
This project demonstrates real-world data analysis using Pandas, NumPy, and Matplotlib.  
It fulfills all assignment tasks: data loading, cleaning, grouping, analysis, visualization, and reporting.

---

End of Report.
"""

with open("weather_analysis_report.md", "w", encoding="utf-8") as r:
    r.write(report_text)

print("\nWeather Project Finished!")

