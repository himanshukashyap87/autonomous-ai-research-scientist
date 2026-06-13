# 🧠 Autonomous AI Research Scientist

An end-to-end Autonomous AI Research Scientist built in Python that can search research papers, summarize findings, identify research gaps, generate novel hypotheses, design experiments, and produce research insights automatically.

---

## 🚀 Project Overview

The goal of this project is to simulate the workflow of a human research scientist using AI agents.

Given a research topic, the system can:

1. Search academic papers from arXiv.
2. Download and process research papers.
3. Generate concise research summaries.
4. Identify limitations and research gaps.
5. Propose novel research hypotheses.
6. Design experiments to validate hypotheses.
7. Generate structured research reports.

This project combines Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), Knowledge Graphs, and Multi-Agent AI systems.

---

## 🏗️ Architecture

```text
User Research Topic
         │
         ▼
 ┌─────────────────┐
 │ Search Agent    │
 └─────────────────┘
         │
         ▼
 ┌─────────────────┐
 │ Summarize Agent │
 └─────────────────┘
         │
         ▼
 ┌─────────────────┐
 │ Gap Agent       │
 └─────────────────┘
         │
         ▼
 ┌─────────────────┐
 │ Hypothesis Agent│
 └─────────────────┘
         │
         ▼
 ┌─────────────────┐
 │ Experiment Agent│
 └─────────────────┘
         │
         ▼
 ┌─────────────────┐
 │ Report Agent    │
 └─────────────────┘
         │
         ▼
    Final Research
        Report
```

---

## ✨ Features

### Research Discovery

* arXiv paper search
* Paper metadata extraction
* Automatic PDF download

### Research Understanding

* AI-powered paper summarization
* Research problem extraction
* Methodology identification
* Limitation analysis

### Research Intelligence

* Research gap detection
* Novel hypothesis generation
* Scientific reasoning support

### Experiment Design

* Automated experiment planning
* Baseline comparison generation
* Evaluation metric suggestion
* Risk assessment

### Future Enhancements

* RAG-based question answering
* Knowledge Graph generation
* Multi-paper reasoning
* Streamlit web interface
* Automated PDF report generation

---

## 📂 Project Structure

```text
autonomous-ai-research-scientist/
│
├── agents/
│   ├── search_agent.py
│   ├── summarize_agent.py
│   ├── gap_agent.py
│   ├── hypothesis_agent.py
│   ├── experiment_agent.py
│   └── report_agent.py
│
├── config/
│   └── settings.py
│
├── data/
│   └── papers/
│
├── graph/
│   └── research_graph.py
│
├── rag/
│   ├── embeddings.py
│   ├── retrieval.py
│   └── chroma_store.py
│
├── utils/
│   ├── arxiv_loader.py
│   ├── paper_downloader.py
│   ├── semantic_scholar.py
│   └── pdf_generator.py
│
├── app.py
├── requirements.txt
└── Dockerfile
```

---

## 🛠️ Technology Stack

### Programming Language

* Python

### AI Models

* OpenRouter
* OpenAI-compatible APIs
* Gemini API (optional)

### Research Sources

* arXiv
* Semantic Scholar

### NLP & ML

* Transformers
* Sentence Transformers
* Hugging Face

### Vector Database

* ChromaDB

### Knowledge Representation

* NetworkX
* Knowledge Graphs

### Deployment

* Docker
* Streamlit (planned)

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/himanshukashyap87/autonomous-ai-research-scientist.git

cd autonomous-ai-research-scientist
```

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
OPENROUTER_API_KEY=YOUR_API_KEY
```

---

## ▶️ Usage

### Search Papers

```bash
python agents/search_agent.py
```

### Generate Summaries

```bash
python agents/summarize_agent.py
```

### Find Research Gaps

```bash
python agents/gap_agent.py
```

### Generate Hypotheses

```bash
python agents/hypothesis_agent.py
```

### Design Experiments

```bash
python agents/experiment_agent.py
```

### Generate Final Report

```bash
python agents/report_agent.py
```

---

## 📈 Current Development Status

* Search Agent ✅
* Summarization Agent ✅
* Gap Analysis Agent ✅
* Hypothesis Generation Agent ✅
* Experiment Design Agent ✅
* GitHub Integration ✅
* Report Agent 🔄
* RAG Pipeline 🔄
* Knowledge Graph 🔄
* Streamlit Dashboard 🔄

---

## 🎯 Future Roadmap

### Phase 1

* Complete report generation
* Improve experiment planning
* Better scientific reasoning

### Phase 2

* RAG integration
* ChromaDB vector search
* Semantic retrieval

### Phase 3

* Knowledge graph generation
* Multi-paper reasoning
* Citation-aware responses

### Phase 4

* Streamlit UI
* Docker deployment
* Public demo

---

## 👨‍💻 Author

**Himanshu Raj**

AI & Machine Learning Enthusiast

Building autonomous systems for scientific discovery using Python, LLMs, and multi-agent AI.
