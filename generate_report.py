from fpdf import FPDF
import os


class ReportPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(80, 80, 80)
        self.cell(0, 8, "Data Mining Final Report - Chicago Crime Dataset 2024", align="R")
        self.ln(4)
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def chapter_title(self, num, title):
        self.set_font("Helvetica", "B", 14)
        self.set_fill_color(30, 80, 162)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, f"  {num}. {title}", fill=True, ln=True)
        self.ln(3)
        self.set_text_color(0, 0, 0)

    def section_title(self, title):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(30, 80, 162)
        self.cell(0, 8, title, ln=True)
        self.set_text_color(0, 0, 0)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        self.set_x(self.l_margin)
        self.multi_cell(0, 6, text)
        self.ln(2)

    def bullet(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        self.set_x(15)
        self.multi_cell(0, 6, f"*  {text}")

    def stat_row(self, label, value):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(30, 80, 162)
        self.cell(90, 7, label)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        self.cell(0, 7, value, ln=True)

    def add_image_centered(self, path, w=160):
        if os.path.exists(path):
            x = (210 - w) / 2
            self.image(path, x=x, w=w)
            self.ln(3)

    def fig_caption(self, text):
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 6, text, align="C", ln=True)
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def table_header(self, cols, widths):
        self.set_font("Helvetica", "B", 10)
        self.set_fill_color(30, 80, 162)
        self.set_text_color(255, 255, 255)
        for col, w in zip(cols, widths):
            self.cell(w, 8, col, border=1, fill=True)
        self.ln()
        self.set_text_color(0, 0, 0)

    def table_row(self, values, widths, fill=False):
        self.set_font("Helvetica", "", 10)
        self.set_fill_color(240, 245, 255)
        for val, w in zip(values, widths):
            self.cell(w, 7, str(val), border=1, fill=fill)
        self.ln()

    def multi_table_row(self, values, widths, fill=False):
        self.set_font("Helvetica", "B" if fill else "", 9)
        self.set_fill_color(240, 245, 255) if fill else self.set_fill_color(255, 255, 255)
        self.set_text_color(0, 0, 0)
        x_start = self.get_x()
        y_start = self.get_y()
        row_h = 6
        ys = []
        for val, w in zip(values, widths):
            self.set_xy(x_start + sum(widths[:list(widths).index(w)]), y_start)
            self.multi_cell(w, row_h, val, border=1, fill=fill)
            ys.append(self.get_y())
        self.set_y(max(ys))


pdf = ReportPDF()
pdf.set_auto_page_break(auto=True, margin=20)
pdf.set_margins(10, 15, 10)


# ─── COVER PAGE ───────────────────────────────────────────────────────────────
pdf.add_page()
pdf.set_font("Helvetica", "B", 26)
pdf.set_text_color(30, 80, 162)
pdf.ln(30)
pdf.cell(0, 14, "Data Mining Final Project", align="C", ln=True)
pdf.cell(0, 14, "Chicago Crime Dataset 2024", align="C", ln=True)
pdf.ln(6)

pdf.set_font("Helvetica", "", 14)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 10, "Preprocessing, Data Integration & Predictive Modeling", align="C", ln=True)
pdf.ln(20)

pdf.set_draw_color(30, 80, 162)
pdf.set_line_width(0.8)
pdf.line(40, pdf.get_y(), 170, pdf.get_y())
pdf.ln(20)

pdf.set_font("Helvetica", "", 12)
pdf.set_text_color(60, 60, 60)
info = [
    ("Course",   "Data Mining"),
    ("Student",  "Samagan Nurdinov"),
    ("Date",     "April 2026"),
    ("Dataset",  "Chicago Crimes 2024 (City of Chicago Open Data)"),
    ("GitHub",   "github.com/techsamagan"),
]
for label, val in info:
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(50, 9, f"{label}:", align="R")
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 9, f"  {val}", ln=True)


# ─── 1. INTRODUCTION ──────────────────────────────────────────────────────────
pdf.add_page()
pdf.chapter_title(1, "Introduction")
pdf.body_text(
    "This report documents the complete data mining pipeline applied to the Chicago Crime "
    "Dataset for 2024, obtained from the City of Chicago's Open Data portal. The dataset "
    "captures every reported crime incident across the city and provides rich spatial, temporal, "
    "and categorical attributes well-suited for both preprocessing and predictive modeling."
)
pdf.body_text(
    "The project is structured into two major phases. The first phase (previously completed) "
    "covers the full data preprocessing pipeline: cleaning, reduction, transformation, and "
    "discretization. The second phase -- presented here as new progress -- adds Data Integration "
    "from a second data source (Chicago community demographics), an enhanced Cluster Analysis "
    "with empirical K selection, and a Random Forest Classification model for predicting arrests."
)
pdf.ln(2)
pdf.section_title("Dataset Overview")
stats = [
    ("Raw Records",             "259,032 rows"),
    ("Original Features",       "22 columns"),
    ("Records After Cleaning",  "257,547 rows  (99.4% retained)"),
    ("Final Feature Set",       "26 engineered columns"),
    ("Integrated Dataset",      "28 columns after demographic merge"),
    ("Year Covered",            "2024"),
    ("Source",                  "City of Chicago Open Data Portal"),
]
for label, val in stats:
    pdf.stat_row(label + ":", val)


# ─── 2. DATA PREPROCESSING (SUMMARY) ─────────────────────────────────────────
pdf.add_page()
pdf.chapter_title(2, "Data Preprocessing Pipeline")

pdf.body_text(
    "A complete preprocessing pipeline was applied before any modeling. The table below "
    "summarizes every technique, its implementation, and the rationale for its selection."
)
pdf.ln(2)

steps = [
    ("Data Cleaning",
     "Dropped 1,486 rows missing Lat/Long; filled Location Description with 'UNKNOWN'",
     "Coordinates are required for all spatial analysis; descriptive field is preserved with placeholder"),
    ("Attribute Subset Selection",
     "Removed 7 identifier columns (ID, Case Number, IUCR, FBI Code, etc.)",
     "These columns add no predictive value and increase dimensionality unnecessarily"),
    ("PCA",
     "Reduced 4 spatial features (Lat, Long, District, Ward) to 2 principal components",
     "District & Ward are highly correlated (r=0.653); 2 PCs retain 84.21% of variance"),
    ("Min-Max Normalization",
     "Scaled Latitude & Longitude to [0, 1] range",
     "Required for K-Means - prevents scale bias in Euclidean distance computation"),
    ("Z-Score Standardization",
     "Standardized District & Ward (mean=0, std=1)",
     "Required for PCA; centers data and equalizes each feature's contribution"),
    ("Feature Engineering",
     "Extracted Hour, Month, Day_of_Week from raw Date string",
     "Exposes temporal patterns hidden inside the timestamp"),
    ("Equal-Width Binning",
     "Hour binned into 4 time periods (Late Night / Morning / Afternoon / Evening)",
     "Reduces 24 discrete hour values to 4 interpretable periods; reduces noise"),
    ("Concept Hierarchy",
     "Mapped 77 Community Areas to 4 City Sectors",
     "Reduces cardinality from 77 to 4; enables geographic-level pattern analysis"),
    ("Binary Discretization",
     "Created Is_Outdoor flag from Location Description",
     "Simplifies dozens of location types into a meaningful indoor/outdoor distinction"),
]

pdf.table_header(["Technique", "Implementation", "Justification"], [42, 68, 80])
for i, (tech, impl, just) in enumerate(steps):
    fill = (i % 2 == 0)
    x_start = pdf.get_x()
    y_start = pdf.get_y()
    row_h = 6
    pdf.set_fill_color(240, 245, 255) if fill else pdf.set_fill_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 9)
    pdf.multi_cell(42, row_h, tech, border=1, fill=fill)
    y1 = pdf.get_y()
    pdf.set_xy(x_start + 42, y_start)
    pdf.set_font("Helvetica", "", 9)
    pdf.multi_cell(68, row_h, impl, border=1, fill=fill)
    y2 = pdf.get_y()
    pdf.set_xy(x_start + 110, y_start)
    pdf.multi_cell(80, row_h, just, border=1, fill=fill)
    y3 = pdf.get_y()
    pdf.set_y(max(y1, y2, y3))

pdf.ln(4)
pdf.section_title("Key Preprocessing Results")
pdf.bullet("99.4% record retention after cleaning - only genuinely unusable rows were removed.")
pdf.bullet("Dimensionality reduced from 22 original to 26 meaningful engineered features.")
pdf.bullet("PCA compressed 4 correlated spatial features into 2 components, retaining 84.21% variance.")
pdf.bullet("Three discretization techniques applied to improve interpretability.")

pdf.ln(4)
pdf.add_image_centered("pca_reduction_plot.png", w=140)
pdf.fig_caption("Figure 1: PCA of Chicago crime locations (PC1 vs PC2). PC1 captures the north-south city layout.")
pdf.add_image_centered("correlation_heatmap.png", w=130)
pdf.fig_caption("Figure 2: Pearson correlation heatmap. District-Ward correlation (r=0.653) justifies PCA reduction.")


# ─── 3. DATA INTEGRATION ──────────────────────────────────────────────────────
pdf.add_page()
pdf.chapter_title(3, "Data Integration - Community Demographics")

pdf.section_title("3.1  Motivation")
pdf.body_text(
    "The Chicago Crime dataset on its own records incidents but provides no socioeconomic "
    "context. To enrich the analysis, population figures from the 2020 U.S. Census were "
    "merged for all 77 Chicago community areas. This allows computation of per-capita crime "
    "rates - a far more meaningful metric than raw counts when comparing areas of very "
    "different sizes."
)

pdf.section_title("3.2  Integration Process")
pdf.body_text(
    "A lookup table mapping each of the 77 Community Area codes to its official name and "
    "2020 Census population was built from the City of Chicago Data Portal's Community "
    "Area boundaries and Census summary files. A left join on 'Community Area' merged "
    "these two population columns (Area_Name, Population) into the preprocessed crime "
    "dataset, producing 'integrated_chicago_crimes_2024.csv' with 28 total columns."
)
pdf.table_header(["Metric", "Value"], [100, 90])
pdf.table_row(["Total community areas matched",       "77 of 77 (100%)"], [100, 90], fill=True)
pdf.table_row(["Population range",                   "2,876 (Fuller Park) to 100,309 (Austin)"], [100, 90])
pdf.table_row(["Overall city crime rate",             "~90 crimes per 1,000 residents"], [100, 90], fill=True)
pdf.table_row(["Highest per-capita crime area",       "Fuller Park - 243 per 1,000 residents"], [100, 90])
pdf.table_row(["Lowest per-capita crime area",        "Edison Park - 24 per 1,000 residents"], [100, 90], fill=True)
pdf.ln(4)

pdf.section_title("3.3  Top 10 Areas by Crime Rate")
top_areas = [
    ("Fuller Park",             "243.0", "2,876",   "699"),
    ("West Garfield Park",      "215.3", "17,433",  "3,754"),
    ("Englewood",               "213.3", "24,369",  "5,197"),
    ("Washington Park",         "208.4", "11,717",  "2,442"),
    ("Near West Side",          "204.7", "53,258",  "10,901"),
    ("Loop",                    "204.6", "45,396",  "9,289"),
    ("Greater Grand Crossing",  "198.5", "32,602",  "6,470"),
    ("East Garfield Park",      "192.7", "19,992",  "3,852"),
    ("Chatham",                 "190.5", "30,585",  "5,827"),
    ("North Lawndale",          "188.5", "34,794",  "6,560"),
]
pdf.table_header(["Community Area", "Rate/1k", "Population", "Crime Count"], [80, 30, 40, 40])
for i, row in enumerate(top_areas):
    pdf.table_row(list(row), [80, 30, 40, 40], fill=(i % 2 == 0))
pdf.ln(4)

pdf.body_text(
    "Per-capita analysis reveals a stark contrast: Fuller Park records 10 times more "
    "crimes per resident than Edison Park. This disparity would be invisible from raw "
    "crime counts alone, where large-population areas like Austin or Near West Side "
    "appear to dominate. Integration with census data makes the analysis equitable and "
    "policy-relevant."
)

pdf.add_image_centered("crime_rate_by_area.png", w=160)
pdf.fig_caption("Figure 3: Top 20 community areas ranked by crime rate per 1,000 residents.")
pdf.add_image_centered("population_vs_crime.png", w=150)
pdf.fig_caption("Figure 4: Population vs crime count by community area (color = crime rate per 1,000).")


# ─── 4. ENHANCED CLUSTERING ───────────────────────────────────────────────────
pdf.add_page()
pdf.chapter_title(4, "Model 1: Enhanced Cluster Analysis (K-Means)")

pdf.section_title("4.1  Why Cluster Analysis?")
pdf.body_text(
    "K-Means clustering is the most natural model for this dataset because crime data "
    "is inherently spatial and does not come with predefined group labels. Clustering "
    "discovers the hidden geographic structure of crime hotspots without any supervision. "
    "The resulting clusters can directly inform police resource allocation and patrol routing."
)

pdf.section_title("4.2  Improvements Over Midterm Version")
pdf.body_text(
    "The original midterm clustering used only Latitude and Longitude as features. "
    "The enhanced version adds two behavioral features - Hour (time of day) and Is_Outdoor "
    "(location type) - so clusters reflect not just WHERE crimes occur, but WHEN and in "
    "WHAT TYPE of environment. Additionally, the Elbow Method was applied to empirically "
    "validate K=10 rather than choosing it arbitrarily."
)
pdf.table_header(["Feature", "Midterm", "Final"], [60, 60, 70])
pdf.table_row(["Input features",     "Latitude, Longitude",           "Latitude, Longitude, Hour, Is_Outdoor"], [60, 60, 70], fill=True)
pdf.table_row(["K selection",        "Arbitrary (K=10)",              "Elbow method (K=10 confirmed)"], [60, 60, 70])
pdf.table_row(["Cluster profiles",   "None",                          "Crime count, arrest rate, avg hour"], [60, 60, 70], fill=True)
pdf.table_row(["Normalization",      "Min-Max on Lat/Long",           "Min-Max on all 4 features"], [60, 60, 70])
pdf.ln(4)

pdf.section_title("4.3  Elbow Method Results")
pdf.body_text(
    "The Within-Cluster Sum of Squares (Inertia) was computed for K=2 through K=15. "
    "The curve shows a clear elbow near K=9 to K=10, where the rate of inertia reduction "
    "slows significantly. K=10 was selected as the optimal balance between cluster "
    "granularity and computational efficiency."
)
pdf.add_image_centered("elbow_curve.png", w=155)
pdf.fig_caption("Figure 5: Elbow method plot. The inflection near K=10 confirms our choice empirically.")

pdf.section_title("4.4  Cluster Profiles")
pdf.body_text(
    "Each cluster has a distinct behavioral signature. Evening/night clusters with "
    "outdoor locations show the highest arrest rates (19-20%), while late-night indoor "
    "clusters show the lowest (10-11%)."
)
profiles = [
    ("2",  "40,012", "14.0%", "18.5", "0%"),
    ("6",  "35,868", "11.7%", "10.9", "0%"),
    ("8",  "31,866", "19.7%", "17.9", "100%"),
    ("4",  "30,494",  "9.8%", "11.4", "0%"),
    ("7",  "25,809", "12.1%", "19.2", "0%"),
    ("3",  "23,803", "20.6%", "17.9", "100%"),
    ("5",  "19,321", "15.7%",  "5.1", "100%"),
    ("0",  "18,848", "11.3%",  "2.1", "0%"),
    ("1",  "15,924", "10.9%",  "4.8", "100%"),
    ("9",  "15,602", "10.7%",  "2.1", "0%"),
]
pdf.table_header(["Cluster", "Crime Count", "Arrest Rate", "Avg Hour", "Outdoor?"], [28, 38, 35, 35, 54])
for i, row in enumerate(profiles):
    pdf.table_row(list(row), [28, 38, 35, 35, 54], fill=(i % 2 == 0))
pdf.ln(4)

pdf.add_image_centered("crime_clusters.png", w=130)
pdf.fig_caption("Figure 6: Enhanced K-Means crime hotspot map (K=10). Red X = cluster centroids.")
pdf.add_image_centered("cluster_profiles.png", w=160)
pdf.fig_caption("Figure 7: Crime count and arrest rate per cluster. Dashed line = city-wide arrest average.")


# ─── 5. CLASSIFICATION MODEL ──────────────────────────────────────────────────
pdf.add_page()
pdf.chapter_title(5, "Model 2: Random Forest Classification (Arrest Prediction)")

pdf.section_title("5.1  Problem Definition")
pdf.body_text(
    "The second model addresses the question: given the characteristics of a reported crime, "
    "can we predict whether it will result in an arrest? This is a binary classification "
    "problem (Arrest = 1 / No Arrest = 0). Accurate arrest prediction has practical "
    "value for resource allocation, crime deterrence strategy, and identifying which crime "
    "types and locations are consistently resolved by law enforcement."
)

pdf.section_title("5.2  Why Random Forest?")
pdf.body_text(
    "Random Forest was selected over simpler models (Logistic Regression, Decision Tree) "
    "for three reasons:"
)
pdf.bullet("It handles the mixed feature set naturally - numeric (Hour, District), binary (Domestic, Is_Outdoor), and label-encoded categorical (Crime Type) without requiring separate encoding strategies.")
pdf.bullet("It is robust to the severe class imbalance (85.8% No Arrest vs 14.2% Arrest) when combined with class_weight='balanced', which up-weights the minority class during training.")
pdf.bullet("Feature importance scores provide interpretable insights into which variables drive arrest likelihood.")

pdf.section_title("5.3  Model Configuration")
pdf.table_header(["Parameter", "Value", "Justification"], [55, 45, 90])
config = [
    ("n_estimators",   "100",           "Sufficient for stable performance; higher values plateau"),
    ("max_depth",      "12",            "Limits overfitting while allowing complex decision boundaries"),
    ("class_weight",   "'balanced'",    "Compensates for 6:1 class imbalance (No Arrest : Arrest)"),
    ("train/test split","80% / 20%",    "Standard split; stratified to preserve arrest rate in both sets"),
    ("Features used",  "12",            "Hour, Month, Day_of_Week, District, Ward, Beat, Domestic, Is_Outdoor, Time_Period_Bin, Community Area, Crime Type (encoded), City Sector (encoded)"),
    ("Target",         "Arrest (0/1)",  "Binary outcome: whether the incident led to an arrest"),
]
for i, row in enumerate(config):
    pdf.table_row(list(row), [55, 45, 90], fill=(i % 2 == 0))
pdf.ln(4)

pdf.section_title("5.4  Results")
pdf.table_header(["Metric", "Value", "Interpretation"], [55, 40, 95])
results = [
    ("Overall Accuracy",    "84.29%",  "Correct prediction on 43,434 of 51,510 test samples"),
    ("ROC-AUC Score",       "0.8154",  "Strong discrimination between arrest and non-arrest cases"),
    ("No Arrest Precision", "0.92",    "92% of predicted 'no arrest' cases are truly no arrest"),
    ("Arrest Recall",       "0.55",    "Model identifies 55% of all actual arrest cases"),
    ("Arrest F1-Score",     "0.49",    "Balanced score accounting for precision-recall tradeoff"),
]
for i, row in enumerate(results):
    pdf.table_row(list(row), [55, 40, 95], fill=(i % 2 == 0))
pdf.ln(4)

pdf.body_text(
    "An ROC-AUC of 0.8154 indicates the model has strong discriminatory power - it is "
    "8x better than a random classifier. The lower arrest recall (0.55) reflects the "
    "difficulty of predicting the minority class: even with balanced weighting, rare "
    "arrest events are harder to capture. This is expected and honest - a perfect "
    "classifier on imbalanced crime data would be suspicious."
)

pdf.add_image_centered("confusion_matrix.png", w=130)
pdf.fig_caption("Figure 8: Confusion matrix. 89% of non-arrests and 55% of arrests are correctly classified.")
pdf.add_image_centered("feature_importance.png", w=155)
pdf.fig_caption("Figure 9: Feature importance scores. Crime type and community area are strongest predictors.")
pdf.add_image_centered("roc_curve.png", w=130)
pdf.fig_caption("Figure 10: ROC curve (AUC=0.8154). Significantly above the random baseline diagonal.")


# ─── 6. FREQUENT PATTERN MINING ──────────────────────────────────────────────
pdf.add_page()
pdf.chapter_title(6, "Model 3: Frequent Pattern Mining (Apriori Algorithm)")

pdf.section_title("6.1  Why Frequent Pattern Mining?")
pdf.body_text(
    "While the clustering model reveals WHERE crimes concentrate and the classification "
    "model predicts WHETHER an arrest will occur, neither model answers a third question: "
    "WHAT combinations of crime attributes co-occur more often than chance? Frequent Pattern "
    "Mining (Apriori algorithm) is the natural tool for this question. It discovers "
    "association rules of the form 'IF [crime type + location type] THEN [arrest outcome]' "
    "along with objective metrics: support (how often the pattern appears), confidence "
    "(reliability), and lift (strength relative to random chance). These rules are "
    "human-readable and directly actionable for law enforcement policy."
)

pdf.section_title("6.2  Data Preparation for Apriori")
pdf.body_text(
    "Each crime incident was converted into a transaction (basket) containing six categorical "
    "items: Crime Category, Time Period, Location Type, City Sector, Arrest Outcome, and "
    "Domestic Flag. The 10 most frequent crime types were retained to keep the itemset space "
    "tractable. This yielded 237,929 transactions across 24 unique items."
)
pdf.table_header(["Parameter", "Value", "Justification"], [55, 45, 90])
config_fpm = [
    ("Transactions",     "237,929",          "Top-10 crime types (filtered from 257,547 total records)"),
    ("Unique items",     "24",               "Crime type (10) + Time (4) + Location (2) + Sector (4) + Arrest (2) + Domestic (2)"),
    ("Min. support",     "3% (0.03)",        "Captures patterns in at least ~7,100 incidents; filters noise"),
    ("Min. confidence",  "60% (0.60)",       "Rule must correctly predict the consequent 60%+ of the time"),
    ("Frequent itemsets","333",              "All 1-, 2-, and 3-item combinations above the support threshold"),
    ("Total rules",      "316",              "All rules above the confidence threshold; 141 are arrest-related"),
]
for i, row in enumerate(config_fpm):
    pdf.table_row(list(row), [55, 45, 90], fill=(i % 2 == 0))
pdf.ln(4)

pdf.section_title("6.3  Top Association Rules")
pdf.body_text(
    "The table below shows the 8 strongest arrest-related rules, ranked by lift. "
    "A lift > 1.0 means the antecedent and consequent co-occur more often than "
    "expected by chance. Lift = 2.43 means Motor Vehicle Theft is 2.43x more likely "
    "to appear with an outdoor, no-arrest outcome than random co-occurrence would predict."
)
fpm_rules = [
    ("Crime:MOTOR VEHICLE THEFT",  "Loc:Outdoor, NotArrested",     "0.068", "0.747", "2.430"),
    ("Crime:DECEPTIVE PRACTICE",   "Loc:Indoor, NotArrested",      "0.059", "0.885", "1.517"),
    ("Crime:BURGLARY",             "Loc:Indoor, NotArrested",      "0.031", "0.870", "1.492"),
    ("Crime:MOTOR VEHICLE THEFT",  "NonDomestic, NotArrested",     "0.087", "0.958", "1.309"),
    ("Crime:DECEPTIVE PRACTICE",   "NonDomestic, NotArrested",     "0.064", "0.951", "1.300"),
    ("Crime:BURGLARY",             "NonDomestic, NotArrested",     "0.032", "0.911", "1.246"),
    ("Crime:ROBBERY",              "NonDomestic, NotArrested",     "0.034", "0.894", "1.223"),
    ("Crime:THEFT",                "NonDomestic, NotArrested",     "0.225", "0.890", "1.217"),
]
pdf.table_header(["Antecedent (IF)", "Consequent (THEN)", "Support", "Confidence", "Lift"], [62, 62, 18, 22, 16])
for i, row in enumerate(fpm_rules):
    pdf.table_row(list(row), [62, 62, 18, 22, 16], fill=(i % 2 == 0))
pdf.ln(4)

pdf.section_title("6.4  Key Interpretations")
pdf.bullet(
    "Motor Vehicle Theft is the strongest pattern driver (lift = 2.43): when a car theft "
    "is reported on an outdoor location, the probability of no arrest is 74.7%. This rule "
    "covers 6.8% of all incidents - a meaningful share of the dataset."
)
pdf.bullet(
    "Deceptive Practice (fraud, identity theft) has the highest confidence: 88.5% of such "
    "crimes occur indoors and result in no arrest. These crimes are difficult to resolve "
    "at the scene because the offender is typically absent."
)
pdf.bullet(
    "Theft is the highest-support pattern (22.5% of transactions), with 89% confidence "
    "toward no arrest. This means nearly 1 in 4 transactions in the database follows the "
    "rule 'Theft => Not Arrested' - the most prevalent crime-outcome pattern in Chicago 2024."
)
pdf.bullet(
    "All top rules share the NotArrested consequent, confirming the 85.8% no-arrest "
    "baseline in the data. The patterns distinguish WHICH crime types and locations are "
    "most strongly associated with unresolved incidents - a direct guide for policy focus."
)

pdf.add_image_centered("apriori_item_frequency.png", w=160)
pdf.fig_caption("Figure 11: Item support across all 24 items. NotArrested and NonDomestic are most frequent.")
pdf.add_image_centered("apriori_scatter.png", w=155)
pdf.fig_caption("Figure 12: Support vs Confidence scatter for arrest-related rules (color = lift).")
pdf.add_image_centered("apriori_top_rules.png", w=160)
pdf.fig_caption("Figure 13: Top 10 rules ranked by lift. Green = Not Arrested consequent; Red = Arrested.")


# ─── 7. KEY FINDINGS ──────────────────────────────────────────────────────────
pdf.add_page()
pdf.chapter_title(7, "Key Findings & Insights")

pdf.section_title("7.1  Geographic Crime Distribution")
pdf.bullet(
    "Crime is not uniformly distributed - it is highly concentrated. The top 10 community "
    "areas account for a disproportionate share of incidents. On a per-capita basis, "
    "Fuller Park (243/1k) has 10x the crime rate of Edison Park (24/1k), revealing "
    "deep socioeconomic inequality in crime exposure across the city."
)
pdf.bullet(
    "K-Means clustering identified 10 distinct hotspot zones. The Loop and Near West Side "
    "appear as major commercial crime hubs (high raw count, moderate arrest rate), while "
    "residential areas like West Garfield Park show high per-capita rates with lower "
    "arrest resolution."
)

pdf.section_title("7.2  Temporal Patterns")
pdf.bullet(
    "Evening and afternoon are the peak crime windows: Afternoon (31.2%) and Evening (28.5%) "
    "together account for nearly 60% of all incidents. However, the arrest rate is highest "
    "in evening outdoor clusters (~20%), suggesting more witnesses or police presence "
    "during these hours."
)
pdf.bullet(
    "Late-night indoor clusters (average hour 2 AM) show the lowest arrest rates (10-11%), "
    "pointing to a gap in enforcement during overnight hours at indoor locations."
)

pdf.section_title("7.3  Arrest Prediction Drivers")
pdf.bullet(
    "Crime Type Encoded is the most important feature in the Random Forest model. "
    "This means the type of crime committed is the single strongest predictor of "
    "whether an arrest will follow - drug offenses and weapons violations resolve "
    "at far higher rates than theft or criminal damage."
)
pdf.bullet(
    "Community Area and Beat (patrol zone) are the 2nd and 3rd most important features, "
    "indicating that local law enforcement capacity and familiarity with an area "
    "significantly influences arrest outcomes."
)
pdf.bullet(
    "Hour of crime is a meaningful predictor: arrests are marginally more likely for "
    "crimes committed during daytime hours, consistent with greater police visibility."
)

pdf.section_title("7.4  Frequent Pattern Insights")
pdf.bullet(
    "Apriori mining revealed that Motor Vehicle Theft, Deceptive Practice, and Burglary "
    "are the three crime types most strongly associated with no arrest outcome (lift 2.43, "
    "1.52, and 1.49 respectively). These crimes share a common structure: the offender "
    "is absent at the time of reporting, making on-scene apprehension nearly impossible."
)
pdf.bullet(
    "Theft is the single highest-support pattern (22.5% of all transactions), with 89% "
    "confidence toward no arrest. This means the most common crime in Chicago is also "
    "among the least likely to be resolved - highlighting a systemic enforcement gap."
)

pdf.section_title("7.5  Data Integration Insight")
pdf.bullet(
    "Raw crime counts are misleading without population context. The Loop appears to be "
    "a top-5 crime area by count (9,289 incidents), but its 204/1k rate is driven partly "
    "by its large daytime transient population not captured by Census residential figures. "
    "This highlights the limitation of using residential population as the denominator "
    "for commercial-core neighborhoods."
)


# ─── 8. FUTURE WORK & LIMITATIONS ────────────────────────────────────────────
pdf.add_page()
pdf.chapter_title(8, "Future Work & Limitations")

pdf.section_title("8.1  Current Limitations")
pdf.bullet(
    "Class imbalance: Arrests represent only 13.85% of incidents. Even with balanced "
    "class weights, the model's arrest recall is 0.55 - meaning 45% of actual arrests "
    "are missed. Techniques like SMOTE (Synthetic Minority Oversampling) or cost-sensitive "
    "learning could improve minority-class recall."
)
pdf.bullet(
    "Population denominator: The Census residential population is an imperfect proxy for "
    "exposure risk. A neighborhood like the Loop has far more daytime activity than its "
    "45,396 residents suggest. Ambient population estimates (from mobile device data) "
    "would produce more accurate crime rate comparisons."
)
pdf.bullet(
    "Temporal scope: This analysis covers only 2024. A multi-year dataset (2018-2024) "
    "would enable trend analysis and detection of pre/post-COVID crime pattern shifts."
)
pdf.bullet(
    "K-Means assumptions: K-Means forces every point into a cluster and assumes spherical "
    "cluster shapes. Chicago's elongated north-south geography and irregular neighborhood "
    "boundaries may not align well with circular Euclidean clusters."
)

pdf.section_title("8.2  Future Improvements")
pdf.bullet(
    "Hierarchical or DBSCAN clustering: Unlike K-Means, DBSCAN can discover clusters "
    "of arbitrary shape and automatically identify noise points (isolated crime incidents). "
    "This would better capture the irregular crime geography of Chicago."
)
pdf.bullet(
    "Weather data integration: Merging daily temperature and precipitation data (available "
    "from NOAA) would allow testing the hypothesis that crime rates increase during warm "
    "weather - a well-documented effect in criminology literature."
)
pdf.bullet(
    "Real-time dashboard: The existing interactive HTML dashboard could be extended with "
    "live predictions from the trained Random Forest model, providing police dispatchers "
    "with a probability-of-arrest score for incoming incidents."
)


# ─── 9. CONCLUSION ────────────────────────────────────────────────────────────
pdf.add_page()
pdf.chapter_title(9, "Conclusion")

pdf.body_text(
    "This project successfully applied a full data mining workflow to the Chicago Crime "
    "2024 dataset - from raw data ingestion through preprocessing, data integration, "
    "and three distinct analytical models. Starting from 259,032 raw records, the pipeline "
    "produced a clean, enriched, and analytically ready dataset that supported unsupervised "
    "learning, supervised classification, and frequent pattern discovery."
)

pdf.section_title("Summary of Deliverables")
deliverables = [
    ("Data Cleaning",           "257,547 records retained; 99.4% preservation rate"),
    ("Data Reduction",          "PCA (84.21% variance in 2 components), 7 columns dropped"),
    ("Normalization",           "Min-Max for K-Means; Z-Score for PCA"),
    ("Discretization",          "3 techniques: time bins, city sectors, indoor/outdoor flag"),
    ("Data Integration",        "2020 Census demographics merged for all 77 community areas"),
    ("Model 1 - Clustering",    "K-Means (K=10) with elbow validation and cluster profiling"),
    ("Model 2 - Classification","Random Forest: 84.3% accuracy, ROC-AUC 0.8154"),
    ("Model 3 - Freq. Patterns","Apriori: 333 itemsets, 316 rules, top lift 2.43 (Motor Vehicle Theft -> Outdoor+NoArrest)"),
    ("Visualizations",          "13 publication-quality charts generated"),
]
pdf.table_header(["Step", "Outcome"], [70, 120])
for i, (step, outcome) in enumerate(deliverables):
    pdf.table_row([step, outcome], [70, 120], fill=(i % 2 == 0))
pdf.ln(6)

pdf.body_text(
    "The most important lesson from this project is that crime data analysis requires "
    "multiple lenses. Raw counts mislead; per-capita rates reveal equity issues. "
    "Geographic clustering shows WHERE to act; classification shows WHAT predicts resolution; "
    "frequent pattern mining shows WHICH crime attribute combinations are systematically "
    "under-resolved. No single model or metric tells the whole story - and that is precisely "
    "why a structured data mining pipeline that combines all three approaches is necessary "
    "for actionable insights."
)


# ─── SAVE ─────────────────────────────────────────────────────────────────────
output_path = "Data_Mining_Report_Chicago_Crime_2024.pdf"
pdf.output(output_path)
print(f"Report saved: {output_path}")
