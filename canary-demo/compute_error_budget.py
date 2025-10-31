import requests
import datetime

def calculate_error_budget():
    # Constants
    SLO_PERCENTAGE = 99.9  # Our SLO is 99.9%
    SECONDS_IN_MONTH = 30 * 24 * 60 * 60  # 30 days in seconds
    
    # Calculate monthly error budget in seconds
    error_budget_percentage = 100 - SLO_PERCENTAGE  # 0.1%
    monthly_error_budget_seconds = (error_budget_percentage / 100) * SECONDS_IN_MONTH
    
    # Prometheus endpoint (please ensure port-forward is active)
    PROMETHEUS_URL = 'http://localhost:9090'
    
    try:
        # Query for total errors
        error_query = 'sum(increase(http_requests_total{code=~"5.*"}[30d]))'
        response = requests.get(f'{PROMETHEUS_URL}/api/v1/query', params={'query': error_query})
        error_data = response.json()
        total_errors = float(error_data['data']['result'][0]['value'][1]) if error_data['data']['result'] else 0
        
        # Query for total requests
        requests_query = 'sum(increase(http_requests_total[30d]))'
        response = requests.get(f'{PROMETHEUS_URL}/api/v1/query', params={'query': requests_query})
        requests_data = response.json()
        total_requests = float(requests_data['data']['result'][0]['value'][1]) if requests_data['data']['result'] else 0
        
        # Calculate remaining error budget percentage
        if total_requests > 0:
            error_rate = (total_errors / total_requests) * 100
            used_budget_percentage = (error_rate / error_budget_percentage) * 100
            remaining_budget_percentage = 100 - used_budget_percentage
        else:
            remaining_budget_percentage = 100
            
        return {
            "monthly_error_budget_seconds": monthly_error_budget_seconds,
            "remaining_error_budget_percentage": remaining_budget_percentage,
            "total_requests": total_requests,
            "total_errors": total_errors
        }
        
    except Exception as e:
        print(f"Error fetching data from Prometheus: {str(e)}")
        return None

def main():
    print("Calculating error budget...")
    print("Make sure you have port-forwarded Prometheus:")
    print("kubectl port-forward svc/prometheus-operated 9090:9090 -n canary-demo")
    print("\nFetching data...")
    
    budget = calculate_error_budget()
    
    if budget:
        print("\nResults:")
        print("-" * 50)
        print(f"Monthly Error Budget (seconds): {budget['monthly_error_budget_seconds']:.2f}")
        print(f"Remaining Error Budget (%): {budget['remaining_error_budget_percentage']:.2f}%")
        print("\nDetailed Statistics:")
        print(f"Total Requests (30d): {budget['total_requests']:.0f}")
        print(f"Total Errors (30d): {budget['total_errors']:.0f}")
        
        print("\nFor answers.yml:")
        print("-" * 50)
        print("error_budget:")
        print(f"  monthly_error_budget_seconds: {budget['monthly_error_budget_seconds']:.2f}")
        print(f"  remaining_error_budget_percentage: {budget['remaining_error_budget_percentage']:.2f}")
    else:
        print("\nFailed to calculate error budget. Please check if Prometheus is accessible.")

if __name__ == "__main__":
    main()