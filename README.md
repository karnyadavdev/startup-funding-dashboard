# Indian Startup Funding Dashboard (2015-2025)

I built this project because I kept reading news about the Indian startup "funding winter" and wanted to see what the numbers actually looked like. Everyone talks about how easy money was in 2021 compared to now, so I wanted to pull real deal data from 2015 to 2025 and visualize the trends myself across sectors, stages, and cities.

Note that this analysis is based on the public 37% sample release (5,006 of 13,697 total rounds, licensed under CC BY-NC 4.0 via Kaggle). To focus strictly on the 2015–2025 window, I filtered out 138 deals from 2026, leaving 4,868 rounds. Dropping 950 deals with undisclosed funding amounts left exactly 3,918 verified funding rounds across the 11-year period. The project includes both a standalone interactive web dashboard (built with HTML, Chart.js, and Leaflet) and a full Tableau workbook (.twbx) laid out for my portfolio.

## Files

- `clean_data.py` - downloads raw data, parses dates, drops empty funding amounts, and saves the cleaned CSV.
- `cleaned_indian_startup_funding.csv` - the filtered dataset with 3,918 rounds used by all the dashboards.
- `make_charts.py` - generates `dashboard.html` with all 6 charts, interactive filters, and city coordinate mappings.
- `dashboard.html` - standalone interactive dashboard you can open in any browser without needing Tableau.
- `make_tableau.py` - generates the Tableau workbook XML (`.twb`) and packages it into a portable `.twbx` file.
- `Indian_Startup_Funding_Landscape.twb` - Tableau workbook XML configured with all 6 sheets and dashboard sizing.
- `Indian_Startup_Funding_Landscape.twbx` - packaged Tableau workbook with bundled data, ready to open in Tableau Public or Desktop.

## How to run it

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. (Optional) Re-clean the dataset:
   ```bash
   python clean_data.py
   ```

3. Generate the web dashboard and open it:
   ```bash
   python make_charts.py
   ```
   Then double-click `dashboard.html` to open it in your browser.

4. Generate the Tableau files:
   ```bash
   python make_tableau.py
   ```
   Open `Indian_Startup_Funding_Landscape.twbx` in Tableau Public Desktop or upload it to Tableau Public web.

## What I learned

- I spent way too long debating what to do with the 950 rows where the funding amount was left blank or undisclosed. I thought about trying to impute values, but any kind of imputation felt like inventing money that was never actually disclosed. Dropping them down to 3,918 verified deals was the only honest option, even though losing that many rows hurt a bit.
- Looking at the sector distribution, the top 3 sectors alone (Consumer at $20.85B / 23.5%, Retail at $12.47B / 14.1%, and Fintech at $10.87B / 12.3%) accounted for $44.19B or 49.85% of all $88.6B raised. Rounding out the top 5 were Food and Agriculture Tech ($6.46B / 7.3%) and Energy ($6.15B / 6.9%).
- The weird realization was that Tableau workbooks (.twb) are literally just giant XML files under the hood. Figuring out that a .twbx is just that same XML zipped together with a Data/ folder saved me from having to manually drag out all six sheets in the desktop app.
- Also realized you don't need a Node or Flask backend for simple dashboards — dumping the clean records straight into client-side JS handles the filter dropdowns instantly.
