import openai
import pandas as pd
import tkinter as tk
from tkinter import scrolledtext

# Set your OpenAI API key
openai.api_key = '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'
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

def handle_query(query, data):
    # Get the response using gpt3_query
    response = gpt3_query(query, data)
    return response

def chat_interface(data):
    # Create a new tkinter window
    window = tk.Tk()
    window.title("Government Scheme Navigator")

    # Create a scrolled text widget for displaying chat history
    chat_history = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=80, height=20)
    chat_history.pack(pady=10)

    # Create an entry widget for user input
    user_input = tk.Entry(window, width=60)
    user_input.pack(pady=5)

    def on_send():
        # Get user input
        query = user_input.get()

        # Check for exit command
        if query.lower() in ["exit", "quit"]:
            window.quit()
            return

        # Handle the query and get response
        response = handle_query(query, data)

        # Display user query and bot response in chat history
        chat_history.insert(tk.END, f"\nYou: {query}")
        chat_history.insert(tk.END, f"\nBot: {response}\n")
        
        # Clear user input field
        user_input.delete(0, tk.END)

    # Create a button for sending user input
    send_button = tk.Button(window, text="Send", command=on_send)
    send_button.pack(pady=5)

    # Run the tkinter event loop
    window.mainloop()

# Load the data
df = pd.read_csv('schemes.csv')

# Run the chat interface
chat_interface(df)
