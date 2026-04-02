# ⚡ Quick Start Guide

Get the Medical Data Analysis web app running in 2 minutes!

## 📦 Prerequisites

- Python 3.8 or higher installed
- The required CSV files (ADMISSIONS.csv and D_LABITEMS.csv)

## 🚀 Installation & Running

### Step 1: Install Dependencies
```bash
cd Disease_Progression_Prediction
pip install -r requirements.txt
```

**Expected time**: 1-2 minutes

### Step 2: Run the Application
```bash
python run.py
```

The Flask app will start on `http://127.0.0.1:5000`

A browser window should open automatically. If not, manually visit the URL above.

**Expected time**: <1 minute

## 🎯 Quick Navigation

### Home Page
- Overview of the project
- Links to data exploration pages
- Project status

### Admissions Data
- View hospital admission records
- See summary statistics
- Browse records with pagination

### Lab Items Data  
- View laboratory tests
- See unique items and metadata
- Browse lab items with pagination

## 💡 Tips

- Use pagination controls to browse large datasets
- Dataset summaries show total records, unique values, and memory usage
- Tables are sortable by clicking column headers
- All data is read-only (no modifications)

## 🛑 Stopping the Application

Press `Ctrl+C` in the terminal to stop the Flask server.

## 📝 Troubleshooting

### "Module not found" error
Make sure you installed requirements:
```bash
pip install -r requirements.txt
```

### "Port already in use" error
The default port 5000 is in use. Edit `config.py` to change FLASK_PORT.

### CSV files not found
Ensure ADMISSIONS.csv and D_LABITEMS.csv are in the project root directory.

---

**That's it!** Your medical data analysis dashboard is now running. 🎉
    print(f"  {rec}")
```

Run it:
```bash
python test_prediction.py
```

## 📊 Output Files Location

After running, check:

```
Disease_Progression_Prediction/
├── models/
│   ├── lstm_final.h5              ← Trained LSTM model
│   ├── gru_final.h5               ← Trained GRU model
│   ├── transformer_final.h5       ← Trained Transformer model
│   ├── training_summary.json      ← Model metrics
│   └── pipeline_config.json       ← Config used
│
└── analysis/
    ├── training_history.png       ← Training curves
    ├── confusion_matrices.png     ← Model accuracy
    ├── model_comparison.png       ← Performance comparison
    ├── prediction_confidence.png  ← Confidence distribution
    ├── timeseries_examples.png    ← Sample sequences
    ├── stage_distribution.png     ← Data distribution
    └── analysis_report.txt        ← Summary report
```

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'tensorflow'"
**Solution:**
```bash
pip install --upgrade tensorflow
```

### Issue: "No data found for patient"
**Solution:** Patient doesn't have lab events in the dataset. Try another patient ID:
```python
# List available patients
from data_processor import DiseaseProgressionDataProcessor
processor = DiseaseProgressionDataProcessor(data_folder)
processor.load_raw_data()
print(processor.patients['subject_id'].head(20))
```

### Issue: "CUDA out of memory"
**Solution:** The GPU doesn't have enough memory. Use CPU:
```bash
# On Windows PowerShell
$env:CUDA_VISIBLE_DEVICES = "-1"
python pipeline.py
```

### Issue: Training is very slow
**Solution:** Use a smaller dataset:
```python
# Modify data_processor.py, line ~120:
unique_patients = self.labevents['subject_id'].unique()[:50]  # Instead of [:100]
```

## 📚 Understanding the Output

### Training History Plot
- **X-axis**: Training epoch (1-50)
- **Y-axis**: Loss or Accuracy
- Good sign: Both training and validation loss decrease together

### Confusion Matrix
- **Diagonal** (bright): Correct predictions
- **Off-diagonal** (dark): Misclassifications
- Better = darker diagonal

### Model Comparison
- Shows accuracy, loss, precision, recall
- Choose model with highest accuracy
- LSTM usually wins

## 🔄 Retraining & Customization

### Train for more epochs:
```python
from pipeline import CompleteDiseasePredictionPipeline
pipeline = CompleteDiseasePredictionPipeline(data_folder)
results, _, _ = pipeline.run_complete_pipeline(epochs=100)  # More epochs
```

### Use only specific model:
```python
from train import ModelTrainer
trainer = ModelTrainer(data_folder)
data = trainer.prepare_data()
model, history = trainer.train_model('lstm', data)  # Only LSTM
```

## 📖 Next Steps

1. **Review Results**: Check the analysis plots and reports
2. **Integration**: Connect to Hospital_Readmission_Prediction app
3. **Validation**: Test on your own patient data
4. **Deployment**: Deploy models to production

## 🎓 Learning Resources

- Read `data_processor.py` to understand data processing
- Study `models.py` to see LSTM/GRU/Transformer code
- Check `analysis.py` for visualization techniques
- Review predictions in `predict.py`

## 💡 Tips for Best Results

1. **More data** = Better models
2. **Longer sequences** (60+ steps) = Better long-term patterns
3. **Ensemble method** = More robust predictions
4. **Cross-validation** = Realistic performance estimates
5. **External validation** = Proof it works on new hospitals

## 🚀 Performance Benchmarks

| Component | Time | Memory |
|-----------|------|--------|
| Data loading | ~2 sec | 500MB |
| Sequence creation | ~5 sec | 200MB |
| LSTM training | ~120 sec | 2GB |
| GRU training | ~90 sec | 1.8GB |
| Transformer training | ~150 sec | 2.2GB |
| Single prediction | <10ms | 100MB |

## ✅ Checklist

- [ ] Dependencies installed successfully
- [ ] Pipeline ran without errors
- [ ] Models saved in `models/` folder
- [ ] Plots generated in `analysis/` folder
- [ ] Test prediction works
- [ ] Ready for integration!

---

**Happy predicting! 🎯**
