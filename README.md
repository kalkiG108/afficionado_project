# ☕ Afficionado Coffee Roasters — Sales Trend & Time-Based Performance Analysis

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

**A complete time-based sales analytics project uncovering when demand occurs at Afficionado Coffee Roasters — enabling data-driven staffing, scheduling, and operational decisions.**

[🚀 Live Dashboard](https://afficionadocoffee-analysis.streamlit.app) · [📄 Research Paper](#deliverables) · [📊 Dataset](https://docs.google.com/spreadsheets/d/14CqwUgV3M37tz0ymk_utin29aDAKtdJA)

</div>

---

## 📌 Project Overview

Specialty coffee retail is highly time-sensitive. Poor understanding of *when* customers arrive leads to:
- Overstaffing during slow hours
- Understaffing during rush periods  
- Inconsistent customer experience
- Inefficient operational costs

This project analyses **149,116 transactions** from **3 NYC store locations** across fiscal year 2025 to deliver quantitative, evidence-based answers to these operational questions.

---

## 🔑 Key Findings at a Glance

| Metric | Finding |
|---|---|
| 💰 Total Revenue | **$698,812.33** |
| 📈 Avg Weekly Revenue | **$13,438.70** |
| ⏰ Peak Hour | **10:00 AM** (18,545 transactions) |
| 📅 Busiest Day | **Wednesday** |
| 📅 Slowest Day | **Monday** |
| 🌅 Top Time Bucket | **Morning 6–11 AM** (54.8% of all transactions) |
| 🏪 Top Store by Revenue | **Hell's Kitchen** ($236,511) |
| 💵 Highest Avg Txn Value | **Lower Manhattan** ($4.81/txn) |

---

## 🏗️ Project Structure

```
afficionado_project/
│
├── data/
│   ├── coffee_sales.csv          # Raw dataset
│   └── coffee_sales_clean.csv    # Cleaned + feature-engineered dataset
│
├── charts/                       # Auto-generated Plotly HTML charts
│   ├── chart1_weekly_trend.html
│   ├── chart2_day_of_week.html
│   ├── chart3_weekday_vs_weekend.html
│   ├── chart4_hourly_demand.html
│   ├── chart5_heatmap_store_hour.html
│   ├── chart6_bucket_by_store.html
│   └── chart7_weekly_by_store.html
│
├── analysis.ipynb                # Phase 1 + Phase 2: EDA & Visualizations
├── app.py                        # Phase 3: Streamlit Dashboard
└── requirements.txt              # Python dependencies
```

---

## 📊 Dashboard Features

The interactive Streamlit dashboard is organized into **4 tabs** with **5 live KPI cards**:

### Sidebar Filters
- 🏪 **Store Location** — filter by Hell's Kitchen, Astoria, Lower Manhattan
- 📅 **Day of Week** — select specific days
- 🕐 **Hour Range** — slider from 6:00 to 20:00
- 📊 **Metric Toggle** — switch between Revenue ($) and Transaction Count

### Tab 1 — 📈 Sales Trend
- Weekly revenue line chart with linear trendline
- Per-store weekly revenue comparison

### Tab 2 — 📅 Day of Week
- Average revenue/transactions by day of week
- Weekday vs Weekend side-by-side comparison

### Tab 3 — 🕐 Hourly Demand
- Dual-axis hourly curve (transactions + revenue)
- Time bucket breakdown with percentage bars

### Tab 4 — 🏪 Location Comparison
- Per-store KPI cards
- Store × Hour transaction heatmap
- Time bucket distribution by store

---

## 🔬 Analytical Methodology

### Phase 1 — Data Ingestion & Feature Engineering
```
✓ Loaded 149,116 rows × 11 columns
✓ Validated: 0 nulls · 0 duplicates · 0 invalid prices/quantities
✓ Engineered: revenue · hour · day_of_week · week_number · time_bucket · is_weekend
```

### Phase 2 — Exploratory Data Analysis
7 Plotly charts covering weekly trend, day-of-week performance, hourly demand curve, store-hour heatmap, time bucket breakdown, and cross-location comparison.

### Phase 3 — Streamlit Dashboard
Interactive web application with real-time filters, KPI cards, and all analytical charts.

---

## 📈 Analytical Charts

| # | Chart | Insight |
|---|---|---|
| 1 | Weekly Sales Trend | Stable revenue, modest upward trend, Week 52 peak |
| 2 | Day-of-Week Performance | Wednesday peak, Monday trough |
| 3 | Weekday vs Weekend | Weekdays account for 71.5% of transactions |
| 4 | Hourly Demand Curve | 10 AM peak — mid-morning break pattern |
| 5 | Store × Hour Heatmap | All 3 stores peak at identical hours |
| 6 | Time Bucket by Store | Morning dominates uniformly across locations |
| 7 | Weekly Trend by Store | Parallel revenue trajectories, Hell's Kitchen leads |

---

## 🚀 Running Locally

### 1. Clone the repository
```bash
git clone https://github.com/kalkiG108/afficionado_project.git
cd afficionado_project
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the notebook (Phase 1 + 2)
```bash
jupyter notebook analysis.ipynb
```
> Run all cells top to bottom. This generates `data/coffee_sales_clean.csv` and all 7 charts in `charts/`.

### 4. Launch the dashboard (Phase 3)
```bash
streamlit run app.py
```
> Opens at `http://localhost:8501`

---

## 📦 Requirements

```
pandas
numpy
plotly
streamlit
```

---

## 🏪 Store Locations

| Store | City Area | Transactions | Revenue | Avg Txn |
|---|---|---|---|---|
| Hell's Kitchen | Midtown West, NYC | 50,735 | $236,511 | $4.66 |
| Astoria | Queens, NYC | 50,599 | $232,244 | $4.59 |
| Lower Manhattan | Financial District, NYC | 47,782 | $230,057 | $4.81 |

---

## 📋 Dataset Description

| Column | Description |
|---|---|
| `transaction_id` | Unique identifier (1–149,456, sequential) |
| `year` | Transaction year (all 2025) |
| `transaction_time` | Time of transaction (HH:MM:SS, range 06:00–20:59) |
| `transaction_qty` | Units purchased |
| `unit_price` | Price per unit (USD) |
| `store_id` | Store identifier |
| `store_location` | Physical store name |
| `product_id` | Product identifier |
| `product_category` | Coffee, Tea, Bakery, Drinking Chocolate, etc. |
| `product_type` | Product variant |
| `product_detail` | Flavor, blend, size detail |

---

## 💡 Operational Recommendations

1. **Staff 9–11 AM heavily** — the 10 AM peak demands maximum floor coverage
2. **Wednesday is the busiest day** — schedule senior staff accordingly  
3. **Use Mondays for operations** — lowest traffic day, ideal for training & maintenance
4. **Review evening hours** — 17–21 PM = only 15.4% of transactions; may not justify full staffing
5. **Lower Manhattan upsell opportunity** — highest avg txn value; premium product placement advised
6. **Plan for Week 52** — holiday peak; pre-order inventory and seasonal menu items

---

## 📁 Deliverables

| Deliverable | Description |
|---|---|
| 📓 `analysis.ipynb` | Full EDA notebook with validation, feature engineering, and 7 charts |
| 🖥️ `app.py` | Interactive Streamlit dashboard |
| 📄 Research Paper | Comprehensive academic write-up (Word document) |
| 🌐 Live Dashboard | [afficionadocoffee-analysis.streamlit.app](https://afficionadocoffee-analysis.streamlit.app) |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| **Python 3.10+** | Core language |
| **Pandas** | Data loading, cleaning, feature engineering |
| **NumPy** | Numerical operations, trendline fitting |
| **Plotly** | Interactive charts and heatmaps |
| **Streamlit** | Web dashboard framework |
| **Jupyter Notebook** | EDA environment |

---

## 📜 License

This project was developed as part of the **Unified Mentor Data Analytics Internship Program**.  
Dataset © Afficionado Coffee Roasters / Unified Mentor.

---

<div align="center">
Made with ☕ and Python
</div>
