from pathlib import Path
import urllib.request
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# COVID-19 Data Analysis and Visualization
# Run: python main.py

DATA_DIR = Path(".")
GRAPH_DIR = DATA_DIR / "graphs"
GRAPH_DIR.mkdir(exist_ok=True)

DATA_URLS = {
    "confirmed.csv": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv",
    "deaths.csv": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv",
    "recovered.csv": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv",
}

def download_data():
    """Download the historical CSV files if they are not already in the project folder."""
    for filename, url in DATA_URLS.items():
        path = DATA_DIR / filename
        if not path.exists():
            print(f"Downloading {filename} ...")
            try:
                urllib.request.urlretrieve(url, path)
                print(f"Saved: {path}")
            except Exception as error:
                raise RuntimeError(
                    f"Could not download {filename}. Check your internet connection, "
                    f"then try again. Original error: {error}"
                )

def load_data(filename):
    df = pd.read_csv(DATA_DIR / filename)
    if "Country/Region" not in df.columns:
        raise ValueError(f"{filename} does not have the expected 'Country/Region' column.")
    # JHU files have four location columns followed by date columns.
    date_columns = list(df.columns[4:])
    if not date_columns:
        raise ValueError(f"No date columns found in {filename}.")
    return df, date_columns

def make_global_chart(confirmed, deaths, recovered, dates):
    global_confirmed = confirmed[dates].sum()
    global_deaths = deaths[dates].sum()
    global_recovered = recovered[dates].sum()

    # Convert JHU date labels into dates for a cleaner chart.
    date_index = pd.to_datetime(dates, format="%m/%d/%y", errors="coerce")
    chart_data = pd.DataFrame({
        "Date": date_index,
        "Confirmed cases": global_confirmed.values,
        "Deaths": global_deaths.values,
        "Recovered": global_recovered.values,
    }).dropna(subset=["Date"])

    plt.figure(figsize=(12, 6))
    for column in ["Confirmed cases", "Deaths", "Recovered"]:
        plt.plot(chart_data["Date"], chart_data[column], label=column)
    plt.title("Global COVID-19: Confirmed Cases, Deaths and Recoveries")
    plt.xlabel("Date")
    plt.ylabel("Cumulative reported count")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(GRAPH_DIR / "global_trends.png", dpi=150)
    plt.close()

def make_top_countries_chart(confirmed, dates):
    country_totals = confirmed.groupby("Country/Region", as_index=True)[dates].sum()
    latest_date = dates[-1]
    top_10 = country_totals[latest_date].sort_values(ascending=False).head(10).sort_values()

    plt.figure(figsize=(10, 6))
    top_10.plot(kind="barh")
    plt.title(f"Top 10 Countries by Reported Confirmed Cases ({latest_date})")
    plt.xlabel("Cumulative confirmed cases")
    plt.ylabel("Country")
    plt.tight_layout()
    plt.savefig(GRAPH_DIR / "top_10_countries.png", dpi=150)
    plt.close()

def make_deaths_chart(deaths, dates):
    country_totals = deaths.groupby("Country/Region", as_index=True)[dates].sum()
    latest_date = dates[-1]
    top_10 = country_totals[latest_date].sort_values(ascending=False).head(10).sort_values()

    plt.figure(figsize=(10, 6))
    top_10.plot(kind="barh")
    plt.title(f"Top 10 Countries by Reported Deaths ({latest_date})")
    plt.xlabel("Cumulative reported deaths")
    plt.ylabel("Country")
    plt.tight_layout()
    plt.savefig(GRAPH_DIR / "top_10_deaths.png", dpi=150)
    plt.close()

def make_correlation_heatmap(confirmed, deaths, recovered, dates):
    # Compare latest cumulative totals by country. This is descriptive, not causal.
    c = confirmed.groupby("Country/Region")[dates[-1]].sum().rename("Confirmed")
    d = deaths.groupby("Country/Region")[dates[-1]].sum().rename("Deaths")
    r = recovered.groupby("Country/Region")[dates[-1]].sum().rename("Recovered")
    combined = pd.concat([c, d, r], axis=1).fillna(0)
    correlation = combined.corr(numeric_only=True)

    plt.figure(figsize=(7, 5))
    sns.heatmap(correlation, annot=True, cmap="coolwarm", vmin=-1, vmax=1, fmt=".2f")
    plt.title("Correlation Between Latest Country Totals")
    plt.tight_layout()
    plt.savefig(GRAPH_DIR / "correlation_heatmap.png", dpi=150)
    plt.close()

def main():
    print("=== COVID-19 Data Analysis and Visualization ===")
    download_data()

    confirmed, dates = load_data("confirmed.csv")
    deaths, _ = load_data("deaths.csv")
    recovered, _ = load_data("recovered.csv")

    # Keep the same date columns across files in case the source changes.
    dates = [date for date in dates if date in deaths.columns and date in recovered.columns]
    if not dates:
        raise ValueError("The three CSV files do not share date columns.")

    make_global_chart(confirmed, deaths, recovered, dates)
    make_top_countries_chart(confirmed, dates)
    make_deaths_chart(deaths, dates)
    make_correlation_heatmap(confirmed, deaths, recovered, dates)

    print("\nDone! Your graphs are saved in the 'graphs' folder:")
    for path in sorted(GRAPH_DIR.glob("*.png")):
        print(f" - {path}")
    print("\nNote: This is historical reported data. The recovery file may be incomplete "
          "for later dates, so interpret recovery totals carefully.")

if __name__ == "__main__":
    main()
