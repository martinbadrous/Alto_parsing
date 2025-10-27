# 🧾 Alto_parsing

**Extract content and coordinates from ALTO XML into simple text outputs.**  
Created and maintained by **[Martin Badrous](https://github.com/martinbadrous)**

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Repository Structure](#repository-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Examples](#examples)
- [How It Works](#how-it-works)
- [Troubleshooting](#troubleshooting)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## Overview

`Alto_parsing` is a lightweight Python utility for **parsing ALTO XML** (a common OCR output format) and exporting either:
- **Bounding boxes** for text elements (x_min, y_min, x_max, y_max), or
- **Top-left coordinates** (x, y)

…alongside the **recognized text**. It’s handy for **document analysis, layout processing, OCR post-processing**, and building datasets for ML.

---

## Features

- ✅ Parse ALTO files to extract **text** + **geometry**
- ✅ Two output modes: **bounding-box** or **top-left**
- ✅ Simple `.txt` outputs for easy downstream use
- ✅ Minimal dependencies; runs on standard Python
- ✅ Works for single files or batch folders

---

## Repository Structure

```bash
Alto_parsing/
├── ALTO_PARSIN_TO_TXT/                # Sample data & demo outputs (you can replace with your own)
│   ├── 00023.xml                      # Example ALTO input
│   ├── bounding_box.txt               # Example output (bounding-box mode)
│   └── top_left_point_position.txt    # Example output (top-left mode)
│
├── ALTO_PARSIN_TO_TXT.py              # Batch parser (folder in → folder out)
├── Alto_to_txt_boundingbox.py         # Single-file parser (bounding-box out)
│
├── requirements.txt                   # Optional deps (can be empty if stdlib only)
└── README.md                          # This file
