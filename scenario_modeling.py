import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("data/netherlands_aqueduct40_country_risks.csv")

# Set plot style
sns.set(style="whitegrid")

# Barplot of risk scores
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x="score", y="indicator", palette="coolwarm")
plt.title("Netherlands - Water Risk Indicators (Aqueduct 4.0)", fontsize=14, weight='bold')
plt.xlabel("Risk Score (0=Low, 5=High)")
plt.ylabel("Indicator")
plt.tight_layout()
plt.show()

# Save cleaned scenario data for integration
scenario_df = df[["indicator", "score"]].set_index("indicator")
scenario_df.to_csv("netherlands_water_scenario_risks.csv")
print("\n💾 Risk data saved to 'netherlands_water_scenario_risks.csv'")
