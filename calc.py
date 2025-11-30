"""
calc.py - Deterministic Financial Calculators
================================================

This module contains pure mathematical functions for financial calculations.
No AI/LLM is used here - only exact formulas.

Functions:
- calculate_sip(): Calculate monthly SIP for a target amount
- calculate_emi(): Calculate EMI for a loan
- format_inr(): Format numbers in Indian Rupee notation
"""

from typing import Dict


def calculate_sip(future_value: float, years: int, annual_rate: float = 12.0) -> Dict[str, float]:
    """
    Calculate monthly SIP required to reach a future value.
    
    Formula: PMT = FV * r / ((1+r)^n - 1)
    where:
        r = monthly rate = annual_rate / 12 / 100
        n = total months = years * 12
        FV = future value target
    
    Args:
        future_value: Target amount in rupees
        years: Investment time horizon
        annual_rate: Expected annual return rate (default 12%)
    
    Returns:
        Dictionary with monthly_sip, total_investment, and expected_returns
    
    Example:
        >>> calc = calculate_sip(1000000, 5, 12.0)
        >>> print(calc['monthly_sip'])
        12244.45
    """
    if years <= 0 or future_value <= 0:
        return {
            "monthly_sip": 0,
            "total_investment": 0,
            "expected_returns": 0,
            "total_value": 0
        }
    
    # Convert annual rate to monthly rate
    r = annual_rate / 12 / 100
    n = years * 12
    
    # PMT formula for future value
    if r == 0:
        monthly_sip = future_value / n
    else:
        monthly_sip = future_value * r / ((1 + r) ** n - 1)
    
    total_investment = monthly_sip * n
    expected_returns = future_value - total_investment
    
    return {
        "monthly_sip": round(monthly_sip, 2),
        "total_investment": round(total_investment, 2),
        "expected_returns": round(expected_returns, 2),
        "total_value": round(future_value, 2)
    }


def calculate_emi(principal: float, years: int, annual_rate: float) -> Dict[str, float]:
    """
    Calculate EMI for a loan.
    
    Formula: EMI = P * r * (1+r)^n / ((1+r)^n - 1)
    where:
        P = principal loan amount
        r = monthly interest rate
        n = total months
    
    Args:
        principal: Loan amount
        years: Loan tenure
        annual_rate: Interest rate per annum
    
    Returns:
        Dictionary with monthly_emi, total_payment, and total_interest
    
    Example:
        >>> emi = calculate_emi(500000, 10, 8.5)
        >>> print(emi['monthly_emi'])
        6207.87
    """
    if years <= 0 or principal <= 0:
        return {
            "monthly_emi": 0,
            "total_payment": 0,
            "total_interest": 0
        }
    
    r = annual_rate / 12 / 100
    n = years * 12
    
    if r == 0:
        monthly_emi = principal / n
    else:
        monthly_emi = principal * r * (1 + r) ** n / ((1 + r) ** n - 1)
    
    total_payment = monthly_emi * n
    total_interest = total_payment - principal
    
    return {
        "monthly_emi": round(monthly_emi, 2),
        "total_payment": round(total_payment, 2),
        "total_interest": round(total_interest, 2)
    }


def format_inr(amount: float) -> str:
    """
    Format a number in Indian Rupee notation with commas.
    
    Indian numbering system:
    - First comma after 3 digits from right
    - Then every 2 digits
    
    Example:
        >>> format_inr(1234567.89)
        '₹12,34,567.89'
        >>> format_inr(50000)
        '₹50,000'
    
    Args:
        amount: The amount to format
    
    Returns:
        Formatted string with ₹ symbol and commas
    """
    # Handle negative numbers
    if amount < 0:
        return f"-₹{format_inr(abs(amount))[1:]}"
    
    # Split into integer and decimal parts
    amount_str = f"{amount:.2f}"
    parts = amount_str.split('.')
    integer_part = parts[0]
    decimal_part = parts[1] if len(parts) > 1 else "00"
    
    # Indian number formatting
    if len(integer_part) <= 3:
        formatted = integer_part
    else:
        # Last 3 digits
        last_three = integer_part[-3:]
        # Remaining digits
        remaining = integer_part[:-3]
        
        # Add commas every 2 digits from right in remaining part
        formatted_remaining = ""
        while len(remaining) > 2:
            formatted_remaining = "," + remaining[-2:] + formatted_remaining
            remaining = remaining[:-2]
        
        if remaining:
            formatted_remaining = remaining + formatted_remaining
        
        formatted = formatted_remaining + "," + last_three
    
    # Remove trailing zeros from decimal
    if decimal_part == "00":
        return f"₹{formatted}"
    else:
        return f"₹{formatted}.{decimal_part}"


if __name__ == "__main__":
    # Test the functions
    print("Testing SIP Calculator:")
    result = calculate_sip(1000000, 5, 12.0)
    print(f"  Target: {format_inr(1000000)}")
    print(f"  Monthly SIP: {format_inr(result['monthly_sip'])}")
    print(f"  Total Investment: {format_inr(result['total_investment'])}")
    print(f"  Expected Returns: {format_inr(result['expected_returns'])}")
    
    print("\nTesting EMI Calculator:")
    emi_result = calculate_emi(500000, 10, 8.5)
    print(f"  Loan: {format_inr(500000)}")
    print(f"  Monthly EMI: {format_inr(emi_result['monthly_emi'])}")
    print(f"  Total Payment: {format_inr(emi_result['total_payment'])}")
    print(f"  Total Interest: {format_inr(emi_result['total_interest'])}")
    
    print("\nTesting INR Formatting:")
    test_amounts = [1234567.89, 50000, 100, 12345678901.50]
    for amt in test_amounts:
        print(f"  {amt} → {format_inr(amt)}")
