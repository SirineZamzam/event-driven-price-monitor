### Event-Driven Price Monitoring System
## Overview
-This project is a modular backend system that monitors product prices from external APIs, detects significant changes, and generates structured decisions through a background processing pipeline.

-It demonstrates event-driven architecture, database modeling, and layered backend design.

## Architecture
External API
     ↓
Ingestion Layer (fetch_price.py)
     ↓
Events Table (PostgreSQL)
     ↓
Background Worker (process_events.py)
     ↓
Decision Logic + AI Abstraction Layer
     ↓
Decisions Table
     ↓
FastAPI REST API

## Tech Stack
-Python

-PostgreSQL

-FastAPI

-Requests

-Event-driven worker pattern

## Features
-Monitors multiple products

-Detects significant price changes (threshold-based)

-Stores historical events

-Background worker processes unprocessed events

-Abstracted AI layer (mocked for development)

-REST API to retrieve events and decisions

-Scheduler for automated continuous monitoring

## Design Decisions
1. Layered Architecture
Separated ingestion, processing, AI logic, and API for modularity and scalability.

2. Event-Driven Pattern
Price changes generate events which are processed asynchronously.

3. Replaceable AI Layer
AI summarization is abstracted behind an interface, allowing easy swap between mock logic and real models.

4. Threshold Filtering
Prevents noise by ignoring minor price fluctuations (<5%).

## How to Run
1. Install dependencies
pip install -r requirements.txt
2. Run scheduler
python -m app.scheduler
3. Run API
uvicorn app.api.main:app --reload

## Future Improvements
-Historical trend analysis

-Forecasting model

-Deployment to cloud

-Containerization (Docker)

-Replace mock AI with local LLM or hosted model

## What This Project Demonstrates
-Backend system design

-Relational data modeling

-Background worker patterns
-External API integration-Modular architecture thinking
