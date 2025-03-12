# Company RAG System - General Overview
Show information of employees, contracts, products and company using RAG (company-info folder) and GPT-4 mini model. 
## 📘 Company RAG System - Example Questions

The **Company RAG System** can categorize and answer questions related to **company information, products, contracts, and employees**. Below are some example queries for each category.

---

### 🔹 Company-related Questions
- Can you give me a brief history of the company?
- What is the company headquartered?

---

### 🔹 Product-related Questions
- What products does the company offer?
- What is the most popular product of the company?

---

### 🔹 Contract-related Questions
- What are the cancellation policies for contracts?
- Are there any special conditions in the contracts?
- How long do the contracts typically last?
- What happens if I need to modify my contract?

---

### 🔹 Employee-related Questions
- Who are the top employees of the company?
- Who are the employees of the company?


## Run code
Create a virtual env and install all the packages in requirements.txt:

    pip install -r requirements.txt

Create a .env file with the following content:
    
    OPENAI_API_KEY=<API_KEY>
    

OpenAI API key could be generated in the following way:
https://gptforwork.com/help/knowledge-base/create-openai-api-key


Execute the following command:

    streamlit run company_rag_system.py