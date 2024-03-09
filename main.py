import tkinter as tk
from tkinter import ttk
from langchain_openai import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import BaseOutputParser
from dotenv import load_dotenv
import os, re, time, threading

# ------------------- CONSTANTS -------------------- #
DARK_FRAME_COLOR = "#35374B"
DARK_USER_FONT_COLOR = "#CCC8AA"
DARK_AI_FONT_COLOR = "#78A083"
DARK_TEXTBOX_BACKGROUND_COLOR = "black"
MESSAGE_BOX_FONT = ("Droid Sans", 12, "normal")
USER_ENTRY_FONT = ("Open Sans", 12, "normal")
AI_TEMP = 0.3  # Controls how creative the AI's answers will be. 0 is safest but least creative.
AI_SPEED = .003  # Controls how fast the response text populates.

# ------------------ ENVIRONMENT ------------------ #
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), 'api_info.env'))

api_key = os.getenv("OPENAI_API_KEY")

chat_model = ChatOpenAI(
    temperature=AI_TEMP,
    openai_api_key=api_key,
    model_name="gpt-3.5-turbo"
)

template = "You're a friendly Python mentor that does the following: Syntax checking and correction: Provide suggestions or corrections for Python code based on common syntax errors.Code completion: Offer suggestions for completing code based on context, similar to how IDEs like PyCharm do.Code explanation: Provide explanations for complex or unfamiliar code snippets to help users understand them better.Code execution: Allow users to run Python code within the chat model and display the output.Documentation lookup: Retrieve and display documentation for Python modules, functions, or methods.Code formatting: Format code according to PEP8 or other standards to improve readability.Error handling: Provide suggestions for handling common errors or exceptions in Python code.Code refactoring: Offer suggestions for improving the structure or efficiency of existing code.Python version compatibility: Provide information on differences between Python 2 and Python 3 syntax.Library recommendations: Suggest Python libraries that could be useful for a given task or problem.Best practices: Offer tips and best practices for writing clean, efficient Python code."


# ----------------- UI CONFIGURATION ------------------- #
# Note: for some reason managing the field color of the entrybox is impossible on windows. I've managed to create find a workaround for customizing the colors of the scrollbar; however, I lose the ability to grab the thumb and move it manually. I've opted to keep this functionality and stick with a white thumb.
def create_dark_theme(root, message_list, send_button, entry_frame, message_frame):
    # Root color
    root.configure(bg=DARK_FRAME_COLOR)

    # Messagebox color
    message_list.configure(bg=DARK_TEXTBOX_BACKGROUND_COLOR)
    
    # Entry frame color
    ttk.Style().configure("EntryFrame.TFrame", background=DARK_FRAME_COLOR)
    entry_frame.configure(style="EntryFrame.TFrame")

    # Button colors
    send_button.configure(bg="#444443", fg="light grey")

    # Custom scrollbar
    style = ttk.Style()
    style.element_create("Custom.Scrollbar.trough", "from", "default")
    style.layout("Custom.TScrollbar",
                [('Custom.Scrollbar.trough', {'sticky': 'ns'}),
                ('Custom.Scrollbar.thumb', {'unit': 1,'sticky': 'ns', 'children':
                                            [('Custom.Scrollbar.grip', {'sticky': ''})]})])
    style.configure("Custom.TScrollbar", troughcolor="default", gripcount=0, background="#444443")
    scrollbar = ttk.Scrollbar(message_frame, orient=tk.VERTICAL, command=message_list.yview, style="Custom.TScrollbar")
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    message_list.config(yscrollcommand=scrollbar.set)


# ------------------ CHAT APP -------------------- #

class AnswerOutputParser(BaseOutputParser):
    def parse(self, text: str):
        """Parse the output of an LLM call."""
        return text.strip()


class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat App")

        self.message_frame = ttk.Frame(self.root, style="TFrame")
        self.message_frame.pack(padx=20, pady=(20, 5))

        self.message_list = tk.Text(self.message_frame, width=50, height=30, wrap=tk.WORD, font=MESSAGE_BOX_FONT, padx=20, pady=20)
        self.message_list.pack(side=tk.LEFT, fill=tk.BOTH)

        self.entry_frame = ttk.Frame(self.root, style="EntryFrame.TFrame")
        self.entry_frame.pack(padx=10, pady=20, fill=tk.BOTH)

        self.entry = ttk.Entry(self.entry_frame, width=30, font=USER_ENTRY_FONT)
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=30, anchor="e")

        self.send_button = tk.Button(self.entry_frame, text="Send", command=self.send_message, width=10)
        self.send_button.pack(padx=(0, 15), side=tk.RIGHT)

        create_dark_theme(self.root, self.message_list, self.send_button, self.entry_frame, self.message_frame)

        self.root.bind('<Return>', self.send_message)

        # Define tags for user and AI messages
        self.message_list.tag_configure("user", foreground=DARK_USER_FONT_COLOR)
        self.message_list.tag_configure("ai", foreground=DARK_AI_FONT_COLOR)


    def send_message(self, event=None):
        user_input = self.entry.get()
        self.entry.delete(0, tk.END)
        if not user_input:
            return

        # Display user's message immediately & in blue
        self.message_list.insert(tk.END, "You: ", "user")
        self.message_list.insert(tk.END, f"{user_input}\n\n", "user")

        def invoke_model():
            chat_prompt = ChatPromptTemplate.from_messages([
                ("system", template),
                ("human", user_input),
            ])
            messages = chat_prompt.format_messages(text=user_input)
            result = chat_model.invoke(messages)
            parsed = AnswerOutputParser().parse(result.content)

            # Split the AI's response into words while preserving formatting
            words = re.findall(r'\S+|\s+', parsed)
            for word in words:
                self.message_list.insert(tk.END, f"{word}", "ai")
                self.message_list.yview(tk.END)  # Scroll to the bottom
                self.message_list.update()  # Update the widget to show the new word
                if word.strip():  # Check if the word is not just whitespace
                    time.sleep(AI_SPEED)  # Adjust the delay between words as needed


            self.message_list.insert(tk.END, "\n\n")  # Add a line break after the response
            self.message_list.yview(tk.END)  # Scroll to the bottom

        threading.Thread(target=invoke_model).start()


# --------------------- MAIN -------------------- #

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()