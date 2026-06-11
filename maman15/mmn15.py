import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Loads CSV file into a Pandas DataFrame.
def load_data(fileName):
    try:
        df = pd.read_csv(fileName)
        return df
    except FileNotFoundError:
        print("Error: file not found.")
    except PermissionError:
        print("Error: file is not accessible.")
    except pd.errors.EmptyDataError:
        print("Error: file is empty.")
    except pd.errors.ParserError:
        print("Error: invalid CSV format.")
    except Exception as e:
        print(f"Error loading file: {e}")
    return None

#Filters asteroids from year 2000 onward.
def data_mask(df):
    df["Close Approach Date"] = pd.to_datetime(df["Close Approach Date"], errors="coerce")
    df = df.query("`Close Approach Date`.dt.year >= 2000")
    return df

#Returns dataset size and column names after cleaning.
def details_data(df):
    df = df.drop(columns=['Orbiting Body', 'Neo Reference ID', 'Equinox'])
    return (len(df), df.shape[1], list(df.columns))

#Returns asteroid with maximum absolute magnitude.
def max_absolute_magnitude(df):
    return (df.loc[df["Absolute Magnitude"].idxmax(), "Name"], df.loc[df["Absolute Magnitude"].idxmax(), "Absolute Magnitude"])

#Returns the asteroid closest to Earth.
def closest_to_earth(df):
    return (df.loc[df["Miss Dist.(kilometers)"].idxmin(), "Name"])

#Counts asteroids per orbit ID.
def common_orbit(df):
    return df["Orbit ID"].value_counts().to_dict()

#Counts asteroids with max diameter above average.
def min_max_diameter(df):
    return (df["Est Dia in KM(max)"] > df["Est Dia in KM(max)"].mean()).sum()

#Histogram of average asteroid diameter (min/max mean) with 100 bins.
def plt_hist_diameter(df):
    ((df["Est Dia in KM(min)"] + df["Est Dia in KM(max)"]) / 2).plot(kind='hist', bins=100, color='gray')
    plt.title("Asteroid Average Diameter Distribution")
    plt.xlabel("Average Diameter (km)")
    plt.ylabel("Number of Asteroids")
    plt.show()

#Histogram of Minimum Orbit Intersection using 10 bins.
def ptl_hist_common_orbit(df):
    df["Minimum Orbit Intersection"].plot(kind='hist', bins=10, color='gray')
    plt.title("Minimum Orbit Intersection Distribution")
    plt.xlabel("Orbit Intersection Distance")
    plt.ylabel("Number of Asteroids")
    plt.show()

#Pie chart showing hazardous vs non-hazardous asteroid percentage.
def plt_pie_hazard(df):
    plt.pie(df["Hazardous"].value_counts(), labels=["Not Hazardous", "Hazardous"], autopct='%1.1f%%')
    plt.title("Hazardous vs Non-Hazardous Asteroids")
    plt.show()

#Linear regression between miss distance and asteroid velocity.
def plt_linear_motion_magnitude(df):
    sns.regplot(x=df["Miss Dist.(kilometers)"], y=df["Miles per hour"], line_kws={"color": "red"})
    plt.title("Distance vs Velocity Linear Regression")
    plt.xlabel("Miss Distance (km)")
    plt.ylabel("Speed (mph)")
    plt.show()