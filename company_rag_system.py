import os
import glob
import streamlit as st
from dotenv import load_dotenv
import openai


class CompanyRagSystem:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY', 'your-key-if-not-using-env')
        self.client = openai.Client(api_key=self.api_key)
        self.model = "gpt-4o-mini"
        self.context = {}
        self.system_message = (
            "You are an expert in answering accurate questions about Insurellm, the Insurance Tech company. "
            "Categorize questions as related to 'company', 'products', 'contracts', or 'employees'. "
            "Retrieve and use only relevant context from the stored knowledge. If you don't know the answer, say so."
        )
        self.load_data()

    def load_data(self):
        paths = {
            "employees": "./company-info/employees/*",
            "products": "./company-info/products/*",
            "contracts": "./company-info/contracts/*",
            "company": "./company-info/company/*"
        }

        for category, path in paths.items():
            files = glob.glob(path)
            for file in files:
                name = os.path.basename(file).split('.')[0]
                with open(file, "r", encoding="utf-8") as f:
                    self.context[(category, name)] = f.read()

    def classify_message(self, message):
        """Determina si el mensaje es sobre company, products, contracts o employees."""
        classification_prompt = (
            "Classify the following message into one of the categories: "
            "'company', 'products', 'contracts', 'employees'. If it doesn't fit any, return 'unknown'.\n\n"
            f"Message: {message}\n\nCategory:"
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": classification_prompt}]
        )
        return response.choices[0].message.content.strip().lower()

    def get_relevant_context(self, message):
        """Busca contexto según la clasificación del mensaje."""
        category = self.classify_message(message)
        relevant_context = []

        for (context_category, title), details in self.context.items():
            if context_category == category:
                relevant_context.append(details)

        return relevant_context

    def add_context(self, message):
        relevant_context = self.get_relevant_context(message)
        if relevant_context:
            message += "\n\nRelevant context:\n\n"
            message += "\n\n".join(relevant_context)
        return message

    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_message}] + history
        message = self.add_context(message)
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
