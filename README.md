# Customer Churn Analysis

An end-to-end data and machine learning project that identifies customers at risk of churning and surfaces actionable retention insights. The pipeline runs from raw data ingestion in SQL Server, through exploratory analysis in Power BI and Python, into a compared and tuned set of classification models, and finally out through a live Streamlit dashboard that any business user can operate.

The dataset comes from a telecom context, but nothing in this architecture is domain-specific. Swap the CSV for banking transactions, SaaS usage logs, or e-commerce purchase histories and the same pipeline runs.

<br>

## What This Project Does

Takes raw customer data and answers two questions: who has already churned and why, and which new customers are likely to churn next. The first question is answered through Power BI. The second is answered through a tuned XGBoost model deployed in a Streamlit app called ChurnRadar.

At the historical analysis level, 6,418 customers were analyzed with an overall churn rate sitting at 27% (28.8% when measured against the 6,007 labeled historical records alone). On the prediction side, the deployed model flags 377 of 411 new joiners as at-risk — worth an estimated ₹43,772 in revenue — giving the retention team a ranked, actionable contact list before those customers actually leave.

The source data is the [Telecom Customer Churn Dataset](https://www.kaggle.com/datasets/nguyenduongthanhthuy/telecom-churn-dataset/data) on Kaggle: 32 columns and 6,418 rows, split into 6,007 labeled historical records (`Customer_Status` ∈ {Churned, Stayed}) used for training/EDA, and 411 unlabeled `Joined` records used as the live prediction target.

<br>

## Dashboard

**Summary Page** — KPIs, demographic breakdown, service usage analysis, geographic churn rates, and churn category distribution.

![Summary Dashboard](Power%20BI%20Dashboard%20Screenshots/Summary%20Page.jpg)

**Prediction Page** — predicted churner profiles with a scrollable at-risk customer table showing individual revenue, charges, and referral data.

![Prediction Dashboard](Power%20BI%20Dashboard%20Screenshots/Predictions%20Page.jpg)

<br>

## Key Numbers

| Metric | Value |
|---|---|
| Total Customers | 6,418 |
| New Joiners | 411 |
| Historical Churn Count | 1,732 |
| Historical Churn Rate | 27.0% |
| Predicted At-Risk Customers (tuned model) | 377 |
| Revenue at Risk (tuned model, 411 new joiners) | ₹43,772 |
| Critical-Risk Share of Flagged Customers | 317 / 377 (84.1%) |
| Deployed Model Accuracy | 84.61% |
| Deployed Model Precision | 73.55% |
| Deployed Model Recall (Churn Class) | 72.91% |
| Deployed Model F1-Score | 73.23% |

<br>

## What Drives Churn

Month-to-Month contract customers churn at 46.5%, compared to 11% for One Year and 2.7% for Two Year contracts. That gap alone tells most of the story.

Beyond contract type, Fiber Optic internet users churn at 57.9%, which is abnormally high and points to either service reliability issues or a pricing problem relative to competitors. The biggest single churn category is competitor switching, with 761 customers explicitly citing that as their reason for leaving.

Geographically, Jammu & Kashmir (57.2%), Assam (38.1%), and Jharkhand (34.5%) have the highest churn rates by state. On the prediction side, Uttar Pradesh, Maharashtra, and Tamil Nadu need the most immediate retention attention.

Customers who subscribe to security and support add-ons churn significantly less. Online Security non-subscribers churn at 34.7% versus 14.9% for subscribers, and the same pattern repeats across Premium Support (34.5% vs 15.8%), Online Backup, and Device Protection Plan.

Payment method tracks with churn almost as cleanly as contract type: Mailed Check customers churn at 42.9%, Bank Withdrawal at 36.0%, and Credit Card at just 16.2% — a signal that digital-first payment habits go along with broader account engagement. Churn also climbs steadily with age, with customers over 50 showing the highest churn rate of any age band, and that group makes up the single largest segment (132 of 377) in the newly-flagged at-risk list.

The notebook now backs all of this with 25+ Python visualizations (box plots, a correlation heatmap, count/bar/KDE plots, and a grouped model-comparison chart) covering demographic, account, geographic, and service-level churn drivers, in addition to the Power BI report.

<br>

## Predicted At-Risk Customer Profile (411 New Joiners)

Applying the tuned model to the 411 new joiners at the default 50% threshold flags 377 customers, breaking down as:

| Attribute | Breakdown |
|---|---|
| Gender | Female: 246 · Male: 131 |
| Age Group | <20: 12 · 20-35: 105 · 35-50: 128 · >50: 132 |
| Marital Status | No: 198 · Yes: 179 |
| Contract | Month-to-Month: 362 · One Year: 15 · Two Year: 0 |
| Tenure Group | <6m: 65 · 6-12m: 90 · 12-18m: 57 · 18-24m: 61 · ≥24m: 104 |
| Payment Method | Credit Card: 192 · Bank Withdrawal: 148 · Mailed Check: 37 |
| Internet Type | None: 149 · DSL: 98 · Fiber Optic: 79 · Cable: 51 |
| Top States | Uttar Pradesh (43), Maharashtra (39), Tamil Nadu (36), Karnataka (30) |

In the live ChurnRadar run, 317 of the 377 flagged customers (84.1%) land in the **Critical** band (≥90% churn probability), with an average churn probability of 94.1% across all flagged customers.

<br>

## Retention Strategy Recommendations

- **Contract upgrade incentives** for Month-to-Month customers, especially the 362 already flagged as at-risk.
- **A rapid-response counter-offer script** for customers showing intent to switch to a competitor (the largest single churn category, at 761 historical customers).
- **A service-quality review of the Fiber Optic tier**, given its consistently high churn rate (42.5%–57.9% depending on cut).
- **Bundle-and-save promotions** for customers with no add-on security or support subscription.
- **Immediate outreach to the 317 Critical-risk customers** identified by ChurnRadar, ahead of any further model refresh.

<br>

## Project Structure

```
Customer Churn Analysis Project/
│
├── Data & Resources/
│   └── Customer_Data.csv
│
├── Python EDA & ML/
│   ├── Python_EDA_ML.ipynb
│   ├── churn_preprocessor.joblib
│   ├── baseline_xgb_model.joblib
│   ├── tuned_xgb_model.joblib
│   ├── high_risk_churn_list.csv
│   └── new_joiners_data.csv
│
├── Power BI Dashboard Screenshots/
│   ├── Summary_Page.png
│   └── Predictions_Page.png
│
├── SQL ETL/
│   ├── 01_etl_pipeline.sql
│   ├── 02_kpi_analysis.sql
│   ├── 03_data_quality_check.sql
│   ├── 04_imputation_strategy.sql
│   ├── 05_clean_table.sql
│   └── 06_analytical_views.sql
│
├── Streamlit App/
│   └── churn_prediction.py
│
├── Churn Analysis.pbix
├── Power BI Dashboard.pdf
└── Customer Churn Analysis and Predictions Project Report.pdf
```

<br>

## Tech Stack

| Layer | Tool |
|---|---|
| Data Storage | Microsoft SQL Server (T-SQL) |
| Business Intelligence | Power BI Desktop |
| Language | Python 3.12 |
| ML Libraries | scikit-learn, XGBoost, LightGBM |
| Data Handling | Pandas, NumPy |
| Visualisation | Matplotlib, Seaborn |
| Live Dashboard | Streamlit |
| Model Persistence | joblib |
| DB Connector | SQLAlchemy + pyodbc |

<br>

## How the Pipeline Works

**SQL Server** handles everything from raw data ingestion to producing clean, analysis-ready views. The pipeline runs across six scripts. Raw CSV data lands in a staging table first (`dbo.stg_Churn`). A null audit runs across all 32 columns. Missing values in service columns are filled with `No` or `None` rather than dropped, because a null there means the customer simply doesn't subscribe, it's not missing data. Churn classification nulls go into an `Others` bucket. The cleaned data writes into a production table (`dbo.prod_Churn`), and two SQL views split it by customer status: `vw_ChurnData` for historical training data, `vw_JoinData` for new joiners.

**Power BI** connects directly to those views. No manual CSV exports needed for the BI layer. The two-page report includes slicers for Monthly Charge Range and Marital Status that filter across all visuals simultaneously.

**The Jupyter Notebook** pulls from SQL Server using SQLAlchemy, runs data understanding (shape, dtypes, missing/duplicate/unique checks), boxplot-based outlier review, and a correlation heatmap before touching any model. Preprocessing runs through a `ColumnTransformer` pipeline (OrdinalEncoder for `Contract`, OneHotEncoder for the remaining 18 categorical columns, passthrough for numerics — no scaling, since every candidate model is tree-based or Naive Bayes). Two derived features, `Age_Group` and `Tenure_Group`, are engineered purely for visualization and dropped before training to avoid leakage.

**Five models were compared:**

| Model | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| Decision Tree | 0.7887 | 0.6084 | 0.7522 | 0.6727 |
| Naive Bayes | 0.7745 | 0.5837 | 0.7637 | 0.6617 |
| Random Forest | 0.8378 | 0.7123 | 0.7349 | 0.7234 |
| XGBoost (baseline) | 0.8386 | 0.7131 | 0.7378 | 0.7252 |
| LightGBM | 0.8228 | 0.6642 | 0.7810 | 0.7179 |

XGBoost was the strongest baseline, so it went into hyperparameter tuning. Rather than optimizing a blended metric, tuning used a custom scorer: maximize accuracy, but only among parameter combinations that keep recall on the churn class at or above 71%. Earlier, unconstrained tuning attempts had pushed accuracy to 86% by dropping recall to 65% — in a retention context that trade goes the wrong way, since a missed churner is a lost customer. The recall-floor-constrained search (`RandomizedSearchCV`, 100 candidates, 5-fold stratified CV) landed on: `n_estimators=200`, `max_depth=7`, `learning_rate=0.05`, `subsample=0.6`, `colsample_bytree=0.7`, `min_child_weight=5`, `gamma=0`, `reg_alpha=1`, `reg_lambda=2`, `scale_pos_weight=2`. That combination improves accuracy, precision, and F1 while giving up less than a point of recall:

| Metric | Baseline XGBoost | Tuned XGBoost (deployed) |
|---|---|---|
| Accuracy | 83.86% | **84.61%** |
| Precision | 71.31% | **73.55%** |
| Recall | **73.78%** | 72.91% |
| F1-Score | 72.52% | **73.23%** |

On the 1,202-customer test set, the tuned model produces 764 true negatives, 91 false positives, 94 false negatives, and 253 true positives — fewer wasted retention offers (lower false positives) than the baseline, at the cost of three additional missed churners. That trade was judged worth it, and `tuned_xgb_model.joblib` is the version that ships.

**ChurnRadar** is the Streamlit app. Upload the two `.joblib` files and a customer CSV, and the dashboard runs predictions automatically. A threshold slider (default 50%) controls which customers appear. Customers get tagged Critical (≥90%), High (75-90%), or Medium (<75%) and the retention team can filter, drill into individual profiles, and export a targeted contact list.

<br>

## Running It Locally

You'll need SQL Server (Express works fine) with ODBC Driver 17, Power BI Desktop, and Python 3.10 or later.

Install the Python dependencies:

```bash
pip install pandas numpy scikit-learn xgboost lightgbm joblib sqlalchemy pyodbc streamlit matplotlib seaborn
```

Run the SQL scripts in order (01 through 06). Update the file path in `01_etl_pipeline.sql` to point at your local `Customer_Data.csv` before running.

Open `Python_EDA_ML.ipynb` and run all cells. It connects to SQL Server, runs the full EDA and preprocessing pipeline, trains and compares all five models, tunes XGBoost, and exports `churn_preprocessor.joblib`, `baseline_xgb_model.joblib`, `tuned_xgb_model.joblib`, and `high_risk_churn_list.csv` into the `Machine Learning Predictions/` folder.

Open `Churn Analysis.pbix` in Power BI Desktop and refresh the data source connection to `db_Churn`. The Prediction page needs `high_risk_churn_list.csv` connected as a flat file source — re-point it at the latest export if you want the dashboard numbers to match the tuned model.

Launch ChurnRadar:

```bash
streamlit run "Streamlit App/churn_prediction.py"
```

Then upload the two joblib files and your customer CSV from the sidebar.

<br>

## About

**Shehraz Sarwar**
Data Scientist | IBM Certified Data Analyst | Ex Data Science Intern @10Pearls & @State Bank Of Pakistan | Section Leader Stanford CIP '25

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/shehraz-sarwar-ghouri-321394247/)
