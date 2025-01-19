import httpx
import os
import requests
import typer
from datetime import datetime, timedelta
import statistics

# DOC https://www.alphavantage.co/documentation/#digital-currency
API_KEY = " WKZDF65B0XDR1BH5" #Kasidit's Key
BASE_URL = "https://www.alphavantage.co/query"

def fetch_fx_data_currency(function: str, from_symbol="USD", to_symbol="THB"):
    params = {
        "function": function,
        "from_currency": from_symbol,
        "to_currency": to_symbol,
        "apikey": API_KEY,
    }
    
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()

def fetch_fx_data_symbol(function: str, from_symbol="USD", to_symbol="THB"):
    params = {
        "function": function,
        "from_symbol": from_symbol,
        "to_symbol": to_symbol,
        "apikey": API_KEY,
    }
    
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()

def fetch_currency_list(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.text
            json_data = convert_csv_to_list_json(data)
            return json_data
        except ValueError:
            typer.echo("Response is not valid.")
            return []
    else:
        typer.echo(f"Failed to fetch, Status code: {response.status_code}")
        return []

def fetch_fx_daily(from_symbol, to_symbol, date=None):
    params = {
        "function": "FX_DAILY",
        "from_symbol": from_symbol,
        "to_symbol": to_symbol,
        "outputsize": "full", 
        "apikey": API_KEY,
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    try:
        time_series = data["Time Series FX (Daily)"]
        if date:
            if date in time_series:
                selected_data = time_series[date]
                rate = selected_data["4. close"]
                return float(rate)
            else:
                raise ValueError(f"ไม่มีข้อมูลสำหรับวันที่ {date}")
        else:
            #ไม่ได้ระบุวันที่ ให้ใช้วันที่ล่าสุด
            latest_date = next(iter(time_series))
            latest_data = time_series[latest_date]
            rate = latest_data["4. close"]
            return float(rate)

    except KeyError:
        raise ValueError("ไม่สามารถดึงอัตราแลกเปลี่ยนได้")
    
def fetch_fx_weekly(from_symbol, to_symbol, date=None):
    params = {
        "function": "FX_WEEKLY",
        "from_symbol": from_symbol,
        "to_symbol": to_symbol,
        "outputsize": "full", 
        "apikey": API_KEY,
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    try:
        time_series = data["Time Series FX (Weekly)"]
        if date:
            if date in time_series:
                selected_data = time_series[date]
                rate = selected_data["4. close"]
                return float(rate)
            else:
                raise ValueError(f"ไม่มีข้อมูลสำหรับวันที่ {date}")
        else:
            #ไม่ได้ระบุวันที่ ให้ใช้วันที่ล่าสุด
            latest_date = next(iter(time_series))
            latest_data = time_series[latest_date]
            rate = latest_data["4. close"]
            return float(rate)

    except KeyError:
        raise ValueError("ไม่สามารถดึงอัตราแลกเปลี่ยนได้")

def fetch_fx_monthly(from_symbol, to_symbol, year_month=None):
    params = {
        "function": "FX_MONTHLY",
        "from_symbol": from_symbol,
        "to_symbol": to_symbol,
        "outputsize": "full", 
        "apikey": API_KEY,
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    try:
        time_series = data["Time Series FX (Monthly)"]  
        if year_month:
            filtered_data = {
                date: values
                for date, values in time_series.items()
                if date.startswith(year_month)
            }            
            if not filtered_data:
                raise ValueError(f"ไม่มีข้อมูลสำหรับเดือน {year_month}")
            
            selected_date, selected_data = next(iter(filtered_data.items()))
            rate = selected_data["4. close"]
            return float(rate)
        
        else:
            # หากไม่ได้ระบุเดือน ให้ใช้ข้อมูลเดือนล่าสุด
            latest_date = next(iter(time_series))
            latest_data = time_series[latest_date]
            rate = latest_data["4. close"]
            return float(rate)

    except KeyError:
        raise ValueError("ไม่สามารถดึงอัตราแลกเปลี่ยนได้")
    
def fetch_max_min_weekly(from_symbol, to_symbol, date=None):
    data = fetch_fx_data_symbol("FX_DAILY", from_symbol=from_symbol, to_symbol=to_symbol)
    try :
        time_series = data["Time Series FX (Daily)"]
        today = datetime.now()
        dates_to_fetch = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
        close_values = []
        date_values = []
        missing_dates = []
        
        for date in dates_to_fetch:
            if date in time_series:
                close_values.append(float(time_series[date]["4. close"]))
                date_values.append(date)
            else:
                missing_dates.append(date)
        if missing_dates:
            print(f"ไม่มีข้อมูลสำหรับวันที่: {', '.join(missing_dates)}")
            
        if len(close_values) < 1:
            raise ValueError("ไม่สามารถหาค่า max และ min ได้ เนื่องจากข้อมูลไม่เพียงพอ")
        
        max_values = max(close_values)
        max_date = date_values[close_values.index(max_values)]

        min_vlaues = min(close_values)
        min_date = date_values[close_values.index(min_vlaues)]
        
        return [max_values, max_date, min_vlaues, min_date]
    
    except KeyError:
        # หากโครงสร้างข้อมูลผิดพลาด
        raise ValueError("ไม่สามารถดึงข้อมูลอัตราแลกเปลี่ยนได้")
    
def fetch_max_min_monthly(from_symbol, to_symbol, date=None):
    data = fetch_fx_data_symbol("FX_DAILY", from_symbol=from_symbol, to_symbol=to_symbol)
    try :
        time_series = data["Time Series FX (Daily)"]
        today = datetime.now()
        dates_to_fetch = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)]
        close_values = []
        date_values = []
        missing_dates = []
        
        for date in dates_to_fetch:
            if date in time_series:
                close_values.append(float(time_series[date]["4. close"]))
                date_values.append(date)
            else:
                missing_dates.append(date)
        if missing_dates:
            print(f"ไม่มีข้อมูลสำหรับวันที่: {', '.join(missing_dates)}")
            
        if len(close_values) < 1:
            raise ValueError("ไม่สามารถหาค่า max และ min ได้ เนื่องจากข้อมูลไม่เพียงพอ")
        
        max_values = max(close_values)
        max_date = date_values[close_values.index(max_values)]

        min_vlaues = min(close_values)
        min_date = date_values[close_values.index(min_vlaues)]
        
        return [max_values, max_date, min_vlaues, min_date]
    
    except KeyError:
        # หากโครงสร้างข้อมูลผิดพลาด
        raise ValueError("ไม่สามารถดึงข้อมูลอัตราแลกเปลี่ยนได้")

def convert_csv_to_list_json(text):
    text = text.strip().split("\n")

    # แยก "currency code" และ "currency name"
    result = []

    for row in text[1:]:
        row = row.strip().split(",")
        result.append([row[0], row[1]])

    return result

def fetch_fx_daily(from_symbol, to_symbol, date=None):
    params = {
        "function": "FX_DAILY",
        "from_symbol": from_symbol,
        "to_symbol": to_symbol,
        "outputsize": "full", 
        "apikey": API_KEY,
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    try:
        time_series = data["Time Series FX (Daily)"]
        if date:
            if date in time_series:
                selected_data = time_series[date]
                rate = selected_data["4. close"]
                return float(rate)
            else:
                raise ValueError(f"ไม่มีข้อมูลสำหรับวันที่ {date}")
        else:
            #ไม่ได้ระบุวันที่ ให้ใช้วันที่ล่าสุด
            latest_date = next(iter(time_series))
            latest_data = time_series[latest_date]
            rate = latest_data["4. close"]
            return float(rate)

    except KeyError:
        raise ValueError("ไม่สามารถดึงอัตราแลกเปลี่ยนได้")
    
def fetch_fx_weekly(from_symbol, to_symbol, date=None):
    params = {
        "function": "FX_WEEKLY",
        "from_symbol": from_symbol,
        "to_symbol": to_symbol,
        "outputsize": "full", 
        "apikey": API_KEY,
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    try:
        time_series = data["Time Series FX (Weekly)"]
        if date:
            if date in time_series:
                selected_data = time_series[date]
                rate = selected_data["4. close"]
                return float(rate)
            else:
                raise ValueError(f"ไม่มีข้อมูลสำหรับวันที่ {date}")
        else:
            #ไม่ได้ระบุวันที่ ให้ใช้วันที่ล่าสุด
            latest_date = next(iter(time_series))
            latest_data = time_series[latest_date]
            rate = latest_data["4. close"]
            return float(rate)

    except KeyError:
        raise ValueError("ไม่สามารถดึงอัตราแลกเปลี่ยนได้")

def fetch_fx_monthly(from_symbol, to_symbol, year_month=None):
    params = {
        "function": "FX_MONTHLY",
        "from_symbol": from_symbol,
        "to_symbol": to_symbol,
        "outputsize": "full", 
        "apikey": API_KEY,
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    try:
        time_series = data["Time Series FX (Monthly)"]  
        if year_month:
            filtered_data = {
                date: values
                for date, values in time_series.items()
                if date.startswith(year_month)
            }            
            if not filtered_data:
                raise ValueError(f"ไม่มีข้อมูลสำหรับเดือน {year_month}")
            
            selected_date, selected_data = next(iter(filtered_data.items()))
            rate = selected_data["4. close"]
            return float(rate)
        
        else:
            # หากไม่ได้ระบุเดือน ให้ใช้ข้อมูลเดือนล่าสุด
            latest_date = next(iter(time_series))
            latest_data = time_series[latest_date]
            rate = latest_data["4. close"]
            return float(rate)

    except KeyError:
        raise ValueError("ไม่สามารถดึงอัตราแลกเปลี่ยนได้")

def fetch_volatile_weekly(from_symbol, to_symbol, date=None):
    data = fetch_fx_data_symbol("FX_DAILY", from_symbol=from_symbol, to_symbol=to_symbol)
    
    try:
        # ดึงข้อมูล Time Series FX (Daily)
        time_series = data["Time Series FX (Daily)"]

        today = datetime.now()
        dates_to_fetch = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
        close_values = []
        missing_dates = []
        for date in dates_to_fetch:
            if date in time_series:
                close_values.append(float(time_series[date]["4. close"]))
            else:
                missing_dates.append(date)

        if missing_dates:
            print(f"ไม่มีข้อมูลสำหรับวันที่: {', '.join(missing_dates)}")
        # ตรวจสอบว่ามีข้อมูลเพียงพอหรือไม่
        if len(close_values) < 2:
            raise ValueError("ไม่สามารถคำนวณ Volatility ได้เนื่องจากข้อมูลไม่เพียงพอ")

        # คำนวณ Volatility (Standard Deviation)
        volatility = statistics.stdev(close_values)
        return volatility

    except KeyError:
        # หากโครงสร้างข้อมูลผิดพลาด
        raise ValueError("ไม่สามารถดึงข้อมูลอัตราแลกเปลี่ยนได้")
    
def fetch_volatile_monthly(from_symbol, to_symbol, date=None):
    data = fetch_fx_data_symbol("FX_DAILY", from_symbol=from_symbol, to_symbol=to_symbol)
    
    try:
        # ดึงข้อมูล Time Series FX (Daily)
        time_series = data["Time Series FX (Daily)"]

        today = datetime.now()
        dates_to_fetch = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)]
        close_values = []
        missing_dates = []
        for date in dates_to_fetch:
            if date in time_series:
                close_values.append(float(time_series[date]["4. close"]))
            else:
                missing_dates.append(date)

        if missing_dates:
            print(f"ไม่มีข้อมูลสำหรับวันที่: {', '.join(missing_dates)}")
        # ตรวจสอบว่ามีข้อมูลเพียงพอหรือไม่
        if len(close_values) < 2:
            raise ValueError("ไม่สามารถคำนวณ Volatility ได้เนื่องจากข้อมูลไม่เพียงพอ")

        # คำนวณ Volatility (Standard Deviation)
        volatility = statistics.stdev(close_values)
        return volatility

    except KeyError:
        # หากโครงสร้างข้อมูลผิดพลาด
        raise ValueError("ไม่สามารถดึงข้อมูลอัตราแลกเปลี่ยนได้")
    
