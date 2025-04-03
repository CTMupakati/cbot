from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load the Excel file (Modify the file path as needed)
excel_file = "crime_data.xlsx"
df_sheets = pd.read_excel(excel_file, sheet_name=None)

def get_crime_stats(crime_type, province, year):
    for sheet_name, df in df_sheets.items():  # Loop through all sheets
        if {'Crime Type', 'Province', 'Year', 'Cases Reported'}.issubset(df.columns):
            result = df[(df["Crime Type"].str.lower() == crime_type.lower()) &
                        (df["Province"].str.lower() == province.lower()) &
                        (df["Year"] == int(year))]
            if not result.empty:
                return result["Cases Reported"].values[0]
    return "No data available."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "").lower()
    
    try:
        words = user_message.split()
        crime_type = words[words.index("murder") if "murder" in words else words.index("robbery")]
        province = words[words.index("in") + 1]
        year = words[-1]
        
        answer = get_crime_stats(crime_type, province, year)
        return jsonify({"reply": f"{crime_type.capitalize()} cases in {province.capitalize()} for {year}: {answer}"})
    except Exception:
        return jsonify({"reply": "I couldn't understand your question. Please ask in this format: 'How many murder cases were recorded in Gauteng for 2024?'"})

if __name__ == "__main__":
    app.run(debug=True)
