import pandas as pd
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/fetch/<unique_id>', methods=['GET'])
def fetch_by_id(unique_id):
    csv_file_path = 'results_with_unique_id.csv'  # Adjust to your file's path
    
    try:
        df = pd.read_csv(csv_file_path)
        df['uuid'] = df['uuid'].str.strip()  # Strip any spaces
        record = df[df['uuid'] == unique_id]  # Search for the record by ID
        
        if not record.empty:
            # Convert the record to a dictionary or JSON format
            record_dict = record.to_dict(orient='records')[0]
            return jsonify(record_dict)
        else:
            return jsonify({"error": f"ID {unique_id} not found"}), 404
    except FileNotFoundError:
        return jsonify({"error": "CSV file not found"}), 500

if __name__ == '__main__':
    app.run(debug=True)
