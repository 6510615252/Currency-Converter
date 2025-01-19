# Command Line Application 

## Overview 
This project is a command-line application built with Python, using the Alpha Vantage API to fetch financial data. It allows users to retrieve exchange rates data, such as daily, weekly, or monthly rates, and view the supported currencies. The application is containerized using Docker.

## Command 
  - **cli-exc help** - display available subcommands/options
  - **cli-exc list [OPTIONS]** - display supported currencies
  - **cli-exc realtime** (from) (to) (amount)** - fetch realtime exchange rates
  - **cli-exc daily** (date) (from) (to) (amount) - fetch daily exchange rates
  - **cli-exc weekly** (week) (from) (to) (amount) - fetch weekly exchange rates
  - **cli-exc monthly** (month) (from) (to) (amount) - fetch monthly exchange rates
  - **cli-exc volatile** (period) (from) (to)** - fetch volatile weekly or monthly
  
  
## Setup 
1. **Clone the Repository:**
   ```sh
   git clone https://github.com/cn330/g01-67_01.git G01_CLA
   cd G01_CLA
   ```

2. **Create and Activate a Virtual Environment:**
   ```sh
   python -m venv .venv
   source .venv/bin/activate  
   ```

   On Windows use
   ```sh
   .venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Install the Application in Editable Mode:**
   ```sh
   pip install -e .
   ```

5. **Using the Application:**
   - To check available commands, run:
     ```sh
     cli-exc help
     cli-exc list
     ```
   - To fetch the exchange rates Realtime, use:
     ```sh
     cli-exc realtime FROM_CURRENCY TO_CURRENCY [OPTIONS]
     
   - To fetch the exchange rates for a specific period, use:
     ```sh
     cli-exc monthly [OPTIONS] FROM_CURRENCY TO_CURRENCY [MONTH]
     cli-exc weekly [OPTIONS] FROM_CURRENCY TO_CURRENCY [DATE]
     cli-exc daily [OPTIONS] FROM_CURRENCY TO_CURRENCY [DATE]
     ```
   - e.g. convert 100 USD to THB using monthly exchange rates
      ```
      cli-exc monthly usd thb 2024-11 --convert --amount 100
      ```

## Docker Setup
The application is containerized with Docker. You can use Docker Compose to run it in a containerized environment. 

1. **Build and Run with Docker Compose:**
   ```sh
   docker-compose up --detach
   ```

2. **To enter a Docker container in interactive mode:**
   ```
   docker exec -it g01-67_01 /bin/bash
   ```   
