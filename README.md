# Inventory Management System (Flask REST API)

## Overview
This project is a Flask-based REST API and CLI inventory management system built for a bootcamp summative lab. It allows employees to create, read, update, and delete inventory items, while also integrating with the Open Food Facts API to fetch real-world product details.

## Features
- Flask REST API
- CRUD inventory routes
- External API integration with Open Food Facts
- CLI interface for interacting with the API
- Unit tests with pytest and mocks
- Mock in-memory data storage using a Python list

## Technologies Used
- Python
- Flask
- Requests
- Pytest
- unittest.mock

## Project Structure
- `app.py` → Flask API
- `store.py` → mock database array
- `external_api.py` → external API integration
- `cli.py` → command-line interface
- `tests/` → automated tests

## Installation
1. Clone the repository:
```bash
git clone <your-repo-url>
cd inventory-management-system
