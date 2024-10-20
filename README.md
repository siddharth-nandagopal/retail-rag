# RetailRAG: A Python-Based Retrieval-Augmented Generation Platform for Data-Driven Business Insights

## Overview
RetailRAG is an advanced data analysis platform that leverages the power of Large Language Models (LLMs) with Retrieval-Augmented Generation (RAG) techniques. It is designed to assist business users, such as finance analysts, C-level executives, and sales and marketing teams, in making data-driven decisions based on rich insights derived from retail transaction data.

The application uses Python to generate synthetic retail datasets, which are then used to provide real-time business reports and actionable insights. It seamlessly integrates with an LLM to deliver context-specific responses, making it a perfect solution for dynamic business needs.

## Key Features
- **Data Generation**: Generates synthetic retail transaction data, including product sales, customer purchase behavior, and store performance.
- **RAG Framework**: Combines vectorized data search with LLM-based response generation to deliver highly relevant answers.
- **Custom Business Prompts**: Allows users to interact with the system through intuitive prompts, making insights accessible without deep technical expertise.
- **Scalable Architecture**: Built with scalability in mind, leveraging PostgreSQL for data storage and advanced indexing for quick data retrieval.
- **Use Cases**: Designed for a wide range of use cases, including sales analysis, financial reporting, marketing insights, and executive summaries.

## Tech Stack
- **Python**: Data generation, API development, and integration with LLM.
- **PostgreSQL**: Stores retail transaction data for efficient retrieval.
- **FastAPI**: API framework for building and exposing RESTful endpoints.
- **Vector Store**: Utilizes FAISS or similar library for vector-based retrieval.
- **LLM**: GPT-4 or any other accessible LLM for generating context-aware responses.
- **Docker**: Containerized deployment for consistent development and production environments.

## Getting Started
1. **Clone the repository**:
   ```bash
   git clone https://github.com/siddharth-nandagopal/retail-rag.git
   cd retail-rag
   ```
2. **Install dependencies**:
   ```bash
   poetry install
   ```
3. **Set up PostgreSQL database**:
   - Update your PostgreSQL credentials in `config.py`.
   - Run the data generation script to populate the database.
4. **Start the API server**:
   ```bash
   uvicorn app.main:app --reload
   ```
5. **Query the RAG model**:
   - Use the provided API endpoints to ask business-related queries.
   - Example queries can be found in the `examples/` folder.
