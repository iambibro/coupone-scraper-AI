"""
This script demonstrates how to use the Coupon Scraper API to fetch coupons.
You can run this as a standalone script to test the functionality.
"""

import requests
import json
import os
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from datetime import datetime

# Add project root to Python path for imports to work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Check if API is running locally, otherwise use a deployed URL
API_BASE_URL = "http://localhost:8000/api"

def get_supported_brands():
    """Get list of supported brands from the API"""
    try:
        response = requests.get(f"{API_BASE_URL}/supported-brands")
        response.raise_for_status()
        return response.json()["supported_brands"]
    except requests.RequestException as e:
        print(f"Error fetching supported brands: {e}")
        return []

def get_coupons_for_brand(brand):
    """Get coupons for a specific brand"""
    try:
        response = requests.get(f"{API_BASE_URL}/coupons?brand={brand}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching coupons for {brand}: {e}")
        return None

def display_coupons(brand_data):
    """Display coupon data in a formatted table"""
    console = Console()
    
    if not brand_data or not brand_data.get("coupons"):
        console.print(f"[yellow]No coupons found for {brand_data.get('brand', 'Unknown brand')}[/yellow]")
        return
    
    # Header info
    console.print(Panel(
        f"[bold]{brand_data['brand']}[/bold] Coupons\n"
        f"Source: {brand_data['source']}\n"
        f"Last Updated: {brand_data['last_updated']}", 
        title="Coupon Information",
        expand=False
    ))
    
    # Create table
    table = Table(show_header=True, header_style="bold")
    table.add_column("Code", style="cyan")
    table.add_column("Description", style="green")
    table.add_column("Valid Till", style="yellow")
    table.add_column("Terms", style="magenta")
    
    # Add rows
    for coupon in brand_data["coupons"]:
        table.add_row(
            coupon.get("code", "N/A"),
            coupon.get("description", "N/A"),
            coupon.get("valid_till", "N/A"),
            coupon.get("terms", "N/A"),
        )
    
    console.print(table)

def main():
    """Main function to demonstrate the API usage"""
    console = Console()
    
    console.print("[bold]Coupon Scraper Demo[/bold]", style="blue")
    console.print("Fetching supported brands...", style="dim")
    
    brands = get_supported_brands()
    
    if not brands:
        console.print("[red]Error: Could not fetch supported brands. Is the API running?[/red]")
        console.print(f"Make sure the API is running at {API_BASE_URL}")
        return
    
    console.print(f"[green]Found {len(brands)} supported brands: {', '.join(brands)}[/green]")
    
    # Process each brand
    for brand in brands:
        console.print(f"\nFetching coupons for [bold]{brand}[/bold]...", style="dim")
        coupons = get_coupons_for_brand(brand)
        
        if coupons:
            display_coupons(coupons)
        else:
            console.print(f"[red]Error fetching coupons for {brand}[/red]")

if __name__ == "__main__":
    main()