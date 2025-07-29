"""
Test runner script for Kalp Network exploratory testing
"""
import os
import sys
import subprocess
from datetime import datetime

def run_tests():
    """Run the test suite with proper configuration"""
    
    # Create reports directory if it doesn't exist
    if not os.path.exists('reports'):
        os.makedirs('reports')
    
    # Generate timestamp for report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Test command with HTML report
    cmd = [
        'python', '-m', 'pytest',
        'tests/',
        '-v',
        '--tb=short',
        f'--html=reports/test_report_{timestamp}.html',
        '--self-contained-html',
        '--capture=no'
    ]
    
    print("Starting Kalp Network Exploratory Testing...")
    print("=" * 60)
    print(f"Command: {' '.join(cmd)}")
    print("=" * 60)
    
    try:
        # Run tests
        result = subprocess.run(cmd, capture_output=False, text=True)
        
        print("\n" + "=" * 60)
        print("Test execution completed!")
        print(f"Report generated: reports/test_report_{timestamp}.html")
        print("Screenshots saved in: screenshots/")
        print("=" * 60)
        
        return result.returncode
        
    except Exception as e:
        print(f"Error running tests: {e}")
        return 1

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)