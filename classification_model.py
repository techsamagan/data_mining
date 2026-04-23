import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    classification_report, confusion_matrix,
    roc_auc_score, roc_curve, accuracy_score
)

def main():
    df = pd.read_csv('final_preprocessed_crimes_2024.csv')

    # --- Feature Engineering ---
    le = LabelEncoder()
    df['Crime_Type_Encoded'] = le.fit_transform(df['Primary Type'])
    df['Sector_Encoded'] = le.fit_transform(df['City_Sector'])

    features = [
        'Hour', 'Month', 'Day_of_Week',
        'District', 'Ward', 'Beat',
        'Domestic', 'Is_Outdoor',
        'Time_Period_Bin', 'Community Area',
        'Crime_Type_Encoded', 'Sector_Encoded'
    ]
    target = 'Arrest'

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"Training samples: {len(X_train):,}  |  Test samples: {len(X_test):,}")
    print(f"Arrest rate in training set: {y_train.mean():.2%}")

    # --- Train Random Forest ---
    # class_weight='balanced' compensates for the 6:1 class imbalance (non-arrest vs arrest)
    rf = RandomForestClassifier(
        n_estimators=100,
        max_depth=12,
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    )
    rf.fit(X_train, y_train)

    y_pred = rf.predict(X_test)
    y_prob = rf.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, y_pred)
    roc_auc  = roc_auc_score(y_test, y_prob)

    print(f"\nAccuracy:  {accuracy:.4f}  ({accuracy:.2%})")
    print(f"ROC-AUC:   {roc_auc:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['No Arrest', 'Arrest']))

    # --- Chart 1: Confusion Matrix ---
    cm = confusion_matrix(y_test, y_pred)
    cm_pct = cm.astype(float) / cm.sum(axis=1, keepdims=True) * 100

    fig, ax = plt.subplots(figsize=(7, 5))
    sns.heatmap(cm, annot=False, fmt='d', cmap='Blues', ax=ax,
                xticklabels=['No Arrest', 'Arrest'],
                yticklabels=['No Arrest', 'Arrest'])

    for i in range(2):
        for j in range(2):
            ax.text(j + 0.5, i + 0.38, f'{cm[i,j]:,}',
                    ha='center', va='center', fontsize=14, fontweight='bold',
                    color='white' if cm[i,j] > cm.max() / 2 else 'black')
            ax.text(j + 0.5, i + 0.65, f'({cm_pct[i,j]:.1f}%)',
                    ha='center', va='center', fontsize=10,
                    color='white' if cm[i,j] > cm.max() / 2 else 'black')

    ax.set_xlabel('Predicted Label', fontsize=12)
    ax.set_ylabel('True Label', fontsize=12)
    ax.set_title(f'Random Forest Confusion Matrix\nAccuracy: {accuracy:.2%}  |  ROC-AUC: {roc_auc:.4f}', fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig('confusion_matrix.png', dpi=150, bbox_inches='tight')
    plt.close()

    # --- Chart 2: Feature Importance ---
    importances = pd.Series(rf.feature_importances_, index=features).sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(9, 6))
    colors = ['#1e50a2' if v >= importances.quantile(0.75) else '#7ba7d4' for v in importances]
    importances.plot(kind='barh', ax=ax, color=colors)
    ax.set_xlabel('Feature Importance (Mean Decrease in Impurity)', fontsize=11)
    ax.set_title('Random Forest Feature Importance\nfor Arrest Prediction', fontsize=13, fontweight='bold')
    ax.axvline(importances.mean(), color='red', linestyle='--', linewidth=1,
               label=f'Mean importance ({importances.mean():.4f})')
    ax.legend()
    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=150, bbox_inches='tight')
    plt.close()

    # --- Chart 3: ROC Curve ---
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.plot(fpr, tpr, color='#1e50a2', lw=2, label=f'Random Forest (AUC = {roc_auc:.4f})')
    ax.plot([0, 1], [0, 1], color='gray', lw=1, linestyle='--', label='Random Classifier (AUC = 0.5)')
    ax.fill_between(fpr, tpr, alpha=0.1, color='#1e50a2')
    ax.set_xlabel('False Positive Rate', fontsize=12)
    ax.set_ylabel('True Positive Rate (Recall)', fontsize=12)
    ax.set_title('ROC Curve - Arrest Prediction Model', fontsize=13, fontweight='bold')
    ax.legend(loc='lower right')
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1.02])
    plt.tight_layout()
    plt.savefig('roc_curve.png', dpi=150, bbox_inches='tight')
    plt.close()

    print("\nSaved: confusion_matrix.png, feature_importance.png, roc_curve.png")

    return {
        'accuracy': accuracy,
        'roc_auc': roc_auc,
        'top_feature': importances.idxmax(),
        'top_importance': importances.max()
    }

if __name__ == '__main__':
    main()
