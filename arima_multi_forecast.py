import pandas as pd
import matplotlib.pyplot as plt
import warnings
from statsmodels.tsa.arima.model import ARIMA

# --- 1. Load and Prepare Data ---
df = pd.read_csv("data/netherlands_master_energy_dataset.csv")
df = df.dropna(subset=["Electricity_Consumption_TWh", "CO2_Emissions_Index", "Renewable_Share_Percent"])
df["Year"] = pd.to_datetime(df["Year"], format="%Y")
df.set_index("Year", inplace=True)

# --- 2. Define Helper Function to Fit Best ARIMA Model ---
def fit_best_arima(series, max_p=3, max_d=2, max_q=3):
    best_aic = float("inf")
    best_order = None
    best_model = None
    warnings.filterwarnings("ignore")

    for p in range(max_p + 1):
        for d in range(max_d + 1):
            for q in range(max_q + 1):
                try:
                    model = ARIMA(series, order=(p, d, q)).fit()
                    if model.aic < best_aic:
                        best_aic = model.aic
                        best_order = (p, d, q)
                        best_model = model
                except:
                    continue
    return best_model, best_order

# --- 3. Forecast and Plot for Each Variable ---
forecast_horizon = 5
results = {}

targets = {
    "Electricity_Consumption_TWh": "⚡ Electricity Consumption (TWh)",
    "CO2_Emissions_Index": "💨 CO₂ Emissions Index",
    "Renewable_Share_Percent": "🌱 Renewable Share (%)"
}

for col, label in targets.items():
    print(f"\nFitting ARIMA for {label}...")

    series = df[col]
    model, order = fit_best_arima(series)

    print(f"✔ Best ARIMA order for {label}: {order}")
    forecast = model.forecast(steps=forecast_horizon)

    # Save forecast
    forecast_years = pd.date_range(df.index[-1] + pd.DateOffset(years=1), periods=forecast_horizon, freq='YS')
    results[col] = pd.Series(forecast.values, index=forecast_years)

    # Plot
    plt.figure(figsize=(10, 5))
    plt.plot(series, label="Historical", color="blue")
    plt.plot(forecast_years, forecast, label="Forecast", linestyle="--", color="orange")
    plt.title(f"{label} Forecast (ARIMA {order})")
    plt.xlabel("Year")
    plt.ylabel(label)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# --- 4. Export Forecasts to CSV ---
forecast_df = pd.DataFrame(results)
forecast_df.index.name = "Year"
forecast_df.to_csv("netherlands_energy_forecast.csv")
print("\n📁 Forecast saved to 'netherlands_energy_forecast.csv'")
