import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder


def main():
    df = pd.read_csv('final_preprocessed_crimes_2024.csv')

    # --- Build transactions ---
    # Each crime incident becomes a basket of categorical items
    df['Crime_Category'] = df['Primary Type'].str.upper().str.strip()

    time_labels = {0: 'LateNight', 1: 'Morning', 2: 'Afternoon', 3: 'Evening'}
    df['Time_Label'] = df['Time_Period_Bin'].map(time_labels)

    df['Location_Type'] = df['Is_Outdoor'].map({1: 'Outdoor', 0: 'Indoor'})
    df['Arrest_Label']  = df['Arrest'].map({1: 'Arrested', 0: 'NotArrested'})
    df['Domestic_Label'] = df['Domestic'].map({1: 'Domestic', 0: 'NonDomestic'})

    # Keep only the 10 most frequent crime types to keep itemsets tractable
    top_crimes = df['Crime_Category'].value_counts().head(10).index
    df = df[df['Crime_Category'].isin(top_crimes)].copy()

    transactions = df.apply(
        lambda r: [
            f"Crime:{r['Crime_Category']}",
            f"Time:{r['Time_Label']}",
            f"Loc:{r['Location_Type']}",
            f"Area:{r['City_Sector']}",
            r['Arrest_Label'],
            r['Domestic_Label'],
        ],
        axis=1
    ).tolist()

    te = TransactionEncoder()
    te_array = te.fit_transform(transactions)
    basket_df = pd.DataFrame(te_array, columns=te.columns_)

    print(f"Transaction matrix: {basket_df.shape[0]:,} rows x {basket_df.shape[1]} items")

    # --- Apriori: frequent itemsets (min support = 3%) ---
    print("\nMining frequent itemsets (min_support=0.03)...")
    freq_itemsets = apriori(basket_df, min_support=0.03, use_colnames=True, max_len=3)
    freq_itemsets['length'] = freq_itemsets['itemsets'].apply(len)
    freq_itemsets = freq_itemsets.sort_values('support', ascending=False)

    print(f"Found {len(freq_itemsets)} frequent itemsets")
    print("\nTop 15 frequent itemsets:")
    print(freq_itemsets.head(15)[['support', 'length', 'itemsets']].to_string(index=False))

    # --- Association rules (min confidence = 60%) ---
    print("\nGenerating association rules (min_confidence=0.60)...")
    rules = association_rules(freq_itemsets, metric='confidence', min_threshold=0.60,
                              num_itemsets=len(freq_itemsets))
    rules = rules.sort_values('lift', ascending=False)

    print(f"Found {len(rules)} association rules")

    # Filter to consequents with arrest-related conclusions
    arrest_rules = rules[
        rules['consequents'].apply(lambda x: any('Arrested' in i or 'NotArrested' in i for i in x))
    ].copy()
    print(f"\nArrest-related rules: {len(arrest_rules)}")
    print("\nTop 10 rules by lift:")
    for _, row in arrest_rules.head(10).iterrows():
        ant = ', '.join(sorted(row['antecedents']))
        con = ', '.join(sorted(row['consequents']))
        print(f"  IF [{ant}] THEN [{con}]  "
              f"supp={row['support']:.3f}  conf={row['confidence']:.3f}  lift={row['lift']:.3f}")

    # --- Chart 1: Support vs Confidence scatter (top rules) ---
    plot_rules = arrest_rules.head(40) if len(arrest_rules) >= 40 else arrest_rules
    fig, ax = plt.subplots(figsize=(10, 7))
    sc = ax.scatter(
        plot_rules['support'], plot_rules['confidence'],
        c=plot_rules['lift'], cmap='RdYlGn', s=90, alpha=0.85, edgecolors='grey', linewidths=0.4
    )
    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label('Lift', fontsize=11)
    ax.set_xlabel('Support', fontsize=12)
    ax.set_ylabel('Confidence', fontsize=12)
    ax.set_title('Frequent Pattern Mining — Association Rules\n(color = lift; each point is one rule)',
                 fontsize=13, fontweight='bold')
    ax.axhline(0.85, color='navy', linestyle='--', linewidth=1, label='Confidence = 85%')
    ax.legend()
    plt.tight_layout()
    plt.savefig('apriori_scatter.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\nSaved: apriori_scatter.png")

    # --- Chart 2: Top 10 rules bar chart (lift) ---
    top10 = arrest_rules.head(10).copy()
    top10['Rule'] = top10.apply(
        lambda r: ', '.join(sorted(r['antecedents'])) + ' → ' + ', '.join(sorted(r['consequents'])),
        axis=1
    )
    colors = ['#1e8a2a' if 'NotArrested' in r else '#c0392b' for r in top10['consequents']]

    fig, ax = plt.subplots(figsize=(13, 6))
    bars = ax.barh(range(len(top10)), top10['lift'].values, color=colors, edgecolor='white')
    ax.set_yticks(range(len(top10)))
    ax.set_yticklabels(top10['Rule'].values, fontsize=8)
    ax.set_xlabel('Lift', fontsize=12)
    ax.set_title('Top 10 Association Rules for Arrest Prediction\n(green = Not Arrested consequence, red = Arrested consequence)',
                 fontsize=12, fontweight='bold')
    ax.axvline(1.0, color='gray', linestyle='--', linewidth=1, label='Lift = 1 (no association)')
    ax.legend()
    patch_g = mpatches.Patch(color='#1e8a2a', label='→ NotArrested')
    patch_r = mpatches.Patch(color='#c0392b', label='→ Arrested')
    ax.legend(handles=[patch_g, patch_r, plt.Line2D([0], [0], color='gray', linestyle='--', label='Lift = 1')],
              fontsize=9)
    plt.tight_layout()
    plt.savefig('apriori_top_rules.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: apriori_top_rules.png")

    # --- Chart 3: Item frequency bar chart ---
    item_freq = basket_df.sum().sort_values(ascending=False).head(20)
    fig, ax = plt.subplots(figsize=(12, 5))
    colors_freq = ['#1e50a2' if i < 5 else '#7ba7d4' for i in range(len(item_freq))]
    ax.bar(item_freq.index, item_freq.values / len(basket_df) * 100,
           color=colors_freq, edgecolor='white')
    ax.set_ylabel('Support (%)', fontsize=11)
    ax.set_title('Top 20 Most Frequent Items in Transaction Database\n(% of crime incidents containing each item)',
                 fontsize=12, fontweight='bold')
    ax.set_xticklabels(item_freq.index, rotation=45, ha='right', fontsize=9)
    plt.tight_layout()
    plt.savefig('apriori_item_frequency.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: apriori_item_frequency.png")

    return {
        'n_transactions': len(basket_df),
        'n_itemsets': len(freq_itemsets),
        'n_rules': len(rules),
        'n_arrest_rules': len(arrest_rules),
        'top_rule_lift': arrest_rules.iloc[0]['lift'] if len(arrest_rules) > 0 else None,
        'top_rule_antecedents': ', '.join(sorted(arrest_rules.iloc[0]['antecedents'])) if len(arrest_rules) > 0 else '',
        'top_rule_consequent': ', '.join(sorted(arrest_rules.iloc[0]['consequents'])) if len(arrest_rules) > 0 else '',
        'top_rule_confidence': arrest_rules.iloc[0]['confidence'] if len(arrest_rules) > 0 else None,
        'top_rule_support': arrest_rules.iloc[0]['support'] if len(arrest_rules) > 0 else None,
    }


if __name__ == '__main__':
    results = main()
    print(f"\nSummary: {results['n_transactions']:,} transactions → "
          f"{results['n_itemsets']} itemsets → {results['n_rules']} rules "
          f"({results['n_arrest_rules']} arrest-related)")
