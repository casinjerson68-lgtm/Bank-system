"""
Bank Queue Management System - Backend Logic
Core classes for managing queues, customers, and service counters
"""

from collections import deque
from datetime import datetime, timedelta
from enum import Enum
import uuid


class ServiceType(Enum):
    """Types of services offered at the bank"""
    DEPOSIT = "Deposit"
    WITHDRAWAL = "Withdrawal"
    LOAN_APPLICATION = "Loan Application"
    ACCOUNT_OPENING = "Account Opening"
    QUERY = "General Query"


class CustomerPriority(Enum):
    """Priority levels for customers"""
    STANDARD = 1
    SENIOR_CITIZEN = 2
    DISABLED = 3
    VIP = 4


class Customer:
    """Represents a customer in the queue"""
    
    def __init__(self, name, service_type, priority=CustomerPriority.STANDARD):
        self.id = str(uuid.uuid4())[:8]
        self.name = name
        self.service_type = service_type
        self.priority = priority
        self.ticket_number = None
        self.arrival_time = datetime.now()
        self.service_start_time = None
        self.service_end_time = None
        self.wait_time = 0
        self.service_time = 0
        self.status = "Waiting"
    
    def get_wait_time(self):
        """Calculate current wait time in seconds"""
        if self.service_start_time:
            self.wait_time = (self.service_start_time - self.arrival_time).total_seconds()
        else:
            self.wait_time = (datetime.now() - self.arrival_time).total_seconds()
        return self.wait_time
    
    def __repr__(self):
        return f"{self.name} (#{self.ticket_number})"


class ServiceCounter:
    """Represents a service counter/teller in the bank"""
    
    def __init__(self, counter_id):
        self.counter_id = counter_id
        self.is_busy = False
        self.current_customer = None
        self.customers_served = 0
        self.total_service_time = 0
    
    def serve_customer(self, customer):
        """Start serving a customer"""
        self.is_busy = True
        self.current_customer = customer
        customer.service_start_time = datetime.now()
        customer.status = "Being Served"
    
    def finish_service(self):
        """Finish serving current customer"""
        if self.current_customer:
            self.current_customer.service_end_time = datetime.now()
            self.current_customer.service_time = (
                self.current_customer.service_end_time - 
                self.current_customer.service_start_time
            ).total_seconds()
            self.current_customer.status = "Completed"
            
            self.customers_served += 1
            self.total_service_time += self.current_customer.service_time
            
            served_customer = self.current_customer
            self.current_customer = None
            self.is_busy = False
            return served_customer
        return None
    
    def get_average_service_time(self):
        """Get average service time at this counter"""
        if self.customers_served == 0:
            return 0
        return self.total_service_time / self.customers_served


class BankQueue:
    """Priority queue for managing customers"""
    
    def __init__(self):
        self.queue = deque()
        self.ticket_counter = 0
    
    def add_customer(self, customer):
        """Add customer to queue with priority"""
        self.ticket_counter += 1
        customer.ticket_number = self.ticket_counter
        self.queue.append(customer)
        self._sort_queue()
        return customer.ticket_number
    
    def _sort_queue(self):
        """Sort queue by priority and arrival time"""
        self.queue = deque(sorted(self.queue, key=lambda c: (-c.priority.value, c.arrival_time)))
    
    def get_next_customer(self):
        """Remove and return the next customer to be served"""
        if self.queue:
            return self.queue.popleft()
        return None
    
    def peek_next(self):
        """View next customer without removing"""
        if self.queue:
            return self.queue[0]
        return None
    
    def get_queue_size(self):
        """Get number of customers waiting"""
        return len(self.queue)
    
    def view_queue(self, limit=20):
        """View customers in queue"""
        customers = list(self.queue)[:limit]
        return customers


class BankQMS:
    """Bank Queue Management System"""
    
    def __init__(self, num_counters=3):
        self.bank_queue = BankQueue()
        self.counters = [ServiceCounter(i+1) for i in range(num_counters)]
        self.served_customers = []
        self.start_time = datetime.now()
    
    def add_customer(self, name, service_type, priority=CustomerPriority.STANDARD):
        """Add a new customer to the queue"""
        customer = Customer(name, service_type, priority)
        ticket_num = self.bank_queue.add_customer(customer)
        return customer, ticket_num
    
    def assign_customer_to_counter(self):
        """Assign next customer in queue to available counter"""
        next_customer = self.bank_queue.get_next_customer()
        if not next_customer:
            return None, None
        
        available_counter = self._get_available_counter()
        if not available_counter:
            self.bank_queue.add_customer(next_customer)
            return None, None
        
        available_counter.serve_customer(next_customer)
        return next_customer, available_counter
    
    def complete_service(self, counter_id):
        """Mark service as complete at a counter"""
        counter = self._get_counter_by_id(counter_id)
        if counter and counter.current_customer:
            customer = counter.finish_service()
            self.served_customers.append(customer)
            return customer
        return None
    
    def _get_available_counter(self):
        """Find an available counter"""
        for counter in self.counters:
            if not counter.is_busy:
                return counter
        return None
    
    def _get_counter_by_id(self, counter_id):
        """Get counter by ID"""
        for counter in self.counters:
            if counter.counter_id == counter_id:
                return counter
        return None
    
    def get_counter_status(self):
        """Get status of all counters"""
        status = []
        for counter in self.counters:
            if counter.is_busy and counter.current_customer:
                customer = counter.current_customer
                wait_time = customer.get_wait_time()
                status.append({
                    'counter_id': counter.counter_id,
                    'is_busy': True,
                    'customer_name': customer.name,
                    'wait_time': wait_time
                })
            else:
                status.append({
                    'counter_id': counter.counter_id,
                    'is_busy': False,
                    'customer_name': None,
                    'wait_time': 0
                })
        return status
    
    def get_statistics(self):
        """Get system statistics"""
        total_served = len(self.served_customers)
        
        if total_served == 0:
            return {
                'total_served': 0,
                'avg_wait_time': 0,
                'avg_service_time': 0,
                'total_time': 0,
                'service_breakdown': {}
            }
        
        avg_wait_time = sum(c.wait_time for c in self.served_customers) / total_served
        avg_service_time = sum(c.service_time for c in self.served_customers) / total_served
        total_time = (datetime.now() - self.start_time).total_seconds()
        
        service_breakdown = {}
        for customer in self.served_customers:
            service = customer.service_type.value
            service_breakdown[service] = service_breakdown.get(service, 0) + 1
        
        return {
            'total_served': total_served,
            'avg_wait_time': avg_wait_time,
            'avg_service_time': avg_service_time,
            'total_time': total_time,
            'service_breakdown': service_breakdown
        }
