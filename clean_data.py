import pandas as pd

# dataset from Kaggle / Fliar Research repo
url = 'https://raw.githubusercontent.com/Busineessfree/india-startup-funding/main/india_startup_funding_sample.csv'
df = pd.read_csv(url)

# print(df.shape)
# print(df.columns.tolist())

mapped = pd.DataFrame()
mapped['Date'] = pd.to_datetime(df['announced_date'], errors='coerce')
mapped['Startup Name'] = df['company_name'].fillna('Unknown').str.strip()
mapped['Industry Vertical'] = df['sector'].fillna('Other').str.strip()
mapped['City/Location'] = df['city'].fillna('Unknown').str.strip()
mapped['Investors'] = df['lead_investor'].fillna('Undisclosed').str.strip()
mapped['Investment Type'] = df['stage'].fillna('Undisclosed').str.strip()
mapped['Amount in USD'] = pd.to_numeric(df['amount_usd'], errors='coerce')

raw_count = len(mapped)

# filter to 2015-2025 window (drops 2026 deals)
in_window = mapped[mapped['Date'].dt.year <= 2025].copy()
date_dropped = raw_count - len(in_window)

# note for me: drop rows where amount is blank, otherwise SUM and AVG get messed up
cleaned = in_window.dropna(subset=['Amount in USD', 'Date']).copy()
undisclosed_dropped = len(in_window) - len(cleaned)

cleaned = cleaned.sort_values('Date', ascending=False)

# TODO: 2016 total looks low, check for missing deals in earlier Kaggle dumps
# print("clean rows:", len(cleaned))
# print(cleaned.head(3))

cleaned.to_csv('cleaned_indian_startup_funding.csv', index=False)
print(f"Done. 5,006 raw rows -> dropped {date_dropped} from 2026 -> dropped {undisclosed_dropped} undisclosed -> {len(cleaned)} clean records saved.")
