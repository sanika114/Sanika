import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# 1. Import the data
df = pd.read_csv("medical_examination.csv")


# 2. Add 'overweight' column (BMI = weight / height^2 in meters)
bmi = df['weight'] / ((df['height'] / 100) ** 2)
df['overweight'] = (bmi > 25).astype(int)


# 3. Normalize cholesterol and gluc (0 = good, 1 = bad)
df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)


# ------------------------------
# DRAW CATEGORICAL PLOT
# ------------------------------
def draw_cat_plot():
    
    # 4. Melt data
    df_cat = pd.melt(
        df,
        id_vars=['cardio'],
        value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight']
    )

    # 5. Group and count
    df_cat = (
        df_cat
        .groupby(['cardio', 'variable', 'value'])
        .size()
        .reset_index(name='total')
    )

    # 6. Draw catplot
    fig = sns.catplot(
        data=df_cat,
        x='variable',
        y='total',
        hue='value',
        col='cardio',
        kind='bar'
    ).fig

    # 7. Save image
    fig.savefig('catplot.png')
    return fig


# ------------------------------
# DRAW HEAT MAP
# ------------------------------
def draw_heat_map():

    # 8. Clean data
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # 9. Correlation matrix
    corr = df_heat.corr()

    # 10. Mask upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # 11. Plot heatmap
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt=".1f",
        center=0,
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.5}
    )

    # 12. Save image
    fig.savefig('heatmap.png')
    return fig
