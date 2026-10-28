import json
import pandas as pd

df = pd.read_csv('cleaned_indian_startup_funding.csv')

# print(df.shape)
# quick lat/lng lookup for major hubs so Leaflet puts bubbles in the right spot
city_coords = {
    'Bengaluru': [12.9716, 77.5946],
    'Mumbai': [19.0760, 72.8777],
    'Gurugram': [28.4595, 77.0266],
    'New Delhi': [28.6139, 77.2090],
    'Noida': [28.5355, 77.3910],
    'Pune': [18.5204, 73.8567],
    'Hyderabad': [17.3850, 78.4867],
    'Chennai': [13.0827, 80.2707],
    'Jaipur': [26.9124, 75.7873],
    'Ahmedabad': [23.0225, 72.5714],
    'Kolkata': [22.5726, 88.3639],
    'Chandigarh': [30.7333, 76.7794],
    'Kochi': [9.9312, 76.2673],
    'Indore': [22.7196, 75.8577],
    'Surat': [21.1702, 72.8311],
    'Goa': [15.2993, 74.1240],
    'Thane': [19.2183, 72.9781],
    'Bhopal': [23.2599, 77.4126],
    'Lucknow': [26.8467, 80.9462],
    'Coimbatore': [11.0168, 76.9558],
    'Vadodara': [22.3072, 73.1812],
    'Nagpur': [21.1458, 79.0882],
    'Patna': [25.5941, 85.1376],
    'Bhubaneswar': [20.2961, 85.8245],
    'Visakhapatnam': [17.6868, 83.2185]
}

# fallback to center of India if city wasn't in the dict
df['Lat'] = df['City/Location'].map(lambda c: city_coords.get(c, [20.5937, 78.9629])[0])
df['Lng'] = df['City/Location'].map(lambda c: city_coords.get(c, [20.5937, 78.9629])[1])
df['Year'] = pd.to_datetime(df['Date']).dt.year

# pack into json so dashboard.html can run standalone without a local backend
records_json = df[['Date', 'Year', 'Startup Name', 'Industry Vertical', 'City/Location', 'Investment Type', 'Amount in USD', 'Lat', 'Lng']].to_json(orient='records')

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Indian Startup Funding Landscape (2015–2025)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

  <style>
    :root {{
      --accent: #B3541E;
      --accent-light: rgba(179, 84, 30, 0.12);
      --accent-glow: rgba(179, 84, 30, 0.25);
      --bg: #F8F9FA;
      --card-bg: #FFFFFF;
      --text-main: #1E232A;
      --text-muted: #64748B;
      --border-color: #E2E8F0;
      --serif: 'Playfair Display', Georgia, serif;
      --sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      background-color: var(--bg);
      color: var(--text-main);
      font-family: var(--sans);
      display: flex;
      justify-content: center;
      padding: 30px 15px;
    }}

    .dashboard-container {{
      width: 100%;
      max-width: 1280px;
      min-height: 1700px;
      background: var(--card-bg);
      box-shadow: 0 10px 40px rgba(0,0,0,0.06);
      border-radius: 8px;
      padding: 40px 50px;
      display: flex;
      flex-direction: column;
      gap: 48px;
    }}

    .dashboard-header {{
      border-bottom: 2px solid var(--border-color);
      padding-bottom: 24px;
    }}

    .dashboard-title {{
      font-family: var(--serif);
      font-size: 34px;
      font-weight: 800;
      color: #111827;
      letter-spacing: -0.5px;
      margin-bottom: 8px;
    }}

    .dashboard-subtitle {{
      font-size: 16px;
      color: var(--text-muted);
      font-weight: 500;
    }}

    .filters-bar {{
      display: flex;
      gap: 24px;
      background: #F8FAFC;
      border: none;
      box-shadow: 0 1px 3px rgba(0,0,0,0.03);
      border-radius: 8px;
      padding: 18px 24px;
      align-items: center;
      flex-wrap: wrap;
    }}

    .filter-label {{
      font-size: 13px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--text-muted);
    }}

    .filter-group {{
      display: flex;
      flex-direction: column;
      gap: 4px;
      flex: 1;
      min-width: 180px;
    }}

    .filter-select {{
      height: 38px;
      padding: 0 12px;
      border: 1px solid var(--border-color);
      border-radius: 6px;
      background: #FFFFFF;
      font-family: var(--sans);
      font-size: 14px;
      font-weight: 500;
      color: var(--text-main);
      cursor: pointer;
      outline: none;
      transition: border-color 0.2s;
    }}

    .filter-select:focus {{
      border-color: var(--accent);
    }}

    .reset-btn {{
      height: 38px;
      padding: 0 18px;
      margin-top: 18px;
      border: 1px solid var(--accent);
      background: transparent;
      color: var(--accent);
      border-radius: 6px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }}

    .reset-btn:hover {{
      background: var(--accent);
      color: #FFFFFF;
    }}

    .kpi-row {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 36px;
    }}

    .kpi-card {{
      background: #FFFFFF;
      border: none;
      border-top: 4px solid var(--accent);
      border-radius: 6px;
      padding: 28px 24px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }}

    .kpi-title {{
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.75px;
      color: var(--text-muted);
    }}

    .kpi-value {{
      font-family: var(--serif);
      font-size: 38px;
      font-weight: 700;
      color: #0F172A;
    }}

    .kpi-subtext {{
      font-size: 12px;
      color: var(--text-muted);
    }}

    .charts-grid-hero {{
      display: grid;
      grid-template-columns: 1.4fr 1fr;
      gap: 36px;
    }}

    .charts-grid-sub {{
      display: grid;
      grid-template-columns: 1.05fr 0.95fr;
      gap: 36px;
    }}

    .chart-panel {{
      border: none;
      border-radius: 8px;
      padding: 24px;
      background: #FFFFFF;
      display: flex;
      flex-direction: column;
      box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }}

    .chart-header {{
      margin-bottom: 16px;
    }}

    .chart-title {{
      font-family: var(--serif);
      font-size: 18px;
      font-weight: 700;
      color: #0F172A;
      margin-bottom: 4px;
    }}

    .chart-subtitle {{
      font-size: 12px;
      color: var(--text-muted);
    }}

    .chart-canvas-wrapper {{
      position: relative;
      flex: 1;
      min-height: 310px;
    }}

    #map {{
      height: 330px;
      width: 100%;
      border-radius: 6px;
    }}

    .table-panel {{
      border: none;
      border-radius: 8px;
      padding: 24px;
      background: #FFFFFF;
      box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }}

    .styled-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
      margin-top: 10px;
    }}

    .styled-table th {{
      text-align: left;
      padding: 10px 14px;
      background: #F8FAFC;
      border-bottom: 2px solid var(--border-color);
      color: var(--text-muted);
      font-weight: 700;
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    .styled-table td {{
      padding: 11px 14px;
      border-bottom: 1px solid #F1F5F9;
      color: #334155;
    }}

    .styled-table tr:hover td {{
      background: #F8FAFC;
    }}

    .funding-pill {{
      display: inline-block;
      padding: 4px 10px;
      border-radius: 4px;
      background: var(--accent-light);
      color: var(--accent);
      font-weight: 700;
      font-family: var(--sans);
    }}

    .rank-badge {{
      display: inline-block;
      width: 22px;
      height: 22px;
      line-height: 22px;
      text-align: center;
      background: #E2E8F0;
      color: #475569;
      font-size: 11px;
      font-weight: 700;
      border-radius: 50%;
      margin-right: 8px;
    }}

    .rank-badge.top3 {{
      background: var(--accent);
      color: #FFFFFF;
    }}

    .footer-bar {{
      margin-top: auto;
      border-top: 1px solid var(--border-color);
      padding-top: 16px;
      display: flex;
      justify-content: space-between;
      font-size: 12px;
      color: #94A3B8;
    }}
  </style>
</head>
<body>

  <div class="dashboard-container">
    <header class="dashboard-header">
      <h1 class="dashboard-title">Indian Startup Funding Landscape (2015–2025)</h1>
      <p class="dashboard-subtitle">Sector trends, city ecosystems and stage-wise deal flow · (5,006-record sample, 3,918 analyzed)</p>
    </header>

    <div class="filters-bar">
      <div class="filter-group">
        <label class="filter-label" for="yearFilter">Year</label>
        <select id="yearFilter" class="filter-select">
          <option value="ALL">All Years (2015–2025)</option>
        </select>
      </div>

      <div class="filter-group">
        <label class="filter-label" for="sectorFilter">Sector</label>
        <select id="sectorFilter" class="filter-select">
          <option value="ALL">All Sectors</option>
        </select>
      </div>

      <div class="filter-group">
        <label class="filter-label" for="cityFilter">City</label>
        <select id="cityFilter" class="filter-select">
          <option value="ALL">All Cities</option>
        </select>
      </div>

      <button id="resetFilters" class="reset-btn">Reset Filters</button>
    </div>

    <div class="kpi-row">
      <div class="kpi-card">
        <div class="kpi-title">Total Funding Raised</div>
        <div id="kpiFunding" class="kpi-value">$0.00B</div>
        <div id="kpiFundingSub" class="kpi-subtext">Across all completed rounds</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-title">Total Deal Count</div>
        <div id="kpiDeals" class="kpi-value">0</div>
        <div class="kpi-subtext">Verified investment rounds</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-title">Average Deal Size</div>
        <div id="kpiAvg" class="kpi-value">$0.0M</div>
        <div class="kpi-subtext">Mean capital per round</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-title">Top Sector</div>
        <div id="kpiSector" class="kpi-value" style="font-size: 24px; padding-top: 5px;">-</div>
        <div id="kpiSectorSub" class="kpi-subtext">By aggregate capital deployed</div>
      </div>
    </div>

    <div class="charts-grid-hero">
      <div class="chart-panel">
        <div class="chart-header">
          <h2 class="chart-title">Funding peaked in 2021 — sharp correction since</h2>
          <p class="chart-subtitle">Annual capital deployed</p>
        </div>
        <div class="chart-canvas-wrapper">
          <canvas id="trendChart"></canvas>
        </div>
      </div>

      <div class="chart-panel">
        <div class="chart-header">
          <h2 class="chart-title">Top 3 sectors absorb nearly half of all capital</h2>
          <p class="chart-subtitle">Top 10 sectors by funding · Categories as classified by the source dataset</p>
        </div>
        <div class="chart-canvas-wrapper">
          <canvas id="sectorChart"></canvas>
        </div>
      </div>
    </div>

    <div class="charts-grid-sub">
      <div class="chart-panel">
        <div class="chart-header">
          <h2 class="chart-title">Bangalore, Mumbai and Delhi-NCR dominate deal flow</h2>
          <p class="chart-subtitle">Bubble size = total funding</p>
        </div>
        <div id="map"></div>
      </div>

      <div class="chart-panel">
        <div class="chart-header">
          <h2 class="chart-title">Early-stage share fell 13 points (33% to 20%)</h2>
          <p class="chart-subtitle">Deals Count by Year and Investment Stage</p>
        </div>
        <div class="chart-canvas-wrapper">
          <canvas id="stageChart"></canvas>
        </div>
      </div>
    </div>

    <div class="table-panel">
      <div class="chart-header">
        <h2 class="chart-title">Top 15 funded startups</h2>
        <p class="chart-subtitle">Ranked by total capital raised in USD</p>
      </div>
      <table class="styled-table">
        <thead>
          <tr>
            <th style="width: 60px;">Rank</th>
            <th>Startup Name</th>
            <th>Sector</th>
            <th>City</th>
            <th style="text-align: right;">Total Funding (USD)</th>
          </tr>
        </thead>
        <tbody id="topTableBody">
        </tbody>
      </table>
    </div>

    <footer class="footer-bar">
      <span>Indian Startup Funding Landscape (2015–2025) · (5,006-record sample, 3,918 analyzed)</span>
      <span>Data: Fliar Research (via Kaggle) (CC BY-NC 4.0)</span>
    </footer>
  </div>

  <script>
    const rawData = {records_json};

    const yearSelect = document.getElementById('yearFilter');
    const sectorSelect = document.getElementById('sectorFilter');
    const citySelect = document.getElementById('cityFilter');
    const resetBtn = document.getElementById('resetFilters');

    // populate dropdowns
    const years = Array.from(new Set(rawData.map(d => d.Year))).filter(Boolean).sort((a,b) => b-a);
    years.forEach(y => {{
      const opt = document.createElement('option');
      opt.value = y;
      opt.textContent = y;
      yearSelect.appendChild(opt);
    }});

    const sectors = Array.from(new Set(rawData.map(d => d['Industry Vertical']))).filter(Boolean).sort();
    sectors.forEach(s => {{
      const opt = document.createElement('option');
      opt.value = s;
      opt.textContent = s;
      sectorSelect.appendChild(opt);
    }});

    const cities = Array.from(new Set(rawData.map(d => d['City/Location']))).filter(Boolean).sort();
    cities.forEach(c => {{
      const opt = document.createElement('option');
      opt.value = c;
      opt.textContent = c;
      citySelect.appendChild(opt);
    }});

    let trendChart = null;
    let sectorChart = null;
    let stageChart = null;
    let map = null;
    let mapMarkers = [];

    function initMap() {{
      map = L.map('map', {{
        center: [21.5, 78.9],
        zoom: 4.4,
        zoomControl: true,
        attributionControl: false
      }});

      L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
        maxZoom: 19
      }}).addTo(map);
    }}

    function formatCurrency(val) {{
      if (val >= 1e9) return '$' + (val / 1e9).toFixed(2) + 'B';
      if (val >= 1e6) return '$' + (val / 1e6).toFixed(1) + 'M';
      if (val >= 1e3) return '$' + (val / 1e3).toFixed(0) + 'K';
      return '$' + val.toLocaleString();
    }}

    function updateDashboard() {{
      const selectedYear = yearSelect.value;
      const selectedSector = sectorSelect.value;
      const selectedCity = citySelect.value;

      const filtered = rawData.filter(d => {{
        if (selectedYear !== 'ALL' && d.Year != selectedYear) return false;
        if (selectedSector !== 'ALL' && d['Industry Vertical'] !== selectedSector) return false;
        if (selectedCity !== 'ALL' && d['City/Location'] !== selectedCity) return false;
        return true;
      }});

      // update big numbers
      const totalFunding = filtered.reduce((acc, d) => acc + (d['Amount in USD'] || 0), 0);
      const totalDeals = filtered.length;
      const avgDeal = totalDeals > 0 ? totalFunding / totalDeals : 0;

      const sectorAgg = {{}};
      filtered.forEach(d => {{
        const s = d['Industry Vertical'] || 'Other';
        sectorAgg[s] = (sectorAgg[s] || 0) + (d['Amount in USD'] || 0);
      }});
      const sortedSectors = Object.entries(sectorAgg).sort((a,b) => b[1] - a[1]);
      const topSector = sortedSectors.length > 0 ? sortedSectors[0][0] : 'None';
      const topSectorVal = sortedSectors.length > 0 ? sortedSectors[0][1] : 0;

      document.getElementById('kpiFunding').textContent = formatCurrency(totalFunding);
      document.getElementById('kpiDeals').textContent = totalDeals.toLocaleString();
      document.getElementById('kpiAvg').textContent = formatCurrency(avgDeal);
      document.getElementById('kpiSector').textContent = topSector;
      document.getElementById('kpiSectorSub').textContent = formatCurrency(topSectorVal) + ' deployed';

      // funding trend area chart
      const yearlyFunding = {{}};
      filtered.forEach(d => {{
        if (!d.Year) return;
        yearlyFunding[d.Year] = (yearlyFunding[d.Year] || 0) + (d['Amount in USD'] || 0);
      }});
      const trendYears = Object.keys(yearlyFunding).sort();
      const trendValues = trendYears.map(y => yearlyFunding[y] / 1e9);

      if (trendChart) trendChart.destroy();
      const ctxTrend = document.getElementById('trendChart').getContext('2d');

      trendChart = new Chart(ctxTrend, {{
        type: 'line',
        data: {{
          labels: trendYears,
          datasets: [{{
            label: 'Funding (USD Billions)',
            data: trendValues,
            fill: true,
            backgroundColor: 'rgba(179, 84, 30, 0.12)',
            borderColor: '#B3541E',
            borderWidth: 2.5,
            tension: 0.35,
            pointBackgroundColor: '#B3541E',
            pointRadius: 4,
            pointHoverRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ display: false }},
            tooltip: {{
              callbacks: {{
                label: function(ctx) {{
                  return ' Amount: $' + ctx.parsed.y.toFixed(2) + ' Billion';
                }}
              }}
            }}
          }},
          scales: {{
            x: {{ grid: {{ display: false }}, border: {{ display: false }} }},
            y: {{
              grid: {{ display: false }},
              border: {{ display: false }},
              ticks: {{
                callback: function(v) {{ return '$' + v + 'B'; }}
              }}
            }}
          }}
        }}
      }});

      // top 10 sectors horizontal bar
      const top10Sectors = sortedSectors.slice(0, 10);
      const sectorLabels = top10Sectors.map(s => s[0]);
      const sectorValues = top10Sectors.map(s => (s[1] / 1e9));

      if (sectorChart) sectorChart.destroy();
      const ctxSector = document.getElementById('sectorChart').getContext('2d');
      sectorChart = new Chart(ctxSector, {{
        type: 'bar',
        data: {{
          labels: sectorLabels,
          datasets: [{{
            axis: 'y',
            data: sectorValues,
            backgroundColor: '#B3541E',
            borderRadius: 4
          }}]
        }},
        options: {{
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ display: false }},
            tooltip: {{
              callbacks: {{
                label: function(ctx) {{
                  return ' Sector: ' + ctx.label + ' | Amount: $' + ctx.parsed.x.toFixed(2) + 'B';
                }}
              }}
            }}
          }},
          scales: {{
            x: {{
              grid: {{ display: false }},
              border: {{ display: false }},
              ticks: {{ callback: function(v) {{ return '$' + v + 'B'; }} }}
            }},
            y: {{ grid: {{ display: false }}, border: {{ display: false }} }}
          }}
        }}
      }});

      // city hub bubbles
      mapMarkers.forEach(m => map.removeLayer(m));
      mapMarkers = [];

      const cityAgg = {{}};
      filtered.forEach(d => {{
        const c = d['City/Location'];
        if (!c || c === 'Unknown') return;
        if (!cityAgg[c]) {{
          cityAgg[c] = {{ amount: 0, deals: 0, lat: d.Lat, lng: d.Lng }};
        }}
        cityAgg[c].amount += (d['Amount in USD'] || 0);
        cityAgg[c].deals += 1;
      }});

      const maxCityAmount = Math.max(...Object.values(cityAgg).map(c => c.amount), 1);

      Object.entries(cityAgg).forEach(([cityName, info]) => {{
        // clamped radius between 5 and 32 so big hubs dont cover the whole country
        const radius = Math.max(5, Math.min(32, Math.sqrt(info.amount / maxCityAmount) * 32));
        const marker = L.circleMarker([info.lat, info.lng], {{
          radius: radius,
          fillColor: '#B3541E',
          color: '#8A3B0F',
          weight: 1.5,
          opacity: 0.9,
          fillOpacity: 0.7
        }}).addTo(map);

        marker.bindPopup(`
          <div style="font-family: sans-serif; font-size: 13px; line-height: 1.4;">
            <b style="color: #111;">${{cityName}}</b><br>
            <span style="color: #64748B;">Total Funding:</span> <b>${{formatCurrency(info.amount)}}</b><br>
            <span style="color: #64748B;">Total Deals:</span> <b>${{info.deals}}</b>
          </div>
        `);
        mapMarkers.push(marker);
      }});

      // stage distribution over time - 3 distinct series
      const stageSeries = [
        {{ key: 'early', label: 'Early (Seed/Pre-Series A/Angel)', color: '#B3541E', stages: ['Seed', 'Pre-Series A', 'Angel', 'Pre-seed', 'Grant'] }},
        {{ key: 'growth', label: 'Growth (Series A-C)', color: '#4B5563', stages: ['Series A', 'Pre-Series B', 'Series B', 'Pre-Series C', 'Series C'] }},
        {{ key: 'late', label: 'Late/Debt', color: '#9CA3AF', stages: [] }}
      ];

      const stageCounts = {{ early: {{}}, growth: {{}}, late: {{}} }};
      filtered.forEach(d => {{
        if (!d.Year) return;
        const stage = d['Investment Type'] || 'Undisclosed';
        let group = 'late';
        if (stageSeries[0].stages.includes(stage)) {{
          group = 'early';
        }} else if (stageSeries[1].stages.includes(stage)) {{
          group = 'growth';
        }}
        stageCounts[group][d.Year] = (stageCounts[group][d.Year] || 0) + 1;
      }});

      const stageDatasets = stageSeries.map(s => ({{
        label: s.label,
        data: trendYears.map(y => stageCounts[s.key][y] || 0),
        backgroundColor: s.color,
        borderRadius: 2
      }}));

      if (stageChart) stageChart.destroy();
      const ctxStage = document.getElementById('stageChart').getContext('2d');
      stageChart = new Chart(ctxStage, {{
        type: 'bar',
        data: {{
          labels: trendYears,
          datasets: stageDatasets
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ position: 'bottom', labels: {{ boxWidth: 12, font: {{ size: 11 }} }} }},
            tooltip: {{ mode: 'index', intersect: false }}
          }},
          scales: {{
            x: {{ stacked: true, grid: {{ display: false }}, border: {{ display: false }} }},
            y: {{ stacked: true, grid: {{ display: false }}, border: {{ display: false }} }}
          }}
        }}
      }});

      // top 15 startups table
      const startupAgg = {{}};
      filtered.forEach(d => {{
        const name = d['Startup Name'];
        if (!name || name === 'Unknown') return;
        if (!startupAgg[name]) {{
          startupAgg[name] = {{ amount: 0, sector: d['Industry Vertical'], city: d['City/Location'] }};
        }}
        startupAgg[name].amount += (d['Amount in USD'] || 0);
      }});

      const sortedStartups = Object.entries(startupAgg)
        .sort((a,b) => b[1].amount - a[1].amount)
        .slice(0, 15);

      const tableBody = document.getElementById('topTableBody');
      tableBody.innerHTML = '';
      sortedStartups.forEach(([name, info], idx) => {{
        const tr = document.createElement('tr');
        const rankClass = idx < 3 ? 'rank-badge top3' : 'rank-badge';
        tr.innerHTML = `
          <td><span class="${{rankClass}}">${{idx + 1}}</span></td>
          <td style="font-weight: 600; color: #0F172A;">${{name}}</td>
          <td><span style="color: #475569;">${{info.sector}}</span></td>
          <td><span style="color: #64748B;">${{info.city}}</span></td>
          <td style="text-align: right;"><span class="funding-pill">${{formatCurrency(info.amount)}}</span></td>
        `;
        tableBody.appendChild(tr);
      }});
    }}

    yearSelect.addEventListener('change', updateDashboard);
    sectorSelect.addEventListener('change', updateDashboard);
    citySelect.addEventListener('change', updateDashboard);

    resetBtn.addEventListener('click', () => {{
      yearSelect.value = 'ALL';
      sectorSelect.value = 'ALL';
      citySelect.value = 'ALL';
      updateDashboard();
    }});

    initMap();
    updateDashboard();
  </script>
</body>
</html>
"""

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("make_charts.py: Generated dashboard.html successfully.")
