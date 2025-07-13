import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# 1. Load data
df = pd.read_csv("data/netherlands_master_energy_dataset.csv")
df = df.dropna(subset=["Electricity_Consumption_TWh"])  # remove missing rows

# 2. Set Year as index and convert to datetime
df["Year"] = pd.to_datetime(df["Year"], format="%Y")
df.set_index("Year", inplace=True)

# 3. Select target variable
y = df["Electricity_Consumption_TWh"]

# 4. Fit ARIMA model (order can be optimized later)
model = ARIMA(y, order=(1, 1, 1))
model_fit = model.fit()

# 5. Forecast next 5 years
forecast = model_fit.forecast(steps=5)

# 6. Create future years
last_year = y.index[-1].year
future_years = pd.date_range(start=f"{last_year + 1}", periods=5, freq='Y')

# 7. Plot
plt.figure(figsize=(10, 6))
plt.plot(y, label="Historical")
plt.plot(future_years, forecast, label="Forecast", linestyle="--")
plt.title("Electricity Consumption Forecast (ARIMA)")
plt.xlabel("Year")
plt.ylabel("TWh")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()