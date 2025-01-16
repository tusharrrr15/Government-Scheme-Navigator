from flask import Flask, render_template, request
import pandas as pd
import openai

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = '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'

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    query = request.form['query']
    response = gpt3_query(query, df)
    return response

if __name__ == '__main__':
    app.run(debug=True)
