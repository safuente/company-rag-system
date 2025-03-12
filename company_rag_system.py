import os
import glob
import streamlit as st
from dotenv import load_dotenv
import openai


class CompanyRagSystem:
    def __init__(self):
        """Initialize the system by loading the API key, setting up OpenAI client, and loading the company data."""
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY', 'your-key-if-not-using-env')
        self.client = openai.Client(api_key=self.api_key)
        self.model = "gpt-4o-mini"
        self.context = {}  # Stores the company-related documents
        self.system_message = (
            "You are an expert in answering questions about Insurellm, the Insurance Tech company. "
            "Categorize user queries as related to 'company', 'products', 'contracts', or 'employees'. "
            "Retrieve and use only relevant context from the stored knowledge. If no relevant information is available, say so."
        )
        self.load_data()

    def load_data(self):
        """Load company-related data into memory from predefined file paths."""
        paths = {
            "employees": "./company-info/employees/*",
            "products": "./company-info/products/*",
            "contracts": "./company-info/contracts/*",
            "company": "./company-info/company/*"
        }

        for category, path in paths.items():
            files = glob.glob(path)  # Get all files in the directory
            for file in files:
                name = os.path.basename(file).split('.')[0]  # Extract filename without extension
                with open(file, "r", encoding="utf-8") as f:
                    self.context[(category, name)] = f.read()  # Store content in a dictionary

    def classify_message(self, message):
        """Classify a user's message into one of the predefined categories: 'company', 'products', 'contracts', or 'employees'."""
        classification_prompt = (
            "You will classify the user’s message into one of these categories: "
            "'company', 'products', 'contracts', 'employees'. If it does not fit any, return 'unknown'.\n\n"
            "Examples:\n"
            "1. 'What products does the company offer?' -> products\n"
            "2. 'Show me the list of employees' -> employees\n"
            "3. 'Give me details about the company's vision' -> company\n"
            "4. 'What contracts are available?' -> contracts\n"
            "5. 'How many employees does the company have?' -> employees\n"
            "6. 'What is the history of the company?' -> company\n"
            "7. 'List the products the company sells' -> products\n"
            "8. 'Provide contract details' -> contracts\n\n"
            f"User's message: {message}\n\nCategory:"
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": classification_prompt}]
        )
        return response.choices[0].message.content.strip().lower()

    def get_relevant_context(self, message):
        """Retrieve relevant company-related information based on the classified category."""
        category = self.classify_message(message)  # Get the category
        relevant_context = []

        for (context_category, title), details in self.context.items():
            if context_category == category:  # Check if the category matches
                relevant_context.append(details)

        return relevant_context

    def add_context(self, message):
        """Attach relevant context to the user's message to improve answer accuracy."""
        relevant_context = self.get_relevant_context(message)
        if relevant_context:
            message += "\n\nRelevant context:\n\n"
            message += "\n\n".join(relevant_context)
        return message

    def chat(self, message, history):
        """Handle chat interaction by processing user input and providing an appropriate response."""
        messages = [{"role": "system", "content": self.system_message}] + history
        message = self.add_context(message)  # Append relevant context
        messages.append({"role": "user", "content": message})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )

        return response.choices[0].message.content


# Streamlit UI
st.title("Company Rag System: Insurellm Expert Assistant")

assistant = CompanyRagSystem()
chat_history = []

user_input = st.text_input("Enter your question related to the company:")
if st.button("Send"):
    if user_input:
        response = assistant.chat(user_input, chat_history)
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": response})

        st.text_area("Response:", response, height=200)
    else:
        st.warning("Please enter a question before sending.")
