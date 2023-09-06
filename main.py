import pandas as pd
from capture_sheet import process_capture_sheet

if __name__ == "__main__":
    df = pd.read_excel("resources/Order Events.xlsx", sheet_name="Sheet1")
    processed_df, validation_df = process_capture_sheet(df)
    processed_df.to_csv("resources/processed.csv", index=False)
    validation_df.to_csv("resources/validation.csv", index=True)