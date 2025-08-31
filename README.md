# Q5 – Real-Time Data Pipeline Prototype

This repository contains a prototype of a streaming pipeline implemented in pure Python using standard libraries.

## Components

- `producer`: Simulates streaming data ingestion (~200 posts/sec).
- `cleaner`: Performs basic normalization (e.g., lowercasing and trimming text).
- `scorer`: Computes a dummy “score” for each post (simulated using MD5).
- `sink`: An idempotent sink preventing duplicates, based on post ID and timestamp.

## How to run

```bash
python Q5.py

## Output
inflight:0 unique_writes: 131
