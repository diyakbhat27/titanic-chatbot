import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns


def create_chart(df, chart_type):

    if chart_type is None:
        return None

    fig, ax = plt.subplots(figsize=(6, 4))

    if chart_type == "age_histogram":
        sns.histplot(df["Age"].dropna(), bins=30, ax=ax)
        ax.set_title("Age Distribution")

    elif chart_type == "fare_histogram":
        sns.histplot(df["Fare"].dropna(), bins=30, ax=ax)
        ax.set_title("Fare Distribution")

    elif chart_type == "survival_count":
        sns.countplot(x="Survived", data=df, ax=ax)
        ax.set_title("Survival Count")

    else:
        plt.close(fig)
        return None

    fig.tight_layout()
    return fig