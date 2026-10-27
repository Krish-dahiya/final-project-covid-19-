# COVID-19 Data Analysis and Visualization

A beginner-friendly Python project that analyzes historical COVID-19 data and creates charts using **Pandas, Matplotlib, and Seaborn**.

## Project features

- Downloads the required historical CSV files automatically.
- Plots global confirmed cases, deaths, and reported recoveries over time.
- Shows the 10 countries with the highest reported confirmed-case totals.
- Shows the 10 countries with the highest reported death totals.
- Creates a correlation heatmap for the latest country totals.
- Saves all graphs in the `graphs/` folder.

## Tools used

- Python
- Pandas
- Matplotlib
- Seaborn

## How to run in VS Code

### 1. Download and extract this project

Extract the ZIP file, then open the `COVID-19-Analysis` folder in VS Code.

### 2. Open the terminal

In VS Code, select **Terminal → New Terminal**.

### 3. Install the libraries

```bash
python -m pip install -r requirements.txt
```

### 4. Run the project

```bash
python main.py
```

On the first run, the program downloads the three historical CSV files from the Johns Hopkins CSSE COVID-19 repository. An internet connection is required for this step.

### 5. View the output

After the program finishes, open the `graphs` folder. It should contain:

- `global_trends.png`
- `top_10_countries.png`
- `top_10_deaths.png`
- `correlation_heatmap.png`

## Dataset source

Historical Johns Hopkins CSSE COVID-19 time-series data:

- [Confirmed cases CSV](https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv)
- [Deaths CSV](https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv)
- [Recovered CSV](https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv)

The source repository is historical/archived. Recovery reporting may be incomplete for later dates, so recovery totals should be interpreted carefully. The charts describe reported counts and do not establish that one factor caused another.

## Folder structure

```text
COVID-19-Analysis/
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
├── REPORT_TEMPLATE.md
├── PRESENTATION.md
├── confirmed.csv       # downloaded automatically on first run
├── deaths.csv          # downloaded automatically on first run
├── recovered.csv       # downloaded automatically on first run
└── graphs/
    └── (charts appear after running main.py)
```

## Project objective

To explore how reported COVID-19 cases, deaths, and recoveries changed over time and compare reported totals between countries using simple visualizations.

## Important note

This is an educational data-analysis project, not a medical tool. Results depend on historical reporting practices and dataset limitations.
