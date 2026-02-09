# Best-Worst Scaling (aka MaxDiff) Tools - Streamlit GUI

A user-friendly web interface for the best-worst scaling (aka MaxDiff) (aka MaxDiff) tools originally created by Dr. Geoff Hollis.

![Best-Worst Tools](https://img.shields.io/badge/Python-3.6+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)
![License](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-green.svg)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [User Guide](#user-guide)
- [Screenshots](#screenshots)
- [Troubleshooting](#troubleshooting)
- [About](#about)
- [License](#license)

---

## 🎯 Overview

This is a **graphical web interface** for the best-worst scaling (aka MaxDiff) (aka MaxDiff) tools, making them accessible to researchers who may not be comfortable with command-line interfaces.

**What is Best-Worst Scaling?**
Best-worst scaling is a research methodology for measuring subjective dimensions (preferences, perceptions, etc.) across items. Participants view K items at a time and select the "best" and "worst" according to the dimension of interest.

**Original Tools:** Created by Dr. Geoff Hollis(University of Alberta)  
**GUI Development:** Parastoo Harati (p.harati@ualberta.ca)  
**Date:** December 2023

---

## ✨ Features

### 🎲 Create Trials
- **Upload** your list of items (words, images, etc.)
- **Configure** trial parameters (number of trials, items per trial)
- **Generate** optimally balanced trial sets
- **Download** as CSV ready for your experiment

### 📈 Score Data
- **Upload** participant response files
- **Select** from 12 different scoring methods
- **Calculate** latent item scores instantly
- **Download** results as CSV

### 🖥️ User Interface
- Clean, modern web interface
- **Flexible Inputs**: Support for plain text, CSV, and TSV formats
- **Smart Column Detection**: Automatically detects and lets you pick item columns
- Drag-and-drop file upload
- Real-time parameter validation
- Instant previews and downloads
- No coding required!

### 🧪 Scientific Validation
- **Proven Accuracy**: Built on Dr. Geoff Hollis's peer-reviewed simulation engine
- **Noise Robustness**: Optimized for "noisy" real-world crowdsourced data
- **Validated Methods**: 12 scoring algorithms tested against simulated "truth"

---

## 🚀 Installation

### Prerequisites

- **Python 3.6 or higher** installed on your system
- **pip** (Python package installer)

### Step-by-Step Installation

#### 1. Open Terminal/Command Prompt

**On Linux/Mac:**
- Press `Ctrl + Alt + T`

**On Windows:**
- Press `Win + R`, type `cmd`, press Enter

#### 2. Navigate to this directory

```bash
cd /path/to/bestworst_tools_streamlit
```

For example:
```bash
cd /media/parastoo/0EFE0F0B0EFE0F0B/Experiments_UofA/Experiments/bestworst_tools_Hollis_original/bestworst_tools_streamlit
```

#### 3. Install Streamlit

```bash
pip3 install -r requirements.txt
```

Or install directly:
```bash
pip3 install streamlit
```

**That's it!** You're ready to use the GUI.

---

## ⚡ Quick Start

### Running the App

1. **Open Terminal** in the `bestworst_tools_streamlit` directory

2. **Run this command:**
   ```bash
   streamlit run app.py
   ```

3. **Your browser will automatically open** to `http://localhost:8501`
   - If it doesn't, manually open your browser and go to that URL

4. **Start using the tools!**
   - Select "Create Trials" or "Score Data" from the sidebar
   - Follow the on-screen instructions

### Stopping the App

- Press `Ctrl + C` in the terminal where the app is running

---

## 📖 User Guide

### Creating Trials

**Step 1: Prepare Your Items**
Create a file with your items. Three formats supported:
- **Plain text (.txt)**: One item per line
  ```
  happiness
  sadness
  anger
  fear
  ```
- **CSV (.csv)**: Items in any column
- **TSV (.tsv)**: Tab-separated values

**Step 2: Upload and Configure**
1. Click "Create Trials" in the sidebar
2. Upload your items file
3. Set parameters:
   - **N (trials)**: How many trials to generate (default: items × 8)
   - **K (items per trial)**: Items shown per trial (recommended: 4)
   - **Generator**: Use "norepeateven" (recommended)

**Step 3: Generate and Download**
1. Click "Generate Trials"
2. Preview the results
3. Click "Download Trials CSV"

**Step 4: Use in Your Experiment**
- Upload the CSV to your experiment platform (Qualtrics, Gorilla, etc.)
- Show participants K items per trial
- Collect their "best" and "worst" choices

---

### Scoring Data

**Step 1: Collect Data**
Your participant data files should be CSV format with these columns:
- `best`: Item chosen as best
- `worst`: Item chosen as worst  
- `option1`, `option2`, `option3`, ... : All items shown
- (Other columns like participant ID are okay and will be ignored)

**Example:**
```csv
participant,best,worst,option1,option2,option3,option4
P001,happiness,anger,happiness,sadness,anger,fear
P001,fear,sadness,joy,fear,sadness,surprise
...
```

**Step 2: Upload Files**
1. Click "Score Data" in the sidebar
2. Upload one or more participant data files
3. Verify column names (default: "best" and "worst")

**Step 3: Select Scoring Methods**
Choose one or more methods:
- **Value** (recommended): Robust tournament-based scoring
- **Best/Worst/BestWorst**: Simple count-based methods
- **Elo**: Chess-style rating system
- **RW**: Rescorla-Wagner learning model
- And more...

**Step 4: Calculate and Download**
1. Click "Calculate Scores"
2. Preview the results
3. Click "Download Scores CSV"

---

## 📸 Screenshots

### Home Page
The home page provides an overview and quick access to both tools.

### Create Trials
- Upload items, configure parameters, generate trials
- Real-time validation ensures parameters are correct
- Preview trials before downloading

### Score Data
- Upload multiple participant files at once
- Select from 12 scoring methods
- Get instant results

---

## 🔧 Troubleshooting

### App won't start

**Problem:** `streamlit: command not found`

**Solution:** Streamlit not installed. Run:
```bash
pip3 install streamlit
```

---

**Problem:** `ModuleNotFoundError: No module named 'streamlit'`

**Solution:** Install streamlit in the correct Python environment:
```bash
python3 -m pip install streamlit
```

---

### Files won't upload

**Problem:** "Error: Invalid file format"

**Solution:** Ensure your file is:
- Plain text (.txt) with one item per line, OR
- CSV (.csv) or TSV (.tsv) with properly formatted columns

---

### Trial generation fails

**Problem:** "Exception: For an even design, trials * K MOD items must equal 0"

**Solution:** When using "norepeateven" or "even" generator:
- N × K must be evenly divisible by the number of items
- Try suggested N values shown in the warning message
- Or use "random" generator (less optimal distribution)

**Example:**
- 1,046 items × 4 items per trial = 4,184 presentations
- Valid N values: 1046, 2092, 3138, 4184, 8368, etc.
- These all divide evenly: (N × 4) ÷ 1046 = whole number

---

### Scoring produces errors

**Problem:** "No valid trials found"

**Solution:** Check that your CSV files have:
- Columns named "best" and "worst" (or customize the names)
- Option columns like "option1", "option2", etc.
- Actual data (not just headers)

---

### Browser doesn't open automatically

**Solution:** Manually open your browser and navigate to:
```
http://localhost:8501
```

---

### Port already in use

**Problem:** `Address already in use`

**Solution:** Stop the existing Streamlit process or use a different port:
```bash
streamlit run app.py --server.port 8502
```

---

## 📚 About

### Original Author
**Dr. Geoff Hollis**   
University of Alberta  

### Citation
When using these tools in published research, please cite:

> Hollis, G. (2017). Scoring best/worst data in unbalanced, many-item designs, with applications to crowdsourcing semantic judgments. *Behavior Research Methods*, XX(X), 1-19. doi: 10.3758/s13428-017-0898-2

### Python 3 Migration & GUI
**Parastoo Harati**  
p.harati@ualberta.ca  
University of Alberta  
December 2023

---

## 📄 License

This software is released under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)** license.

https://creativecommons.org/licenses/by-nc-sa/4.0/

You are free to:
- **Share** — copy and redistribute the material
- **Adapt** — remix, transform, and build upon the material

Under the following terms:
- **Attribution** — You must give appropriate credit
- **NonCommercial** — You may not use the material for commercial purposes
- **ShareAlike** — If you remix, transform, or build upon the material, you must distribute your contributions under the same license

---

## 🙏 Acknowledgments

We honor the memory of **Dr. Geoff Hollis**, whose innovative work on best-worst scaling (aka MaxDiff) methodologies has been invaluable to the research community. This graphical interface aims to make his tools accessible to researchers worldwide, including those who may not be comfortable with command-line interfaces.


---

## 📞 Support

### For questions about:

**This GUI or Python 3 version:**
- Contact: Parastoo Harati
- Email: p.harati@ualberta.ca

**Original methodology:**
- See the published paper (citation above)

---

## 🗂️ File Structure

```
bestworst_tools_streamlit/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── QUICK_START.txt        # Quick reference guide
```

---

## 🔗 Related Files

This GUI uses the Python 3 scripts from:
- `../bestworst_tools_python3/scripts/`

For command-line usage, see:
- `../bestworst_tools_python3/README.txt`

---

**Happy researching! 🎉**
