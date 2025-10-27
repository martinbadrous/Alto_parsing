# Alto_parsing  
**Extracting content coordinates from ALTO XML files → structured text output**

## Martin Badrous  
Computer Vision & Image Processing Engineer  
GitHub: [martinbadrous/Alto_parsing](https://github.com/martinbadrous/Alto_parsing)

---

## 📌 Overview  
This repository provides a lightweight Python utility to parse ALTO XML files (often used in OCR/text-layout tasks) and extract the coordinates of content elements (text blocks, words, lines) into plain text files (with bounding box information).  
It is designed for quick experiments or preprocessing pipelines where you need spatial location of textual elements.

---

## 🧰 Features  
- Parse ALTO XML files to retrieve text elements + their bounding-boxes.  
- Export results into simple `.txt` files (e.g., one element per line: *text | x-min y-min x-max y-max*).  
- Supports two modes:  
  - **Bounding-box mode** → full extents of each element.  
  - **Top-left point mode** → only the top-left corner, for simpler downstream usage.  
- Minimal dependencies → easy to incorporate into larger pipelines.

---

## 🗂 Repository Structure  
