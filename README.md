# INF438 - Advanced Databases Course Projects

Three assignments covering big data processing: local Hadoop clusters, MapReduce analytics, and cloud data lakes on AWS.

## Overview

- **hadoop-docker-lab** - Local Hadoop cluster setup with Docker (HDFS, YARN, MapReduce)
- **Devoir 2** - MapReduce analysis of NYC CitiBike data (577K records)
- **Devoir 3** - AWS serverless data lake with Lambda, S3, and Athena

---

## Repository Structure

```
INF438/
├── hadoop-docker-lab/          # Foundational Hadoop setup
├── Devoir2/                     # MapReduce batch analytics
├── Devoir3/                     # AWS serverless data lake
└── README.md                    # This file
```

---

## Assignments

### 1. hadoop-docker-lab

Local Hadoop cluster setup using Docker Compose.

**Technologies:** Docker, Hadoop 3.2.1, HDFS, YARN, Python Streaming

**Services:** NameNode, DataNode, ResourceManager, NodeManager, HistoryServer

**Tasks:**
- Cluster setup and configuration
- HDFS operations (upload, list, retrieve files)
- Basic MapReduce example (WordCount)
- Job monitoring via web interfaces

---

### 2. Devoir 2 - CitiBike MapReduce Analysis

MapReduce analysis of NYC CitiBike trip data (577,704 records).

**Technologies:** Hadoop Streaming, Python mappers/reducers, Matplotlib

**Analyses:**
1. Top departure stations (W 20 St & 11 Ave: 5,983 trips)
2. User type comparison (Subscribers: 337K trips, 18min avg; Customers: 240K trips, 29min avg)
3. Hourly activity patterns (Peak at 18:00 with 53,915 trips)

**Files:**
- `mapper1.py`, `reducer1.py` - Station analysis
- `mapper2.py`, `reducer2.py` - User type analysis
- `mapper3.py`, `reducer3.py` - Hourly patterns
- Result visualizations in `deliverables/`

---

### 3. Devoir 3 - AWS Data Lake

Serverless data pipeline with AWS services.

**Technologies:** AWS S3, Lambda, Athena; Python (boto3, pandas, matplotlib); JSON/JSON Lines

**Pipeline:**
```
Generate orders (500 records)
    ↓
S3 raw/ (upload)
    ↓
Lambda (transform: uppercase, calculate totals)
    ↓
S3 processed/ (JSON + JSON Lines)
    ↓
Athena (SQL queries)
    ↓
Python analysis (visualization)
```

**Queries:**
1. Display all orders
2. Total order count
3. Orders by city
4. Revenue by country
5. Top 5 products

**Files:**
- `generate_data.py` - Synthetic data generator
- `lambda_function.py` - ETL transformation
- `s3_select_queries.txt` - SQL queries
- `sales_analysis.py` - Analysis and visualization
- `plots/sales_analysis.png` - Dashboard

---

## Technologies Used

| Category | Tools |
|----------|-------|
| **Big Data** | Hadoop, HDFS, YARN, MapReduce |
| **Cloud** | AWS S3, Lambda, Athena |
| **Containers** | Docker, Docker Compose |
| **Languages** | Python 3 |
| **Libraries** | boto3, pandas, matplotlib |
| **Data Formats** | CSV, JSON, JSON Lines |

---

## Documentation

Assignment instructions in each directory:
- `hadoop-docker-lab/document/` - Setup guide
- `Devoir2/document/` - MapReduce specifications
- `Devoir3/document/` - AWS project requirements
