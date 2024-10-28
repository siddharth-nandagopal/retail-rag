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
   asdf install
   ```
3. **Set up credentials**:
   - Update your credentials in `.env` at the root of this git project.

4. **Start the Services**:
   ```bash
   docker-compose up --build -d
   ```
5. **Query the RAG model**:
   - Use the provided API endpoints to ask business-related queries.
   - Examples:
   ```
   curl -X POST "http://localhost:8000/search/product_search" \
   -H "Content-Type: application/json" \
   -d '{
   "query": "What are the most popular products in 2024?"
   }'
   ```

   ```
   curl -X GET "http://localhost:8000/data/customers/1000" -H "accept: application/json"
   ```


### Explanation of the Docker Compose Services:

- **postgres (Data Layer)**: Hosts the PostgreSQL database for storing all structured retail data. It initializes with an init.sql script for creating tables.
- **data-generator (Data Ingestion & Embedding Layer)**: Generates synthetic retail data and populates the PostgreSQL database using the COPY method. This service connects to postgres and populates the database.
- **vector-store (Data Ingestion & Embedding Layer)**: Manages vector embeddings using a library like FAISS, and stores them in a dedicated volume for fast similarity search.
- **api (API Layer)**: The FastAPI service that handles data queries and requests for semantic search. It connects to both the PostgreSQL database and the vector store. (Note: AI inference must be modularized into separate layer/service - easy to swap 3rd party AI models) Also, it does AI inference, manages the LLM for generating responses based on data retrieved from the vector store and the database. It interacts with the api service to receive query results and deliver responses.




# Lessons learnt:

## Vector Store

Imagine you are the head of a retail company called "Retail Insights Inc." Your job is to make data-driven decisions using the mountains of sales data generated every day. But going through all the data manually takes too long. So, you decide to hire an assistant—let’s call them "Vector."

### Vector’s Role in the Story:
**Vector** is an assistant who can help you make sense of all your data quickly. Instead of just storing all your data in a basic filing cabinet (like a traditional database), Vector organizes the data into a highly structured, searchable format, allowing you to find exactly what you need in seconds. This is especially useful when you're dealing with text data, like customer reviews, product descriptions, or insights from sales data.

### What Vector Does:
1. **Understanding Your Data (Creating Embeddings)**:
   - Before Vector starts, they first need to understand what each piece of data means. Imagine that every sales record, product description, or customer review is a note written in different languages. Vector translates each note into a special language—numbers in a multi-dimensional space—called an **embedding**.
   - Think of embeddings as labels on each of the notes that help Vector understand what each note is about. These embeddings capture the essence or meaning of each data point. For example, notes about "smartphones," "tablets," and "gadgets" would have similar labels because they are closely related.

2. **Organizing Data into a Smart Map (Vector Store)**:
   - After translating the data into embeddings, Vector arranges these notes into a **smart map**. This smart map is the **vector store**.
   - Imagine the vector store as a vast, organized library where related books (data points) are kept close together. Books on similar topics are on nearby shelves, while those that are less related are farther apart. This way, if you ask Vector about "smartphones," they can quickly find related notes like "tablets" and "gadgets" since they are stored nearby.

3. **Answering Questions (Retrieving Relevant Data)**:
   - Let’s say you ask Vector, "Which products saw the highest sales growth last quarter?" Instead of scanning through each note manually, Vector uses the vector store to look for notes that are most relevant to your question.
   - Vector finds notes that talk about sales, growth, and product performance—because those notes are closest to the "meaning" of your question in their smart map. Vector then pulls out the top matches and hands them over to you.

4. **Explaining Answers with the Help of GPT (Generating a Response)**:
   - Once Vector finds the relevant notes, they bring them to a more articulate assistant—**GPT**—who can read the notes and explain them to you in plain English.
   - GPT takes the data Vector retrieved and crafts a response that makes sense to you, like: "The highest sales growth last quarter came from our new range of smartphones, which saw a 15% increase due to a holiday promotion."

### How the Vector Store Helps You Make Decisions:
- **Speed**: Instead of spending hours reading through sales records, you get your answers in seconds. The vector store lets you jump straight to the most relevant information.
- **Accuracy**: By organizing data based on meaning, Vector ensures that you get the most relevant insights, making your decisions more informed.
- **Intelligence**: Vector learns from every new piece of data you give them. As you update the smart map with new sales data or customer reviews, Vector keeps improving, making future searches even more accurate.


## Vector & Postgresql

In a Retrieval-Augmented Generation (RAG) system that uses a vector store, PostgreSQL and the vector store serve different but complementary purposes. Here's a story to explain the roles of each and how they work together in your RAG application:

### Story: Vector and Postgres as a Team
Imagine you are running a big retail company, "Retail Insights Inc." You rely on two assistants: **Vector** (the vector store) and **Postgres** (the relational database). Each of them has unique strengths, and they work together to make sure your business runs smoothly.

### Roles and Strengths:
1. **Postgres - The Detailed Record Keeper**:
   - Postgres is like a meticulous librarian who is great at organizing detailed records and storing structured data.
   - It stores the raw **transaction data**—things like customer IDs, product IDs, quantities, prices, transaction dates, and store details.
   - Postgres ensures **data integrity** and **relations** between different entities (like linking `invoice_id` to `customer_id` and `product_id`). For example, when you want to see all transactions for a specific customer or calculate total sales for a product, Postgres quickly retrieves that data.
   - It’s optimized for **structured queries** like SQL, making it ideal for aggregations (e.g., total sales by region), filtering (e.g., transactions above a certain amount), and data transformations.

2. **Vector - The Knowledge Organizer**:
   - Vector, on the other hand, is like a super-smart assistant who excels at understanding the **meaning** behind unstructured data.
   - It converts **textual data** (like product descriptions, customer reviews, or even insights derived from transaction data) into vectors (numerical representations) and organizes them based on their semantic relationships.
   - Vector is excellent at handling **fuzzy queries**—questions that aren’t just looking for a specific value but instead want an understanding of broader trends or insights. For example, when you ask, "What products do customers love the most?" Vector can find reviews and descriptions with similar sentiments.

### How They Work Together:
1. **Postgres as the Data Source**:
   - Postgres holds the raw data that your RAG application generates and updates—things like customer transactions, product details, and sales records.
   - When a business user asks a question like, "What are the top 5 products sold in California last month?" the first step might be to run a SQL query in Postgres to pull out the relevant sales data for California during that time period.

2. **Vector for Deep Insights**:
   - After retrieving this structured data from Postgres, the next step could be to understand **why** certain products performed better. This is where Vector comes in.
   - Suppose the business user now asks, "What do customers in California say about these products?" Vector uses its stored embeddings of customer reviews and product feedback to find similar sentiments or feedback trends, helping to provide context behind the sales numbers.

3. **Example Workflow**:
   - A business user, like a CEO, asks: "How did the holiday season impact our electronics sales, and what were customers saying about the new product features?"
   - **Step 1**: The RAG application queries Postgres to retrieve sales data for electronics during the holiday season—total units sold, revenue, regions, etc.
   - **Step 2**: The application then queries the vector store to find embeddings related to customer feedback and reviews about "new product features" in the electronics category.
   - **Step 3**: The results from both sources are combined, and GPT uses this combined data to craft a narrative, like: "Electronics sales increased by 15% during the holiday season, with high demand for the new features. Customer reviews frequently mentioned the long battery life and sleek design as major selling points."

### Why Use Both?
- **Structured vs. Unstructured Data**: Postgres is ideal for structured, tabular data with clear relationships, like transactions or inventory data. Vector is better for unstructured data and understanding the **context** behind that data, like extracting meaning from customer reviews.
- **Query Efficiency**: For queries where the answer is a specific number or summary (e.g., total sales), Postgres is efficient. For queries that require understanding of concepts, similarities, or context (e.g., finding reviews similar to "customers love the design"), Vector is more effective.
- **Data Integrity and Backup**: Postgres can serve as the **single source of truth** for all the raw data. Even if the vector store gets updated or retrained, the original data remains safe and consistent in Postgres.
- **Combining Insights**: Using both allows you to combine **quantitative** insights (e.g., sales figures) with **qualitative** insights (e.g., customer sentiments), giving a holistic view of your business performance.


## Performance of data insertion into PostgreSQL

The performance of data insertion into PostgreSQL using different methods can vary significantly based on factors like data volume, memory usage, and network latency. Let's compare three methods: pandas.to_sql, psycopg2 with execute_batch, and psycopg2 using CSV as an intermediate store:

| **Method**                    | **Speed (with large datasets)** | **Memory Usage**    | **Ease of Use** | **Best For**                   |
|-------------------------------|---------------------------------|---------------------|-----------------|--------------------------------|
| `pandas.to_sql`               | Slow                            | High                | Easy            | Small to medium datasets       |
| `psycopg2` with `execute_batch` | Moderate to fast                | Moderate            | Moderate        | Large datasets with batch control |
| `psycopg2` using CSV (`COPY`) | Very fast                       | Low (disk-based)    | Complex         | Very large datasets (1M+ rows) |


## Optimal batch load size

Determining the optimal batch load size when loading data into datastore depends on several factors, including network latency, the size of each row, datastore configuration, available memory, and the nature of the data being loaded. However, you can use a basic formula to estimate a good starting point for the batch size:

### Formula for Estimating Batch Load Size

A formula to determine a suitable batch size might be:
```
Batch Size = Available Memory for Load / Average Row Size
```

Where:
- **Available Memory for Load**: The portion of memory you can allocate to the data-loading process. This depends on the available system memory and any other concurrent processes.
- **Average Row Size**: The average size of each row in the data being loaded.

### Estimating the Values

1. **Determine Available Memory for Load**:
   - If the total system memory is M_total (e.g., 16 GB), and you want to allocate a portion for this process:
     ```
     available = M_total * Memory Allocation Percentage
     ```
   - For example, if you allocate 30% of a 16 GB system to this process:
     ```
     available = 16 GB * 0.30 = 4.8 GB
     ```

2. **Estimate Average Row Size**:
   - Calculate the average size of a single row based on the size of each column. For example, if a row contains:
     - `customer_id`: `INT` (4 bytes)
     - `product_id`: `INT` (4 bytes)
     - `quantity`: `INT` (4 bytes)
     - `unit_price`: `FLOAT` (4 bytes)
     - `price`: `FLOAT` (4 bytes)
     - `discount_applied`: `FLOAT` (4 bytes)
     - `transaction_date`: `TIMESTAMPTZ` (8 bytes)
     - `payment_method`: `VARCHAR(20)` (Average ~20 bytes)
     - `store_address`: `VARCHAR(100)` (Average ~50 bytes)
     - `product_description`: `TEXT` (Average ~200 bytes)

     Sum these estimates to get the approximate average row size. For the example above:
    
      ```
      Average Row Size} = 4 + 4 + 4 + 4 + 4 + 4 + 8 + 20 + 50 + 200 = 302 bytes
      ```

3. **Calculate Batch Size**:
   - Convert memory to bytes (e.g., 4.8 GB = 4.8 * 1024^3  bytes):
     ```
     M_available = 4.8 * 1024^3 = 5,161,345,024 bytes
     ```
   - Calculate the batch size:
     ```
     Batch Size = 5,161,345,024 bytes / 302 bytes per row = 17,090,778 rows
     ```

This means that, in theory, you could load around 17 million rows in a single batch given the memory and average row size assumptions.

### Practical Considerations:
1. **Start Smaller**: In practice, starting with a smaller batch size (e.g., 10,000 rows) and gradually increasing it while monitoring memory usage and database performance is often safer.
2. **Transaction Size**: Large batches can put a lot of stress on your datastore/API-service. Datastore will need to manage the transaction and might use more disk space temporarily due to its MVCC (Multi-Version Concurrency Control) mechanism. It’s common to adjust batch sizes based on how datastore/service performs under the load.
3. **Network Latency**: If you are loading data over a network, smaller batches might be more efficient due to latency considerations.
4. **Vacuum and Indexing**: After large inserts, datastore might need time to vacuum and update indexes. Consider this when determining your batch size.
5. **Iterative Testing**: Measure the time taken for a few batch sizes, monitor resource consumption (CPU, memory, I/O), and find the sweet spot that balances speed and resource use.


## Comparison of relative imports and absolute imports:

| **Criterion**                  | **Absolute Import**                                        | **Relative Import**                                         |
|--------------------------------|------------------------------------------------------------|-------------------------------------------------------------|
| **Example**                    | `from model.load_model import ModelLoader`                 | `from ..model.load_model import ModelLoader`                |
| **Project Size**               | Ideal for large projects or libraries meant for reuse.     | Suitable for small, self-contained packages.                |
| **Readability**                | Clearer and easier to understand.                          | Can be less clear, especially with deep hierarchies.        |
| **Refactoring and Maintenance**| Easier to maintain when reorganizing or refactoring.       | Can be prone to breakage if files are moved.                |
| **PEP 8 Recommendation**       | Recommended by PEP 8.                                      | Not recommended by PEP 8 for complex projects.              |
| **Development Convenience**    | Requires more typing for deeply nested modules.            | Easier and shorter to write for nested modules.             |
| **Usage Context**              | Good for reusable libraries and top-level scripts.         | Works well inside packages but not for standalone scripts.  |
| **Suitability for Standalone Scripts** | Works well when running scripts directly. | Often fails if running a script directly as `python script.py`. |
| **Ambiguity**                  | Less prone to ambiguity, as the full path is specified.    | More ambiguous, especially when using multiple `..` or `.`. |
| **Clarity of Module Location** | Makes it clear where the module resides.                   | Requires checking directory structure for module location.  |
| **Verbosity**                  | More verbose, especially with deeply nested structures.    | More concise when referring to nearby modules.              |





# troubleshoot

1. ### Issue:
```
python-build 3.12.0 ~/.asdf/installs/python/3.12.0
Downloading Python-3.12.0.tar.xz...
-> https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tar.xz
Installing Python-3.12.0...

BUILD FAILED (Ubuntu 22.04 using python-build 2.4.16)

Inspect or clean up the working tree at /tmp/python-build.20241020212613.426208
Results logged to /tmp/python-build.20241020212613.426208.log

Last 10 log lines:
  File "/tmp/python-build.20241020212613.426208/Python-3.12.0/Lib/ensurepip/__init__.py", line 172, in _bootstrap
    return _run_pip([*args, "pip"], [os.fsdecode(tmp_wheel_path)])
  File "/tmp/python-build.20241020212613.426208/Python-3.12.0/Lib/ensurepip/__init__.py", line 87, in _run_pip
    return subprocess.run(cmd, check=True).returncode
           ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/tmp/python-build.20241020212613.426208/Python-3.12.0/Lib/subprocess.py", line 577, in run
    raise CalledProcessError(retcode, process.args,
                             output=stdout, stderr=stderr)
subprocess.CalledProcessError: Command '['/tmp/python-build.20241020212613.426208/Python-3.12.0/python', '-W', 'ignore::DeprecationWarning', '-c', '\nimport runpy\nimport sys\nsys.path = [\'/tmp/tmpaelzkk6y/pip-24.2-py3-none-any.whl\'] + sys.path\nsys.argv[1:] = [\'install\', \'--no-cache-dir\', \'--no-index\', \'--find-links\', \'/tmp/tmpaelzkk6y\', \'--root\', \'/\', \'--upgrade\', \'pip\']\nrunpy.run_module("pip", run_name="__main__", alter_sys=True)\n']' returned non-zero exit status 1.
make: *** [Makefile:2267: install] Error 1
```
### solution:
It looks like you're encountering a problem while trying to install Python 3.12.0 using `python-build` with `asdf` on Ubuntu 22.04. This error might be due to missing dependencies or configuration issues during the build process. Here are some steps you can take to try to resolve this:

1. **Install Build Dependencies**
Python often requires specific build dependencies. Make sure you have these installed:

```bash
sudo apt update
sudo apt install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
libffi-dev liblzma-dev
```

2. **Clean Up Previous Attempts**
Clean up any previous build artifacts that may have been left behind:

```bash
asdf uninstall python 3.12.0
rm -rf /tmp/python-build.*
```

3. **Try the Installation Again**
Attempt to install Python again:

```bash
asdf install python 3.12.0
```

4. **Check for Logs**
If it fails again, inspect the log file mentioned (`/tmp/python-build.20241020212613.426208.log`) to see if there are any additional clues about missing dependencies or errors during the build process.

5. **Use Python Version Manager**
If `asdf` continues to have trouble, you might try using `pyenv` directly to see if it can build Python 3.12.0 successfully:

```bash
curl https://pyenv.run | bash
# Add pyenv to your shell's init script, e.g., ~/.bashrc
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
source ~/.bashrc
pyenv install 3.12.0
```

6. **Update `asdf` and `python-build`**
Make sure that both `asdf` and `python-build` are up to date, as newer versions might include fixes for this problem:

```bash
asdf update
asdf plugin update python
```

These steps should help you resolve the build issue. If you continue to face difficulties, sharing the contents of the log file might provide more detailed insights.


2. ### Issue:
```
poetry install
Creating virtualenv retail-rag-yG_YMoDp-py3.12 in ~/.cache/pypoetry/virtualenvs
Updating dependencies
Resolving dependencies... (2.7s)

Package operations: 6 installs, 0 updates, 0 removals

  - Installing six (1.16.0)
  - Installing python-dateutil (2.9.0.post0)
  - Installing typing-extensions (4.12.2)
  - Installing dotenv (0.0.5): Preparing...
  - Installing faker (30.6.0)
  - Installing psycopg2 (2.9.10): Failed

  ChefBuildError

  Backend subprocess exited when trying to invoke get_requires_for_build_wheel
  
  running egg_info
  writing psycopg2.egg-info/PKG-INFO
  writing dependency_links to psycopg2.egg-info/dependency_links.txt
  writing top-level names to psycopg2.egg-info/top_level.txt
  
  Error: pg_config executable not found.
  
  pg_config is required to build psycopg2 from source.  Please add the directory
  containing pg_config to the $PATH or specify the full executable path with the
  option:
  
      python setup.py build_ext --pg-config /path/to/pg_config build ...
  
  or with the pg_config option in 'setup.cfg'.
  
  If you prefer to avoid building psycopg2 from source, please install the PyPI
  'psycopg2-binary' package instead.

```
### solution:
The error indicates that the `pg_config` executable, which is required to build `psycopg2` from source, is missing from your environment. Here are a few options to resolve this issue:

**Option 1: Install `libpq-dev` (Recommended for Linux/Ubuntu)**

For Ubuntu or other Debian-based systems, install the `libpq-dev` package, which includes `pg_config`:

```bash
sudo apt-get install libpq-dev
```

Then, try running the `poetry install` command again.

**Option 2: Use `psycopg2-binary`**

If you prefer to avoid building `psycopg2` from source, you can switch to the `psycopg2-binary` package. Update your `pyproject.toml` to use `psycopg2-binary` instead of `psycopg2`:

```toml
[tool.poetry.dependencies]
psycopg2-binary = "^2.9"
```

After updating the file, run:

```bash
poetry install
```

**Option 3: Specify the Path to `pg_config`**

If you have `pg_config` installed but it's not in your `$PATH`, specify its location directly:

```bash
export PATH=$PATH:/path/to/pg_config
```

Replace `/path/to/pg_config` with the directory containing `pg_config`, then run the installation again.

Let me know if any of these solutions work for you!



3. ### Issue:
```
2024-10-24 18:03:31 /app/.venv/lib/python3.12/site-packages/transformers/tokenization_utils_base.py:1601: FutureWarning: clean_up_tokenization_spaces was not set. It will be set to True by default. This behavior will be depracted in transformers v4.45, and will be then set to False by default. For more details check this issue: https://github.com/huggingface/transformers/issues/31884
2024-10-24 18:03:31   warnings.warn(
2024-10-24 18:03:52 Traceback (most recent call last):
2024-10-24 18:03:52   File "/app/generate_embeddings.py", line 113, in <module>
2024-10-24 18:03:52     main()
2024-10-24 18:03:52   File "/app/generate_embeddings.py", line 107, in main
2024-10-24 18:03:52     process_and_store_embeddings(batch_size=1000)
2024-10-24 18:03:52   File "/app/generate_embeddings.py", line 72, in process_and_store_embeddings
2024-10-24 18:03:52     save_embeddings(batch_idx, product_texts, product_embeddings, financial_embeddings, time_embeddings)
2024-10-24 18:03:52   File "/app/generate_embeddings.py", line 90, in save_embeddings
2024-10-24 18:03:52     vector_store.add_embeddings(["financial_vector"] * len(financial_embeddings), financial_embeddings)
2024-10-24 18:03:52   File "/app/vector_store.py", line 37, in add_embeddings
2024-10-24 18:03:52     raise ValueError(
2024-10-24 18:03:52 ValueError: Embedding dimension 4 does not match FAISS index dimension 384
2024-10-24 18:03:52 Generating product embeddings for batch 0...
2024-10-24 18:03:52 Product embeddings for batch 0 generated.
2024-10-24 18:03:52 Financial embeddings for batch 0 generated and normalized.
2024-10-24 18:03:52 Time embeddings for batch 0 generated and normalized.
2024-10-24 18:03:52 Creating new FAISS index...
2024-10-24 18:03:52 FAISS index created.
2024-10-24 18:03:52 Added 1000 embeddings to the index.
2024-10-24 18:03:52 FAISS index saved to /vector_store_data/faiss_index.bin
2024-10-24 18:03:52 Product embeddings for batch 0 added to vector store.
```
### Solution:
The error message indicates that there is a mismatch between the dimensions of the embeddings you are trying to add to the FAISS index:

    Product embeddings have a dimension of 384 (as generated by sentence-transformers), and the FAISS index was initially created to match this dimension.
    Financial embeddings, however, have a dimension of 4 because they include four features: quantity, unit_price, price, and discount_applied.

FAISS requires that all vectors stored in the same index have the same dimensionality. Since the product embeddings and financial embeddings have different dimensions, they should be stored in separate FAISS indices.
Solution: Store Each Embedding Type in Separate FAISS Indices

We can modify the script to create separate FAISS indices for each embedding type. This allows for storing product-related, financial, and time-based vectors independently.

Key Changes:

    Separate FAISS Indices:
        Created three separate FAISS indices for product, financial, and time embeddings.
        Each index is initialized with the appropriate dimension (384 for product, 4 for financial, and 1 for time).
    Dimension Check:
        Added validation to ensure the embeddings match the index's expected dimension before adding them.
    Multiple Index Management:
        Managed multiple indices within VectorStore and handled saving/loading each index separately.
        