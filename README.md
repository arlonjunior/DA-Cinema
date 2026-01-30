# DA: Cinema Analytics Dashboard: State of the Art
## Overview
#### Course: Domain Application
CineSense Analysis is a Streamlit app that lets users explore cinema data using plain language instead of complex queries. 
It converts natural questions into structured searches, making insights faster and easier to access. 
The system is built from modular Python files and uses RapidFuzz’s  to safely and accurately match names and locations during natural language search.

## Project Structure
```
CineSense Analysis/
├── main.py                                 # Entry point for app navigation
├── eda.py                                  # Exploratory data analysis functions & layout
├── cinema_performance.py                   # Cinema & city performance analytics
├── genre_trends.py                         # Genre and film trend visualizations
├── forecast.py                             # Revenue forcasting using ML/time series
├── recommender.py                          # Strategy or movie recommendation engine
├── utils.py                                # Reads, cleans, preprocesses raw data
├── nls_utils.py                            # Helper using Rapidfuzz

├── Data/
│   └── dataset_cinema_sense.csv            # The main dataset (or multiple region-wise)

├── .streamlit/
│   └── config.toml                         # App them ing (color, font, etc)

├── requirements.txt                        # All necessary Python packages
├── README.md                               # Project description and setup guide
```

## Running Instructions
The development of the Streamlit-based application involved the combination of 8 modular Python files, 
where each one of them has a specific layer of responsibility in the functionality of the web application.

### A. User-facing dashboard 
| Module                    | File                  | Role                                             |
|---------------------------|-----------------------|--------------------------------------------------|
| Executive Summary         | eda.py                | Shows key KPIs and revenue trends.               |
| Cinema & City Performance | cinema_performance.py | Ranks cinemas and city attendance.               |
| Genre and Film Trends     | genre_trends.py       | Analyses genre revenue and popularity.           |
| Forecasting               | forecast.py           | Predicts future revenue.                         |
| Strategy Recommendations  | recommender.py        | Suggests actions based on film and actor impact. |

### B. Helper modules 
| Module                     | File         | Role                                                  |
|----------------------------|--------------|-------------------------------------------------------|
| Entry Point                | main.py      | Starts the app and handles user flow.                 |
| Data Ingestion & Cleansing | utils.py     | Loads and cleans the dataset.                         |
| NLS Helper                 | nls_utils.py | Supports fuzzy matching for natural language queries. |

#### 1. Install Dependencies in terminal
```bash
pip install -r requirements.txt
```
#### 2. Perform Data Ingestion & Cleaning script
- Run `utils.py` to load and cleanse data to be used.

#### 3. Perform NLS Helper script
- Run `nls_utils.py` to support fuzzy matching for natural language queries.

#### 4. Perform User-facing dashboard scripts in order 
- Run `eda.py` to show key KPIs and revenue trends.
- Run `cinema_performance.py` to rank cinemas and city attendance. 
- Run `genre_trends.py` to analyse genre revenue and popularity.
- Run `forecast.py` to predict future revenue.
- Run `recommender.py` to suggest actions based on film and actor impact.

### 5. Run the entry point in Python terminal
Run `main.py` to start the app and handles user flow with the below script.
```bash
streamlit run main.py    
```

## Technologies Used
| Component                      | Technology Used            |
|--------------------------------|----------------------------|
| Storage                        | Local machine              |
| Programming Languages          | Streamlit, Python          |
| IDE                            | PyCharm (CE)               |
| Database/Data Export (Dataset) | CSV file via local machine |

## Author
Arlon Junior