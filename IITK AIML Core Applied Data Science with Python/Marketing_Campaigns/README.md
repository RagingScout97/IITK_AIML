# Marketing Campaigns

IITK AIML Core, Applied Data Science with Python.

2240 customers in `marketing_data.csv`. Each row has the people side (birth year, education, marital status, income, kids), product spend over the last 2 years, purchases by channel (web, catalog, store), and which campaigns they accepted. The brief asked for EDA plus hypothesis testing to see what actually drives customer acquisition.

## Run it

Python 3 with pandas, numpy, matplotlib, seaborn, scipy. Open this folder first so the notebook finds the CSV:

```bat
cd Marketing_Campaigns
jupyter notebook marketing_campaigns.ipynb
```

Or open the `.ipynb` in VS Code / Cursor, pick a Python 3 kernel, and Run All.

Everything is inside the notebook. No helper `.py` file this time. I wrote it in small cells so each step prints something before moving on.

## Cleaning

`Income` came in as text like `$84,835.00`, and the header had a space in front (` Income `). I strip the column names, then `parse_income` drops the `$` and commas and makes it a float. `Dt_Customer` is `6/16/14` style, so I parse it with `%m/%d/%y`.

24 incomes were blank. The brief said people with the same education and marital status earn about the same, so I filled each blank with the median of its Education + Marital_Status group. Median, not mean, because a few big incomes pull the mean up.

Marital_Status had `YOLO`, `Absurd` and `Alone`. Those went into `Single`. Education values were fine.

## New columns

- `Children` = Kidhome + Teenhome
- `Age` = 2014 - Year_Birth (the join dates sit around 2014)
- `TotalSpend` = sum of the six `Mnt*` columns
- `TotalPurchases` = web + catalog + store

## Outliers and encoding

Boxplots showed one income of 666666 and birth years before 1940. I dropped Income >= 200000 and Year_Birth < 1940. That removed 4 rows, so 2236 are left.

Education has an order, so it got an ordinal map (Basic 0 up to PhD 4). Marital_Status and Country have no order, so they got one-hot columns with `pd.get_dummies`.

Then a correlation heatmap. Income and TotalSpend go up together. More children goes with less spend.

## Hypothesis tests

I used Welch's t-test (`stats.ttest_ind` with `equal_var=False`) and alpha = 0.05.

| Question | Result |
|---|---|
| Older people buy more in store | Yes. 6.2 vs 5.3 store purchases, p close to 0 |
| Parents buy more online | No. Parents average 3.97 web purchases vs 4.39, p = 0.0005 |
| Other channels eat store sales | No sign of it. Store vs web+catalog corr is +0.62 |
| US beats the rest on total purchases | Not significant. 13.5 vs 12.5, p = 0.15, only 109 US rows |

The parents one surprised me. I expected busy parents to lean online, but the data goes the other way.

## Plots for the other questions

- Wine brings in the most money by far. Fruit and sweets are the lowest.
- Age vs last campaign (`Response`) corr is -0.02, so basically nothing.
- Spain has the most last-campaign accepts (176), but Spain also has the most customers.
- Spend drops once there are children at home.
- About 20 complaints in total. Graduation has the most, but it is also the biggest education group.

## Files

| File | What |
|---|---|
| `marketing_campaigns.ipynb` | the report |
| `marketing_data.csv` | original data, not overwritten |
| `1736837211_marketing_campaign_problem_statement.docx` | the brief |
| `Data Dictionary - Response to marketing campaigns.xlsx` | column meanings |

## Limits

Cannibalization is only checked with a correlation, not a proper model over time. Age is fixed to 2014, so it is age at joining, not age today.
