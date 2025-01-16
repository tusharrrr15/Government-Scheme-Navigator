from flask import Flask, render_template, request, redirect, url_for, jsonify
import csv
import pandas as pd
import openai

app = Flask(__name__)

openai.api_key = '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'

# Initialize an empty dictionary to hold schemes data
schemes_data = {}

def load_schemes_from_csv(filename):
    """Load schemes data from a CSV file and populate the schemes_data dictionary."""
    global schemes_data  # Reference the global schemes_data dictionary
    
    # Clear existing data
    schemes_data.clear()
    
    # Open the CSV file
    with open(filename, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Process each row in the CSV file
        for row in reader:
            state = row['state']
            gender = row['gender']
            scheme_name = row['name']
            scheme_link = row['link']
            scheme_information = row['information']
            
            # Check if the state and gender keys exist in the dictionary
            if state not in schemes_data:
                schemes_data[state] = {}
            if gender not in schemes_data[state]:
                schemes_data[state][gender] = []
            
            # Append the scheme data to the list
            schemes_data[state][gender].append({
                'name': scheme_name,
                'link': scheme_link,
                'information': scheme_information
            })

# Load the schemes data from the CSV file on startup
load_schemes_from_csv('demo_schemes.csv')

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/ask')
def render_ask():
    return render_template('index.html')

@app.route('/schemes')
def render_schemes():
    return render_template('index2.html')

@app.route('/get_schemes', methods=['POST'])
def get_schemes():
    state = request.form.get('state')
    gender = request.form.get('gender')
    
    if state and gender:
        schemes = schemes_data.get(state, {}).get(gender, [])
        return jsonify({'schemes': schemes, 'state': state, 'gender': gender})
    else:
        return jsonify({'error': 'Invalid state or gender'})

@app.route('/index3.html')
def render_index3():
    state = request.args.get('state')
    gender = request.args.get('gender')

    if not state or not gender:
        return redirect(url_for('index'))

    schemes = schemes_data.get(state, {}).get(gender, [])
    return render_template('index3.html', state=state, schemes=schemes)

# Load the data
df = pd.read_csv('schemes.csv')

def gpt3_query(query, data):
    try:
        # Summarize data
        data_summary = data.head(100).to_string(index=False)

        # Prepare the prompt
        prompt = f"""
        User query: {query}
        Data context:
        {data_summary}
        
        Provide a response to the user's query based on the data context.
        """
        
        # Get response from OpenAI API
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": "You are a helpful assistant who can answer questions based on provided data."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        
        # Return the response content
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return "Sorry, I'm unable to process your request right now."


@app.route('/query', methods=['POST'])
def query():
    query = request.form['query']
    response = gpt3_query(query, df)
    return response

if __name__ == '__main__':
    app.run(debug=True)
