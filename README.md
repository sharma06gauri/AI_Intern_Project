# AI_Intern_Project
# AI Engineer Intern – Take Home Problem

## 📌 Project Overview
This project is a **Proof of Concept (POC)** that enables a CXO to enter natural language queries and retrieve accurate results from a rental application database by translating **NL → SQL**.

## 🚀 Features
- NL queries mapped to SQL and executed
- Supports joins, aggregations, and conditions
- Plain-text results for demo
- Graceful fallback: “Sorry, unable to answer at this point in time.”

## 🛠 Tech Stack
- Python
- SQLite3, Pandas (for testing), Regex/NLP utilities
- CLI interface

## 📂 Repository Structure
```
AI_Intern_Project/
│── app.py
│── config/
│── data/
│── requirements.txt
│── README.md
│── report.pdf
```
> Update paths/names as per your repo.

## ⚙️ Setup
```bash
pip install -r requirements.txt
python3 app.py
```

## ✅ Sample Queries
- What’s the occupancy rate of properties in Bradford last quarter?
- Who are the top 10 tenants by total rent paid?
- What’s the average rating of apartments vs houses?
- Which landlords generated the most revenue this year?
- List all currently available 2BHKs under $2500 in London.

## 📊 Results
See **report.pdf** for screenshots and results.

## 🏁 Conclusion
This POC demonstrates NL→SQL for the `rental_app` database and can be extended with advanced NLP and visualizations.
