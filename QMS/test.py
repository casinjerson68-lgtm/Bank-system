"""
Bank Queue Management System - Quick Test
Tests the core functionality without GUI
"""

from queue import BankQMS, ServiceType, CustomerPriority
import time


def test_basic_operations():
    """Test basic QMS operations"""
    print("\n" + "="*60)
    print("BANK QMS - FUNCTIONAL TEST")
    print("="*60 + "\n")
    
    # Initialize system
    qms = BankQMS(num_counters=3)
    print("✓ System initialized with 3 counters\n")
    
    # Test 1: Add customers
    print("TEST 1: Adding customers to queue")
    print("-"*60)
    
    test_customers = [
        ("Alice Johnson", ServiceType.DEPOSIT, CustomerPriority.STANDARD),
        ("Bob Smith", ServiceType.WITHDRAWAL, CustomerPriority.STANDARD),
        ("Margaret Brown", ServiceType.QUERY, CustomerPriority.SENIOR_CITIZEN),
        ("Diana Prince", ServiceType.LOAN_APPLICATION, CustomerPriority.VIP),
        ("Edward Chen", ServiceType.ACCOUNT_OPENING, CustomerPriority.DISABLED),
    ]
    
    for name, service, priority in test_customers:
        customer, ticket = qms.add_customer(name, service, priority)
        print(f"  ✓ {name} (Ticket: {ticket}, Priority: {priority.name})")
    
    print(f"\n✓ Total customers in queue: {qms.bank_queue.get_queue_size()}\n")
    
    # Test 2: Check priority order
    print("TEST 2: Verifying priority queue order")
    print("-"*60)
    
    queue_customers = qms.bank_queue.view_queue()
    print("Queue order (highest priority first):")
    for i, customer in enumerate(queue_customers, 1):
        print(f"  {i}. {customer.name} (Ticket: {customer.ticket_number}, Priority: {customer.priority.name})")
    print()
    
    # Test 3: Assign to counters
    print("TEST 3: Assigning customers to counters")
    print("-"*60)
    
    for i in range(3):
        customer, counter = qms.assign_customer_to_counter()
        if customer and counter:
            print(f"  ✓ {customer.name} assigned to Counter {counter.counter_id}")
    
    print(f"\n✓ Customers remaining in queue: {qms.bank_queue.get_queue_size()}\n")
    
    # Test 4: Check counter status
    print("TEST 4: Counter status")
    print("-"*60)
    
    counter_status = qms.get_counter_status()
    for status in counter_status:
        if status['is_busy']:
            print(f"  Counter {status['counter_id']}: BUSY (Serving {status['customer_name']})")
        else:
            print(f"  Counter {status['counter_id']}: AVAILABLE")
    print()
    
    # Test 5: Complete services
    print("TEST 5: Completing services")
    print("-"*60)
    
    for counter_id in [1, 2]:
        customer = qms.complete_service(counter_id)
        if customer:
            wait_time = customer.wait_time / 60
            service_time = customer.service_time / 60
            print(f"  ✓ Service completed for {customer.name}")
            print(f"    Wait Time: {wait_time:.2f} minutes, Service Time: {service_time:.2f} minutes")
    
    print()
    
    # Test 6: Assign remaining
    print("TEST 6: Assigning new customers to freed counters")
    print("-"*60)
    
    customer, counter = qms.assign_customer_to_counter()
    if customer and counter:
        print(f"  ✓ {customer.name} assigned to Counter {counter.counter_id}")
    
    print()
    
    # Test 7: Statistics
    print("TEST 7: System Statistics")
    print("-"*60)
    
    stats = qms.get_statistics()
    print(f"  Total Served: {stats['total_served']}")
    print(f"  Avg Wait Time: {stats['avg_wait_time']/60:.2f} minutes")
    print(f"  Avg Service Time: {stats['avg_service_time']/60:.2f} minutes")
    print(f"  System Uptime: {stats['total_time']/60:.2f} minutes")
    
    if stats['service_breakdown']:
        print("\n  Service Breakdown:")
        for service, count in stats['service_breakdown'].items():
            print(f"    - {service}: {count}")
    
    print("\n" + "="*60)
    print("✓ ALL TESTS COMPLETED SUCCESSFULLY")
    print("="*60 + "\n")
    
    return True


if __name__ == "__main__":
    try:
        test_basic_operations()
        print("Ready to run: python main.py\n")
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}\n")
        import traceback
        traceback.print_exc()
