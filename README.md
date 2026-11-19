# TDM 202: Applied Data Engineering & Analytics Portfolio

**Niharika Rai** · Purdue University · The Data Mine (Corporate Partners Program) · Spring 2026

This repository holds the 11 projects I completed for **TDM 202**, the second-semester seminar of Purdue's [Data Mine](https://datamine.purdue.edu/) learning community. Each project is a Jupyter notebook that runs on **Anvil**, Purdue's NSF-funded high-performance computing cluster. The projects work with real datasets: millions of NYC taxi trips, 60,000 handwritten-digit images, and 120 years of Olympic results.

Together they cover the main stages of a modern data workflow:

> **Collect** data from the web and from APIs → **Process** it at scale → **Model and optimize** → **Visualize** the results → **Serve** them through a REST API → **Package** the work in containers so it can be reproduced

---

## Technical Skills at a Glance

| Area | Tools & Concepts |
|---|---|
| **Languages** | Python, Bash, SQL-style query logic, HTML/XPath/CSS selectors |
| **Data Processing** | Polars (lazy and streaming engines), Pandas, NumPy, Apache Arrow / Parquet |
| **Machine Learning Foundations** | PyTorch tensors, broadcasting, matrix multiplication, data normalization |
| **Optimization & Modeling** | SciPy (`minimize`, BFGS, SLSQP), constrained optimization, linear programming, least-squares curve fitting |
| **Web Data Collection** | `requests`, `lxml`, XPath, CSS selectors, pagination, sessions, `robots.txt` compliance |
| **Reliability Engineering** | Rate limiting, exponential backoff with jitter, retry logic, structured logging |
| **Backend / APIs** | FastAPI, Pydantic validation, RESTful design, CRUD, HTTP status codes, pagination |
| **Visualization** | Plotly Express, Matplotlib, ipywidgets (interactive dashboards) |
| **DevOps / HPC** | Apptainer (Singularity) containers, definition files, bind mounts, shell scripting, Linux on an HPC cluster |
| **Practices** | Reproducible experiments, configuration-driven design, performance benchmarking, debugging, documentation |

---

## Highlights

- **Benchmarked Polars against Pandas on 4.25 million rows (~571 MB) of NYC taxi data.** The same cost-breakdown calculation took **~0.01 s with Polars lazy evaluation and ~0.20 s with Pandas, roughly 20× faster**. I read the query plans to see why: predicate pushdown and projection pushdown.
- **Built a reusable `RobustScraper` class** that combines rate limiting, exponential backoff with jitter, rotating User-Agent headers, persistent sessions, `robots.txt` checks, and logging. These are the same reliability patterns production data-ingestion services use.
- **Implemented a REST API in FastAPI** with full CRUD, PATCH partial updates, pagination, and Pydantic request validation (bad input is rejected with a `422`). The code is in [`main.py`](main.py).
- **Containerized a Python workload with Apptainer** on an HPC cluster. Inputs come from a config file and outputs go through bind mounts, so experiments are reproducible and do not require rebuilding the image.
- **Solved a resource-allocation (production planning) problem** with constrained optimization. The model found the profit-maximizing product mix ($780) under labor and material limits.
- **Built a multi-tab interactive Olympics dashboard** using ipywidgets and Plotly. It has dropdowns, range sliders, multi-select filters, and chart-type toggles.

---

## Project Breakdown

### 1. Web Scraping Fundamentals: HTML Parsing with XPath & CSS
📓 [`Niharika_Rai_TDM202_project1.ipynb`](Niharika_Rai_TDM202_project1.ipynb)

- Parsed HTML documents into element trees with `lxml` and extracted titles, headings, paragraphs, links, and attributes.
- Wrote **XPath** queries (`//tag[@attr='value']`, `contains()`, relative `.//` paths) and **CSS selectors** for the same tasks, and compared the two approaches.
- Converted nested and tabular HTML (quotes, tags, tables, product listings) into structured Python data: lists of dictionaries and name → URL mappings.
- Used `zip()` to pair related elements, and parsed CSS class names to get values such as star ratings.

**Skills:** HTML DOM structure, XPath, CSS selectors, data structuring

### 2. Scraping Live Websites: Requests, Pagination & Link Crawling
📓 [`Niharika_Rai_webscraping_project2.ipynb`](Niharika_Rai_webscraping_project2.ipynb)

- Fetched live pages with `requests`, checked HTTP status codes, and parsed the responses.
- Used browser developer tools to inspect page structure and design selectors for real sites.
- Wrote a **pagination crawler** that follows "Next" links until none are left. It collected **100 quotes from 10 pages**, each with its text, author, and tags.
- Resolved relative links to absolute URLs with `urljoin`, built author → profile-URL and tag → URL indexes, and removed duplicate tags.

**Skills:** HTTP requests, crawling, pagination, URL handling, data cleaning

### 3. Responsible & Robust Scraping: Production-Grade Patterns
📓 [`Niharika_Rai_webscraping_project3.ipynb`](Niharika_Rai_webscraping_project3.ipynb)

- **Rate limiting:** added fixed delays between requests and timed the run (5 pages in ~10.7 s, about 2.1 s per request).
- **Fault tolerance:** wrote **exponential backoff with random jitter** to retry after `429 Too Many Requests` and `503 Service Unavailable` responses and after network timeouts.
- **Session management:** used `requests.Session` to keep cookies between requests, and rotated **User-Agent headers** for each request.
- **Ethics and compliance:** parsed `robots.txt` with `urllib.robotparser` to check whether a path may be crawled and whether the site sets a crawl delay. I tested it on several sites, including one that disallows scraping.
- **Capstone:** combined all of these features in an object-oriented **`RobustScraper` class** with structured `logging`. It scraped 50 quotes from multiple pages.

**Skills:** Resilient system design, OOP, logging, retry/backoff strategies, ethical data collection

### 4. Interactive Data Visualization: Olympic History Dashboard
📓 [`Niharika_Rai_visualization_project4.ipynb`](Niharika_Rai_visualization_project4.ipynb)

- Explored the **120-year Olympic athlete dataset** with Pandas: filtering, `groupby` aggregations, and medal counts by country, year, and medal type.
- Built interactive widgets with **ipywidgets + Plotly Express**:
  - **Medals panel:** pick a country from a dropdown to see its medal history.
  - **Physical traits panel:** histograms of athlete age, height, or weight over a year range chosen with a slider.
  - **Sports panel:** pick several sports and a season (Summer/Winter), then switch between bar and line charts.
- Combined the panels into one **tabbed dashboard** with custom styling and handled empty selections without errors.

**Skills:** Exploratory data analysis, event-driven UI, dashboard design, data storytelling

### 5. PyTorch Tensors: Foundations for Deep Learning
📓 [`Niharika_Rai_PyTorch_Tensors_project5.ipynb`](Niharika_Rai_PyTorch_Tensors_project5.ipynb)

- Loaded the **MNIST** dataset (60,000 images × 784 pixels) and converted it from a Pandas DataFrame to a NumPy array to PyTorch tensors, with the correct dtypes (`float32` and `int64`).
- Reshaped flat pixel vectors into image tensors `[N, 1, 28, 28]` and displayed digits with Matplotlib.
- Did element-wise arithmetic, comparisons, and logical operations on tensors.
- Wrote **per-image standardization** (z-score normalization) by hand using **broadcasting**, and checked the results against PyTorch's and NumPy's built-in functions.
- Applied a random linear projection to the full dataset with **matrix multiplication** (`[60000×784] @ [784×10]`), the same operation a neural-network layer performs.

**Skills:** Tensor operations, broadcasting, linear algebra, ML data preprocessing

### 6. High-Performance Data Processing with Polars
📓 [`Niharika_Rai_Polars_project6.ipynb`](Niharika_Rai_Polars_project6.ipynb)

- Analyzed **4,251,015 NYC Yellow Taxi trips** (Sept 2025, Parquet, ~571 MB in memory).
- Wrote reusable Polars **expressions**, including tip percentage, conditional logic with `when/then/otherwise`, and trip-distance categories, plus derived features such as trip duration.
- Used **lazy evaluation** (`.lazy()`, `scan_parquet`) and read optimized query plans with `.show_graph()` to find predicate and projection pushdown.
- Ran queries on the **streaming engine**, which handles data larger than RAM by processing it in chunks.
- **Benchmarked** eager, lazy, and streaming Polars against Pandas. Polars lazy was **~20× faster** than Pandas for the same calculation.
- Explained the role of the **Apache Arrow columnar format** and zero-copy data sharing.

**Skills:** Big-data processing, query optimization, performance benchmarking, columnar storage

### 7. Mathematical Optimization with SciPy
📓 [`Niharika_Rai_Optimization_project8.ipynb`](Niharika_Rai_Optimization_project8.ipynb)

- Found minima of 1-D and 2-D objective functions with **BFGS**, and checked the results against plots and contour maps.
- Solved **constrained problems** with **SLSQP**, shaded feasible regions on plots, and showed how constraints move the optimum.
- Modeled a **production-planning business problem**: maximize profit across two products under labor and material limits. Optimal plan: **36 units of A and 28 of B, $780 profit**, using 100% of both resources.
- Fit a regression line to noisy data by **minimizing the sum of squared errors**, the same idea behind least-squares regression in machine learning.

**Skills:** Operations research, linear programming, numerical optimization, model fitting

### 8. REST APIs with FastAPI
📓 [`Niharika_Rai_APIs_project9.ipynb`](Niharika_Rai_APIs_project9.ipynb) · 🐍 [`main.py`](main.py)

- Called public APIs (httpbin, JSONPlaceholder) and compared query parameters with JSON request bodies.
- **Built a REST API with FastAPI** (`main.py`) that has:
  - Health-check and info endpoints for service monitoring
  - Full **CRUD** (`GET`, `POST`, `PUT`, `DELETE`) with correct status codes (`400`, `404`)
  - **Pydantic models** that validate request bodies (bad input is rejected with `422`)
  - **PATCH** partial updates using `exclude_unset`
  - **Paginated** list endpoints (`skip` / `limit`)
- Tested every endpoint with Python `requests` and `curl`, including error cases.
- Explained REST principles, how CRUD operations map to HTTP methods, and when to use PUT versus PATCH.

**Skills:** Backend development, API design, data validation, HTTP

### 9. Containers on HPC: Apptainer Fundamentals
📓 [`Niharika_Rai_Containers1_project10.ipynb`](Niharika_Rai_Containers1_project10.ipynb)

- Wrote an **Apptainer definition file** (`Bootstrap`, `From`, `%files`, `%post`, `%runscript`) to build a Python 3.11 image from a Docker registry.
- Built and ran the containerized app, sent its output to log files, and checked the image metadata and target architecture (`amd64`).
- Used **bind mounts** so code changes show up inside the container without a rebuild.
- Compared containers with virtual machines and explained why Apptainer suits shared HPC systems: it runs without root and works with job schedulers.

**Skills:** Containerization, Linux, HPC environments, reproducible builds

### 10. Containerized Workflows: Reproducible Experiments & Debugging
📓 [`Niharika_Rai_Containers2_project11.ipynb`](Niharika_Rai_Containers2_project11.ipynb)

- Ran a **config-driven Monte Carlo experiment** (estimating π over 5 runs × 10,000 samples) inside a container. Parameters came from `config.json`, and results were written to `results.json`.
- Kept the experiment logic (`analyze.py`) separate from the computation (`workload.py`) so each part can be maintained or swapped on its own.
- **Debugged failing container jobs**: fixed wrong bind-mount paths and a missing environment variable (`RUN_MODE`) by reading the stack traces.
- Wrote a **portable Bash wrapper script** (`run_analysis.sh`) that works from any directory, and confirmed it succeeds by checking its exit code.

**Skills:** Reproducible research, configuration management, debugging, shell scripting, batch workflows

---

## Repository Structure

```
tdm202/
├── README.md
├── main.py                                       # FastAPI REST service (Project 9)
├── Niharika_Rai_TDM202_project1.ipynb            # HTML parsing: XPath & CSS
├── Niharika_Rai_webscraping_project2.ipynb       # Live scraping & pagination
├── Niharika_Rai_webscraping_project3.ipynb       # Robust & ethical scraping
├── Niharika_Rai_visualization_project4.ipynb     # Interactive Olympics dashboard
├── Niharika_Rai_PyTorch_Tensors_project5.ipynb   # PyTorch tensors on MNIST
├── Niharika_Rai_Polars_project6.ipynb            # Polars at scale on NYC taxi data
├── Niharika_Rai_Optimization_project8.ipynb      # SciPy optimization
├── Niharika_Rai_APIs_project9.ipynb              # REST APIs with FastAPI
├── Niharika_Rai_Containers1_project10.ipynb      # Apptainer fundamentals
└── Niharika_Rai_Containers2_project11.ipynb      # Containerized reproducible workflows
```

---

## Running the Code

The notebooks were written for Purdue's **Anvil** cluster, and several of them read datasets stored there (`/anvil/projects/tdm/data/...`). To run them elsewhere, change those paths to local copies of the public datasets (NYC TLC trip records, MNIST, and the Kaggle "120 Years of Olympic History" dataset). The scraping and API notebooks run anywhere with internet access.

**Run the FastAPI service locally:**

```bash
pip install fastapi uvicorn pydantic
```

```bash
uvicorn main:app --reload
```

Then open `http://127.0.0.1:8000/docs` for FastAPI's auto-generated interactive documentation.

---

## About the Course

TDM 202 (1 credit hour) continues TDM 201 and is required for students in The Data Mine's **Corporate Partners Program**, where students work on applied data science projects with industry sponsors. The seminar teaches the practical engineering skills those projects need: getting data, processing it efficiently at scale, building services, and making work reproducible.

Each project began with a guided prompt and starter code. I extended the code, debugged it, wrote my own examples, and explained the concepts in writing. Following Purdue's academic integrity standards, every notebook documents the outside resources I used, including AI tools I used for debugging and checking my understanding.

---

## Contact

I'm looking for **internship and entry-level roles in data science, data engineering, analytics, and software engineering**. I'd love to connect.

- **GitHub:** [github.com/Niharika-Rai](https://github.com/Niharika-Rai)
- **LinkedIn:** *add your LinkedIn URL here*
- **Email:** *add your preferred contact email here*
