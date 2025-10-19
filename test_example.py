"""
Test Example File for Code Cartographer

This is a sample Python file you can use to test the Code Cartographer tool.
It contains a mix of imports, function definitions, and function calls.
"""

import os
import json
from typing import List, Dict, Optional
from datetime import datetime


def load_config(file_path: str) -> Dict:
    """
    Load configuration from a JSON file.
    
    Args:
        file_path: Path to the JSON configuration file
        
    Returns:
        Dictionary containing configuration data
        
    Raises:
        FileNotFoundError: If the config file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
    
    with open(file_path, 'r') as f:
        return json.load(f)


def process_data(data: List[int], operation: str = 'sum') -> int:
    """
    Process a list of integers with the specified operation.
    
    Args:
        data: List of integers to process
        operation: Operation to perform ('sum', 'max', 'min', 'avg')
        
    Returns:
        Result of the operation
    """
    if operation == 'sum':
        return sum(data)
    elif operation == 'max':
        return max(data)
    elif operation == 'min':
        return min(data)
    elif operation == 'avg':
        return sum(data) // len(data) if data else 0
    else:
        raise ValueError(f"Unknown operation: {operation}")


def validate_input(value: Optional[int]) -> bool:
    """
    Validate that the input value is a positive integer.
    
    Args:
        value: Value to validate
        
    Returns:
        True if valid, False otherwise
    """
    return value is not None and value > 0


def generate_report(data: Dict, output_path: str) -> None:
    """
    Generate a report from the processed data.
    
    Args:
        data: Dictionary containing report data
        output_path: Path where the report should be saved
    """
    timestamp = datetime.now().isoformat()
    
    report = {
        'generated_at': timestamp,
        'data': data,
        'version': '1.0.0'
    }
    
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"Report generated at: {output_path}")


def main():
    """Main entry point for the application."""
    print("Starting Code Cartographer test example...")
    
    # Example usage
    try:
        # Load configuration (would fail since file doesn't exist, but shows intent)
        # config = load_config('config.json')
        
        # Process some sample data
        sample_data = [1, 2, 3, 4, 5, 10, 15, 20]
        
        total = process_data(sample_data, 'sum')
        maximum = process_data(sample_data, 'max')
        minimum = process_data(sample_data, 'min')
        average = process_data(sample_data, 'avg')
        
        print(f"Sum: {total}")
        print(f"Max: {maximum}")
        print(f"Min: {minimum}")
        print(f"Avg: {average}")
        
        # Validate some inputs
        is_valid = validate_input(total)
        print(f"Result is valid: {is_valid}")
        
        # Generate a report
        report_data = {
            'sum': total,
            'max': maximum,
            'min': minimum,
            'avg': average
        }
        
        # generate_report(report_data, 'report.json')
        
        print("✅ Example completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise


if __name__ == "__main__":
    main()



