#!/usr/bin/env python3

import typer
from cli_app.fetch_api import fetch_fx_data_currency, fetch_fx_data_symbol, fetch_fx_daily, fetch_fx_weekly, fetch_fx_monthly, fetch_currency_list,fetch_volatile_weekly,fetch_volatile_monthly, fetch_max_min_weekly, fetch_max_min_monthly
import time
import keyboard
import typer

# ใช้ typer สร้างแอป CLI 
app = typer.Typer()

# help - แสดงรายการ subcommands ที่ใช้งานได้
@app.command("help")
def help():
    """
    Usage: cli-exc help
    
    แสดงรายการ subcommands ที่สามารถใช้งานได้
    """
    
    typer.echo("Available commands:")
    typer.echo("help :แสดงคำสั่งทั้งหมด")
    typer.echo("list [OPTIONS] :แสดงสกุลเงินที่แอปพลิเคชันรองรับ")
    typer.echo("realtime :แสดงข้อมูลอัตราแลกเปลี่ยนปัจจุบัน")    
    typer.echo("daily :แสดงข้อมูลอัตราแลกเปลี่ยนรายวัน")
    typer.echo("weekly :แสดงข้อมูลอัตราแลกเปลี่ยนรายสัปดาห์")
    typer.echo("monthly :แสดงข้อมูลอัตราแลกเปลี่ยนรายเดือน")
    typer.echo("max_min :แสดงข้อมูลการแลกเปลี่ยนสูงสุด - ต่ำสุด ในช่วงเวลาที่กำหนด")
    typer.echo("volatile [OPTIONS] :แสดงความผกผันในระยะเวลา 1 สัปดาห์หรือ 1 เดือน")

# list - แสดงรสกุลเงินที่แอปพลิเคชันรองรับ
@app.command("list")
def list(find="ALL"):
    """
    Usage: cli-exc list [OPTIONS]
    
    แสดงสกุลเงินที่แอปพลิเคชันรองรับ

    Options:
    --find TEXT  ค้นหาและแสดงเฉพาะสกุลเงินที่มีข้อความ TEXT
                ตัวอย่าง ต้องการค้นหาหน่วยเงิน USD, 'cli-exc list --find USD'
    --help       แสดงข้อความนี้
    """

    physical_url = "https://www.alphavantage.co/physical_currency_list/"
    digital_url = "https://www.alphavantage.co/digital_currency_list/"
    
    typer.echo("\nPress 'Enter' to show physical and digital currencies")
    typer.echo("Press 'p' to show physical currencies")
    typer.echo("Press 'd' to show digital currencies")
    typer.echo("or Press 'q' to quit.")

    while True:
        if keyboard.is_pressed('enter'):
            typer.echo("Fetching physical currencies...")
            physical_currencies = fetch_currency_list(physical_url)

            typer.echo("Fetching digital currencies...")
            digital_currencies = fetch_currency_list(digital_url)
            
            all_currencies = physical_currencies + digital_currencies
            break
        
        elif keyboard.is_pressed('p'):  
            typer.echo("Fetching physical currencies...")
            all_currencies = fetch_currency_list(physical_url)
            break
            
        elif keyboard.is_pressed('enter'): 
            typer.echo("Fetching digital currencies...")
            all_currencies = fetch_currency_list(digital_url)
            break
            
        elif keyboard.is_pressed('q'): 
            return
        
        elif keyboard.read_event() == keyboard.KEY_DOWN:
            typer.echo("Invalid input..")
            typer.echo("Press 'Enter' to show physical and digital currencies")
            typer.echo("Press 'p' to show physical currencies")
            typer.echo("Press 'd' to show digital currencies")
            typer.echo("or Press 'q' to quit.")
        

    # Display 10 items per page
    page_size = 10
    total = len(all_currencies)
    
    i = 0
    while i < total:
        typer.echo("\nNum | Currency Code | Description")
        typer.echo("-" * 40)
        if(find == "ALL"):
            
            j = i
            for code, description in all_currencies[i:i+page_size]:
                j = j + 1
                typer.echo(f"{j:<3} | {code:<13} | {description}")
            
            typer.echo("\nPress Space to show more, Enter to show all remaining, or 'q' to quit.")
            while True:
                if keyboard.is_pressed('q'):
                    time.sleep(0.5)
                    typer.echo("Exiting list.")
                    return
                elif keyboard.is_pressed(' '):  
                    time.sleep(0.5)
                    i += page_size
                    break
                elif keyboard.is_pressed('enter'): 
                    time.sleep(0.5)
                    for code, description in all_currencies[i:]:
                        j = j + 1
                        typer.echo(f"{j:<3} | {code:<13} | {description}")
                    return
        else:
            j = i
            for code, description in all_currencies[i:]:
                if (find.lower().strip() in code.lower() + "|" + description.lower()):
                    j = j + 1
                    typer.echo(f"{j:<3} | {code:<13} | {description}")
                    
            typer.echo(f"\nFound {j} items that include '{find}'")
            return

@app.command("realtime")
def realtime(form_cur, to_cur, money=1.0):
    """
    แสดงข้อมูลอัตราแลกเปลี่ยนปัจจุบัน
    """
    data = fetch_fx_data_currency("CURRENCY_EXCHANGE_RATE", form_cur, to_cur)
    data = data["Realtime Currency Exchange Rate"]
    
    ex_rate = float(data["5. Exchange Rate"])
    money = float(money)
    to_money = money*ex_rate
    time = data["6. Last Refreshed"] + data["7. Time Zone"]
    from_sym = data["1. From_Currency Code"]
    to_sym = data["3. To_Currency Code"]
    
    typer.echo(f'{time}:')
    typer.echo(f'อัตตราแลกเปลี่ยนปัจจุบันคือ {ex_rate:.4f}')
    typer.echo('===================================')
    typer.echo(f'{"จากเงิน":<9} {money:<10.4f} {from_sym}')
    typer.echo(f'{"แลกได้":<9} {to_money:<10.4f} {to_sym}')

@app.command("max_min")
def max_min(peroid: str, currency_from : str, currency_to : str):
    if peroid == "weekly":
        data = fetch_max_min_weekly(currency_from, currency_to)
        typer.echo('===================================')
        typer.echo(f"อัตราแลกเปลี่ยนสูงสุดในช่วง 1 สัปดาห์ที่ผ่านมา : {data[0]}")
        typer.echo(f"เมื่อวันที่ {data[1]}")
        typer.echo('===================================')
        typer.echo(f"อัตราแลกเปลี่ยนต่ำสุดในช่วง 1 สัปดาห์ที่ผ่านมา : {data[2]}")
        typer.echo(f"เมื่อวันที่ {data[3]}")
    elif peroid == "monthly":
        data = fetch_max_min_monthly(currency_from, currency_to)
        typer.echo('===================================')
        typer.echo(f"อัตราแลกเปลี่ยนสูงสุดในช่วง 1 เดือนที่ผ่านมา : {data[0]}")
        typer.echo(f"เมื่อวันที่ {data[1]}")
        typer.echo('===================================')
        typer.echo(f"อัตราแลกเปลี่ยนต่ำสุดในช่วง 1 เดือนที่ผ่านมา : {data[2]}")
        typer.echo(f"เมื่อวันที่ {data[3]}")
        
    else:
        typer.echo("โปรดระบุ period ให้ถูกต้อง: 'weekly' หรือ 'monthly'")
        
@app.command("volatile")
def volatile( period: str,currency_from: str, currency_to: str):
    if period == "weekly":
        volatile_last_week = fetch_volatile_weekly(currency_from, currency_to)
        typer.echo(f"ความผันผวนในช่วง 1 สัปดาห์ที่ผ่านมา : {volatile_last_week}")
        
    elif period == "monthly":
        volatile_last_month = fetch_volatile_monthly(currency_from, currency_to)
        typer.echo(f"ความผันผวนในช่วง 1 สัปดาห์ที่ผ่านมา : {volatile_last_month}")
        
    else:
        typer.echo("โปรดระบุ period ให้ถูกต้อง: 'weekly' หรือ 'monthly'")

def convert_currency(amount, from_currency, to_currency): #funtion แปลงสกุลเงิน
    rate = fetch_fx_daily(from_currency, to_currency)
    converted_amount = amount * rate
    return converted_amount

@app.command("daily")
def daily(from_currency: str, to_currency: str, date: str = typer.Argument(None, help="วันที่ที่ต้องการดูอัตราแลกเปลี่ยน (YYYY-MM-DD)"), amount: float = typer.Option(None, "--amount", "-a", help="จำนวนเงินที่ต้องการแปลง"), convert: bool = typer.Option(False, "--convert", "-c", help="แปลงสกุลเงิน")):

    try:
        rate = fetch_fx_daily(from_currency, to_currency, date)
        typer.echo(f"อัตราแลกเปลี่ยนรายวันจาก {from_currency} ไปยัง {to_currency}: {rate}")
        if convert :
            if amount:
                rate = fetch_fx_daily(from_currency, to_currency, date)
                result = convert_currency(amount, from_currency, to_currency)
                typer.echo(f"{amount} {from_currency} = {result:.2f} {to_currency}")
            else:
                typer.echo(f"ไม่พบจำนวนเงินที่ต้องการแปลง กรุณาพิมพ์คำสั่งใหม่อีกครั้ง")

            
    except ValueError as e:
        typer.echo(f"ข้อผิดพลาด: {e}")

@app.command("weekly")
def weekly(from_currency: str, to_currency: str, date: str = typer.Argument(None, help="วันที่ของสัปดาห์ที่ต้องการดูอัตราแลกเปลี่ยน (YYYY-MM-DD)"), amount: float = typer.Option(None, "--amount", "-a", help="จำนวนเงินที่ต้องการแปลง"), convert: bool = typer.Option(False, "--convert", "-c", help="แปลงสกุลเงิน")):

    try:
        rate = fetch_fx_weekly(from_currency, to_currency, date)
        typer.echo(f"อัตราแลกเปลี่ยนรายสัปดาห์จาก {from_currency} ไปยัง {to_currency}: {rate}")
        if convert :
            if amount:
                rate = fetch_fx_weekly(from_currency, to_currency, date)
                result = convert_currency(amount, from_currency, to_currency)
                typer.echo(f"{amount} {from_currency} = {result:.2f} {to_currency}")
            else:
                typer.echo(f"ไม่พบจำนวนเงินที่ต้องการแปลง กรุณาพิมพ์คำสั่งใหม่อีกครั้ง")

            
    except ValueError as e:
        typer.echo(f"ข้อผิดพลาด: {e}")

@app.command("monthly")
def monthly(from_currency: str, to_currency: str, month: str = typer.Argument(None, help="เดือนที่ต้องการดูอัตราแลกเปลี่ยน (YYYY-MM)"), amount: float = typer.Option(None, "--amount", "-a", help="จำนวนเงินที่ต้องการแปลง"), convert: bool = typer.Option(False, "--convert", "-c", help="แปลงสกุลเงิน")):

    try:
        rate = fetch_fx_monthly(from_currency, to_currency, month)
        typer.echo(f"อัตราแลกเปลี่ยนรายเดือนจาก {from_currency} ไปยัง {to_currency}: {rate}")
        if convert :
            if amount:
                rate = fetch_fx_monthly(from_currency, to_currency, month)
                result = convert_currency(amount, from_currency, to_currency)
                typer.echo(f"{amount} {from_currency} = {result:.2f} {to_currency}")
            else:
                typer.echo(f"ไม่พบจำนวนเงินที่ต้องการแปลง กรุณาพิมพ์คำสั่งใหม่อีกครั้ง") 
    except ValueError as e:
        typer.echo(f"ข้อผิดพลาด: {e}")

        
if __name__ == "__main__":
    app()