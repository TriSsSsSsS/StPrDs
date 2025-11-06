# 📈 Stock Prices Dataset - Automated Downloader

Automated stock data downloader for Russell 1000 companies using GitHub Actions. Downloads and updates stock price data every 2 days at 2:00 AM UTC.

## 🚀 Features

- ✅ **Automated Downloads**: Runs every 2 days via GitHub Actions
- 📊 **Russell 1000 Coverage**: Downloads data for 1007 tickers
- 💾 **Efficient Storage**: Compressed CSV files (gzip)
- 🔄 **Incremental Updates**: Appends new data without duplicates
- 📝 **Comprehensive Logging**: Tracks all downloads and errors
- 🤖 **Auto-Commit**: Automatically commits and pushes updated data

## 📁 Project Structure

```
Stock Prices Dataset/
├── .github/
│   └── workflows/
│       └── stock_downloader.yml    # GitHub Actions workflow
├── stock_data/                      # Downloaded stock data (auto-created)
│   ├── AAPL.csv.gz
│   ├── MSFT.csv.gz
│   └── ...
├── stock_downloader.py              # Main Python script
├── Stock_Data_Downloader.ipynb      # Original Jupyter notebook
├── tickers.csv                      # List of tickers
├── requirements.txt                 # Python dependencies
├── download_log.txt                 # Download history log
└── README.md                        # This file
```

## 🛠️ Setup Instructions

### 1. Create GitHub Repository

1. Create a new repository on GitHub
2. Clone this folder to your local machine
3. Initialize Git (if not already done):
   ```bash
   cd "c:\Users\trion\OneDrive\Desktop\Files\Stock Prices Dataset"
   git init
   git add .
   git commit -m "Initial commit: Stock data downloader"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

### 2. Configure GitHub Actions

The workflow is already configured in `.github/workflows/stock_downloader.yml`. It will:
- Run automatically every 2 days at 2:00 AM UTC
- Download stock data for the past 3 days
- Commit and push changes automatically

**No additional configuration needed!** GitHub Actions will use the built-in `GITHUB_TOKEN` for authentication.

### 3. Enable GitHub Actions

1. Go to your repository on GitHub
2. Click on the **Actions** tab
3. Enable workflows if prompted
4. The workflow will run automatically based on the schedule

### 4. Manual Trigger (Optional)

You can also trigger the workflow manually:
1. Go to **Actions** tab
2. Click on **Stock Data Downloader** workflow
3. Click **Run workflow** button

## 📅 Schedule

- **Frequency**: Every 2 days
- **Time**: 2:00 AM UTC (adjust in workflow file if needed)
- **Cron Expression**: `0 2 */2 * *`

To change the schedule, edit `.github/workflows/stock_downloader.yml`:
```yaml
schedule:
  - cron: '0 2 */2 * *'  # Modify this line
```

### Common Cron Examples:
- Every day at 2 AM: `0 2 * * *`
- Every 3 days at 2 AM: `0 2 */3 * *`
- Every Monday at 2 AM: `0 2 * * 1`
- Twice daily (2 AM & 2 PM): `0 2,14 * * *`

## 🔧 Local Testing

To test the script locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the downloader
python stock_downloader.py
```

## 📊 Data Format

Each ticker's data is saved as a compressed CSV file with the following columns:
- `Datetime`: Timestamp of the data point
- `Open`: Opening price
- `High`: Highest price in the interval
- `Low`: Lowest price in the interval
- `Close`: Closing price
- `Volume`: Trading volume
- `Ticker`: Stock ticker symbol

**Interval**: 30 minutes  
**Compression**: gzip  
**File naming**: `{TICKER}.csv.gz` (e.g., `AAPL.csv.gz`)

## 📝 Logs

- **download_log.txt**: Contains detailed logs of all download operations
- **GitHub Actions Artifacts**: Each run uploads the log as an artifact (30-day retention)

## 🔍 Monitoring

### Check Workflow Status
1. Go to **Actions** tab in your GitHub repository
2. View the latest runs of **Stock Data Downloader**
3. Click on a run to see detailed logs

### View Summary
Each workflow run creates a summary showing:
- Run date and time
- Number of files downloaded
- Recent log entries
- File statistics

## 🐛 Troubleshooting

### Workflow Not Running
- Check if GitHub Actions is enabled in repository settings
- Verify the cron schedule is correct
- Check repository activity (workflows may pause for inactive repos)

### Download Failures
- Check `download_log.txt` for specific errors
- Some tickers may be delisted or unavailable
- Yahoo Finance API may have rate limits

### Permission Issues
- Ensure the workflow has write permissions
- Go to Settings → Actions → General → Workflow permissions
- Select "Read and write permissions"

## 📦 Dependencies

- **yfinance**: Yahoo Finance data downloader
- **pandas**: Data manipulation
- **requests**: HTTP library

See `requirements.txt` for specific versions.

## 🎯 Customization

### Change Download Period
Edit `stock_downloader.py`:
```python
# Default: Downloads last 3 days (from 2 days ago to today)
start_date = end_date - timedelta(days=2)

# Change to download last 7 days:
start_date = end_date - timedelta(days=6)
```

### Change Data Interval
Edit `stock_downloader.py`:
```python
# Default: 30-minute intervals
interval="30m"

# Options: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
interval="1h"  # Hourly data
```

### Add/Remove Tickers
Edit the `ALL_TICKERS` list in `stock_downloader.py` or modify `tickers.csv`.

## 📈 Data Usage Examples

### Load a Ticker
```python
import pandas as pd

# Load Apple stock data
df = pd.read_csv('stock_data/AAPL.csv.gz', compression='gzip', parse_dates=['Datetime'])
print(df.head())
```

### Analyze Multiple Tickers
```python
from pathlib import Path
import pandas as pd

data_dir = Path('stock_data')
all_data = []

for file in data_dir.glob('*.csv.gz'):
    df = pd.read_csv(file, compression='gzip', parse_dates=['Datetime'])
    all_data.append(df)

combined_df = pd.concat(all_data, ignore_index=True)
print(f"Total records: {len(combined_df)}")
```

## 🤝 Contributing

Feel free to open issues or submit pull requests for improvements!

## 📄 License

This project is open source and available for educational purposes.

## ⚠️ Disclaimer

This data is provided for informational purposes only. Always verify data accuracy before making financial decisions.

---

**Last Updated**: November 2025  
**Maintained by**: Automated GitHub Actions Workflow
