# Medical Data Analysis - Simplified Project

A lightweight web application for exploring and analyzing medical data from two CSV files.

## 📊 What's Included

- **ADMISSIONS.csv**: Hospital admission records with patient demographics and outcomes
- **D_LABITEMS.csv**: Laboratory test items with descriptions and categories

## 🚀 Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   python run.py
   ```

3. **Open in browser**:
   Visit `http://127.0.0.1:5000`

## 📁 Project Structure

```
Disease_Progression_Prediction/
├── app.py                 # Flask web application
├── run.py                 # Application launcher
├── data_processor.py      # Data loading and analysis
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── ADMISSIONS.csv         # Hospital admission data
├── D_LABITEMS.csv         # Lab items data
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── admissions.html   # Admissions data viewer
│   └── labitems.html     # Lab items viewer
└── static/               # CSS and JS files
    ├── css/
    └── js/
```

## 🎯 Features

- ✅ Simple data exploration interface
- ✅ Dataset statistics and summaries
- ✅ Paginated data browsing
- ✅ Lightweight and responsive design
- ✅ No complex ML dependencies

## 📦 Dependencies

- Flask 2.3.3
- Pandas 2.1.4
- NumPy 1.26.4
- Matplotlib 3.8.2
- Seaborn 0.13.0

## 💻 Usage

### View ADMISSIONS Data
1. Navigate to "Admissions" in the menu
2. See summary statistics (total records, unique patients, memory usage)
3. Browse records with pagination

### View LAB ITEMS Data
1. Navigate to "Lab Items" in the menu
2. See item statistics (total items, unique IDs, memory usage)
3. Browse laboratory test items with pagination

## 🛠️ Customization

Edit `config.py` to customize:
- Maximum rows displayed per page
- Flask host and port
- Data file paths

## 📝 License

MIT License