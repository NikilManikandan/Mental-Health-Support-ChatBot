import tkinter as tk
from tkinter import scrolledtext
from ai71 import AI71

# Initialize AI71 client
AI71_API_KEY = "Enter API key here"
client = AI71(AI71_API_KEY)

messages = [{"role": "system", "content": "You are a mental health support chatbot."}]

def send_message(event=None):
    user_message = user_input.get("1.0", tk.END).strip()
    if user_message:
        messages.append({"role": "user", "content": user_message})
        chat_window.insert(tk.END, f"User: {user_message}\n")
        user_input.delete("1.0", tk.END)

        response = ""
        for chunk in client.chat.completions.create(
            messages=messages,
            model="tiiuae/falcon-180B-chat",
            stream=True,
        ):
            delta_content = chunk.choices[0].delta.content
            if delta_content:
                chat_window.insert(tk.END, delta_content)
                response += delta_content
                chat_window.see(tk.END)

        messages.append({"role": "assistant", "content": response})
        chat_window.insert(tk.END, "\n")
        
    if event:
        return "break"

# Set up the main application window
app = tk.Tk()
app.title("Mental Health Support Chatbot")

# Create a scrolled text widget for the chat window
chat_window = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=80, height=20, state='normal')
chat_window.pack(padx=10, pady=10)

# Create a text widget for user input
user_input = tk.Text(app, height=3, width=80)
user_input.pack(padx=10, pady=10)

# Bind the Enter key to the send_message function
user_input.bind("<Return>", send_message)

# Create a button to send the message
send_button = tk.Button(app, text="Send", command=send_message)
send_button.pack(pady=10)

# Run the application
app.mainloop()
