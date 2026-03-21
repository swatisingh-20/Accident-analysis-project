import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Read Excel
df = pd.read_excel("Accident_Data_2026.xlsx")

# Add new row
df.loc[len(df)] = [
    'uttarpradesh',
    'lucknow',
    pd.to_datetime('2026-01-05'),
    pd.to_datetime('07:15').time(),
    'rain',
    'city',
    2,
    'major'
]
# Data Understanding
print(df.head())
print(df.tail(1))
print(df.describe())
print(df.info())

# Data Cleaning
print(df.isnull())
print(df.dropna())
print(df.drop_duplicates())
df = df.rename(columns={'Vehicles_Involved':'Number_of_Vehicle'})
print(df.sort_values('Number_of_Vehicle',ascending=False))

# Date Extract
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day
df['Weekday'] = df['Date'].dt.day_name()
print(df)

# Groupby

print(df['Number_of_Vehicle'].value_counts())
print(df.groupby('State').size().sort_values(ascending=False))
print(df.groupby('Weather').size())
print(df.groupby(['Road_Type','Severity']).size())
print(df['Weekday'].value_counts())
print(df['Number_of_Vehicle'].mean())

# SQLite Database
conn = sqlite3.connect("Accident_analysis.db")
df.to_sql("Accident_analysis", conn, if_exists="replace", index=False)
print("Database connected and data inserted")

# SQL Queries
query1 = "SELECT COUNT(*) AS Total FROM Accident_analysis"
df1 = pd.read_sql(query1, conn)
print(df1)


query2 = """
SELECT State, COUNT(*) AS Total
FROM Accident_analysis
GROUP BY State
ORDER BY Total DESC
"""
df2 = pd.read_sql(query2, conn)
print(df2)


query3 = """
SELECT Weather, COUNT(*) AS Total
FROM Accident_analysis
GROUP BY Weather
"""
df3 = pd.read_sql(query3, conn)
print(df3)


query4 = """
SELECT Severity, COUNT(*) AS Total
FROM Accident_analysis
GROUP BY Severity
"""
df4 = pd.read_sql(query4, conn)
print(df4)


query5 = """
SELECT Number_of_Vehicle FROM Accident_analysis
"""
df5 = pd.read_sql(query5, conn)

# Graph 1 State Wise
plt.figure()
plt.bar(df2["State"], df2["Total"])
plt.title("State Wise Accidents")
plt.xticks(rotation=45)
plt.savefig("state_chart.png")
plt.show()

# Graph 2 Severity Pie
plt.figure()
plt.pie(df4["Total"], labels=df4["Severity"], autopct='%1.0f%%')
plt.title("Severity Distribution")
plt.savefig("severity_chart.png")
plt.show()

# Graph 3 Weather
plt.figure()
plt.bar(df3["Weather"], df3["Total"])
plt.title("Weather Wise Accidents")
plt.savefig("weather_chart.png")
plt.show()

# Histogram
plt.figure()
plt.hist(df5["Number_of_Vehicle"])
plt.title("Vehicles Histogram")
plt.savefig("vehicle_chart.png")
plt.show()

# Close DB
conn.close()
print("Project Finished Successfully")