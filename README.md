# 🧾 Alto_parsing

**Extract text content and coordinates from ALTO XML files into structured text outputs.**  
Created and maintained by **[Martin Badrous](https://github.com/martinbadrous)**

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Repository Structure](#repository-structure)
- [Quick Setup & Usage (All-in-One)](#quick-setup--usage-all-in-one)
- [Example Output](#example-output)
- [How It Works](#how-it-works)
- [Applications](#applications)
- [Example Workflow](#example-workflow)
- [Requirements](#requirements)
- [Troubleshooting](#troubleshooting)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## Overview

`Alto_parsing` is a lightweight Python utility for **parsing ALTO XML** (a common OCR output format) and exporting either:
- **Bounding boxes** for text elements (`x_min`, `y_min`, `x_max`, `y_max`), or
- **Top-left coordinates** (`x`, `y`)

…alongside the **recognized text**.  
It’s designed for **document analysis**, **layout processing**, **OCR post-processing**, and building datasets for machine learning.

---

## Features

- ✅ Parse ALTO XML files and extract **text + geometry**
- ✅ Two output modes: **bounding-box** or **top-left**
- ✅ Simple `.txt` outputs for easy downstream use
- ✅ Works for single files or folder batches
- ✅ Minimal dependencies and fast execution

---

## Repository Structure

```bash
Alto_parsing/
├── 00023.xml                    # Example ALTO input (trimmed for demos)
├── ALTO_PARSIN_TO_TXT.py        # Batch parser CLI (directory or single file)
├── Alto_to_txt_boundingbox.py   # Thin single-file wrapper around the CLI
├── alto_parser.py               # Shared parsing utilities used by the CLIs
├── bounding_box.txt             # Example bounding-box output for 00023.xml
├── top_left_point_position.txt  # Example top-left output for 00023.xml
├── requirements.txt             # Optional deps (standard library by default)
└── README.md                    # This file
```

---

## Quick Setup & Usage (All-in-One)

💡 Copy and paste all commands below at once in your terminal.  
Works on Linux/macOS; for Windows, use PowerShell and replace `source venv/bin/activate` with `venv\Scripts\activate`.

```bash
# 1. Clone the repository
git clone https://github.com/martinbadrous/Alto_parsing.git
cd Alto_parsing

# 2. (Optional) Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# 3. Install dependencies (safe even if requirements.txt is empty)
pip install -r requirements.txt

# 4. (Optional) Speed up XML parsing
pip install lxml

# 5. Parse a single ALTO file (Bounding Box mode)
python3 Alto_to_txt_boundingbox.py   00023.xml   bounding_box.txt

# 6. Parse a folder of ALTO files (Batch mode)
python3 ALTO_PARSIN_TO_TXT.py   --indir ./scans/alto_xmls   --outdir ./scans/parsed_txts   --mode bounding_box

# 7. View output
head ./scans/parsed_txts/00023.txt
```

---

## Example Output

**Input (`00023.xml`):**
```xml
<String CONTENT="Hello" HPOS="120" VPOS="50" WIDTH="35" HEIGHT="15"/>
<String CONTENT="World" HPOS="170" VPOS="50" WIDTH="45" HEIGHT="15"/>
```

Fields are tab-separated by default (use `--separator` to change this).

**Bounding-box Output:**
```
Hello   120     50      155     65
World   170     50      215     65
```

**Top-left Output:**
```
Hello   120     50
World   170     50
```

---

## How It Works

1. Loads ALTO XML using Python’s `xml.etree.ElementTree` (or `lxml` if available).  
2. Iterates over `<String>`, `<TextLine>`, and `<TextBlock>` tags.  
3. Reads geometry attributes:
   - `HPOS` → x  
   - `VPOS` → y  
   - `WIDTH`, `HEIGHT` → size
4. Computes:
   - **Bounding box:** `(x_min, y_min, x_max, y_max)`
   - **Top-left point:** `(x_min, y_min)`
5. Writes text + coordinates line by line into `.txt` output.

> ALTO schemas can vary — adjust tag or attribute names if necessary.

---

## Applications

- Document layout visualization and analysis  
- Dataset generation for OCR or layout ML models  
- Mapping OCR output to scanned image positions  
- Feature extraction for document understanding  
- Ground-truth alignment and validation tasks  

---

## Example Workflow

```bash
# Parse all ALTO XMLs in a folder (writes ./scans/alto_xmls/parsed by default)
python3 ALTO_PARSIN_TO_TXT.py --indir ./scans/alto_xmls --mode top_left

# Or send the result to a custom directory
python3 ALTO_PARSIN_TO_TXT.py --indir ./scans/alto_xmls --outdir ./outputs --mode bounding_box

# Inspect results
head ./outputs/page_001.txt
```

---

## Requirements

- **Python ≥ 3.7**
- Optional:
  ```bash
  pip install lxml
  ```

---

## Troubleshooting

| Problem | Cause | Fix |
|----------|--------|-----|
| No text extracted | Tag names differ in your ALTO schema | Adjust the script’s XML tag references |
| Coordinates look wrong | Different page unit scaling | Normalize coordinates or check DPI |
| Parsing is slow | Large XML files | Install `lxml` and use batch mode |
| Unicode errors | Encoding mismatch | Run `export PYTHONIOENCODING=utf-8` |

---

## Roadmap

- [ ] Add JSON/CSV output options  
- [ ] Add visualization overlay (draw boxes on page)  
- [ ] Multiprocessing for large batch processing  
- [ ] CLI progress bar and better logging  
- [ ] Automatic ALTO schema detection  

---

## Contributing

Pull requests are welcome!  
If you find a bug or have an idea (e.g. JSON export, visualization), open an **Issue** on GitHub.

**Contribution guide:**
1. Fork this repo  
2. Create a new branch (`feature/new-parser`)  
3. Commit and push your changes  
4. Open a Pull Request 🚀

---

## License

This project is licensed under the **MIT License**.  
See the `LICENSE` file for details.

---

## Author

**Martin Badrous**  
Computer Vision & Robotics Engineer  
📍 Based in France | 🇪🇬 Egyptian origin  
🔗 [GitHub Profile](https://github.com/martinbadrous)

---

⭐ **If this project helps your research or work, please give it a star on GitHub!**
