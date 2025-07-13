import pandas as pd
import gradio as gr

# --- 1. Load the Data ---
# Ensure the filepath is correct relative to where you run the script.
try:
    df = pd.read_csv("data/netherlands_master_energy_dataset.csv")
    # Set 'Year' as the index for easy data lookup.
    df.set_index('Year', inplace=True)
    print("✅ Data loaded successfully.")
except FileNotFoundError:
    print("❌ ERROR: 'data/netherlands_master_energy_dataset.csv' not found.")
    df = None # Set DataFrame to None if loading fails

# --- 2. Define the Gradio Function ---
def get_energy_info(year):
    """
    Retrieves and formats energy data for a selected year from the DataFrame.
    """
    if df is None:
        return "Error: Data file could not be loaded."
    try:
        # Use .loc to select the row corresponding to the chosen year
        data_row = df.loc[year]
        
        # Use the CORRECT column names from your CSV file
        consumption = data_row['Electricity_Consumption_TWh']
        co2_index = data_row['CO2_Emissions_Index']
        renewable_share = data_row['Renewable_Share_Percent']
        
        # Format the output string for display
        output_text = (
            f"📈 Year: {year}\n"
            f"⚡ Electricity Consumption: {consumption} TWh\n"
            f"💨 CO₂ Emissions Index: {co2_index}\n"
            f"🌱 Renewable Energy Share: {renewable_share}%"
        )
        return output_text
        
    except KeyError:
        # Handle cases where the selected year might not be in the data
        return f"Error: Data not found for the year {year}."

# --- 3. Create and Launch the Gradio Interface ---
if df is not None:
    # Create a list of years from the DataFrame index for the dropdown
    year_list = df.index.tolist()

    # Build the Gradio interface
    iface = gr.Interface(
        fn=get_energy_info,
        inputs=gr.Dropdown(choices=year_list, label="Select Year", value=year_list[0]),
        outputs=gr.Textbox(lines=4, label="Energy Information"),
        title="Netherlands Energy Info",
        description="Displays electricity consumption, CO2 emissions, and renewable share for a selected year.",
        allow_flagging="never"
    )
    
    # Launch the web interface
    iface.launch()
else:
    print("Application cannot start because the data file failed to load.")