# Bank Queue Management System (GUI)

A comprehensive, user-friendly tkinter-based queue management system designed specifically for bank operations. This system handles customer queuing, priority management, service counter allocation, and real-time analytics with a modern graphical interface.

## Features

### 🎯 Core Functionality
- **Graphical User Interface**: Intuitive tkinter GUI with real-time updates
- **Priority Queue Management**: Automatic sorting by customer priority and arrival time
- **Multiple Service Counters**: Support for simultaneous service at multiple counters
- **Automatic Customer Assignment**: Intelligently assigns customers to available counters
- **Real-time Status Updates**: Live monitoring of queue and counter status every second
- **Ticket System**: Unique ticket numbers for each customer

### 📋 Service Types
- Deposits
- Withdrawals
- Loan Applications
- Account Opening
- General Queries

### 👥 Customer Priorities
1. **Standard** - Regular customers
2. **Senior Citizens** - Priority service for elderly customers
3. **Disabled** - Accessibility priority
4. **VIP** - Premium customers (highest priority)

### 📊 Real-time Monitoring
- **Queue Display**: View all waiting customers with position, ticket number, service type, and priority
- **Counter Status**: Monitor each counter's availability and current customer
- **Live Statistics**: Track total served, average wait times, average service times, and service breakdown
- **System Uptime**: Monitor how long the system has been running

## Installation

### Requirements
- Python 3.6 or higher
- tkinter (usually comes with Python)

### Setup
```bash
# No external dependencies required - tkinter is part of standard Python
# Simply navigate to the QMS directory and run:
python main.py
```

## File Structure

```
QMS/
├── queue.py          # Core business logic and data models
├── main.py           # Tkinter GUI application
├── config.py         # Configuration and constants
└── README.md         # This file
```

## Usage Guide

### Starting the Application
```bash
python main.py
```

### Interface Overview

The application window is divided into four main sections:

#### 1. **Add New Customer Panel** (Top-Left)
- Enter customer name
- Select service type from dropdown
- Choose customer priority level
- Click "Add Customer" to add to queue

#### 2. **Current Queue Panel** (Top-Center)
- Displays all waiting customers
- Shows position in queue, ticket number, name, service type, priority, and status
- Automatically sorted by priority

#### 3. **Counter Status Panel** (Top-Right)
- Shows status of each counter (AVAILABLE or BUSY)
- Displays current customer and wait time for busy counters
- "Serve Next Customer" button to assign next in queue
- Individual "Complete Counter X" buttons to finish service

#### 4. **Statistics Panel** (Bottom-Left)
- Total customers served
- Average wait time (in minutes)
- Average service time (in minutes)
- System uptime (in minutes)
- Service type breakdown

### Step-by-Step Example

1. **Add Customers**
   - Enter name: "John Smith"
   - Select Service: "Deposit"
   - Select Priority: "Standard"
   - Click "Add Customer"

2. **Serve Customers**
   - Click "Serve Next Customer"
   - System automatically assigns to available counter

3. **Complete Service**
   - When service is done, click "Complete Counter 1" (or appropriate counter)
   - System records wait time and service time

4. **Monitor Progress**
   - Queue display updates automatically
   - Statistics update in real-time
   - Counter status changes as customers are served

## Technical Architecture

### Classes Overview

#### `Customer`
Represents an individual customer with:
- Unique ID and ticket number
- Arrival time tracking
- Wait time and service time calculation
- Status tracking (Waiting, Being Served, Completed)

#### `ServiceCounter`
Represents a service counter/teller with:
- Current customer tracking
- Service statistics (total served, average time)
- Busy/available status

#### `BankQueue`
Priority queue implementation with:
- Automatic sorting by priority and arrival time
- Ticket number generation
- Customer lookup and removal

#### `BankQMS`
Main orchestrator that:
- Manages all counters
- Handles customer assignment
- Generates statistics and reports

#### `BankQMSGUI`
Tkinter GUI application that:
- Displays all information
- Handles user interactions
- Auto-refreshes every second

### Data Flow

```
User Input → GUI Event Handler → QMS Logic → Update Display → Auto-Refresh
```

## Configuration

Edit `config.py` to customize:
- Number of service counters
- Auto-refresh interval
- Window dimensions
- Color theme
- Sample data

## System Statistics Explained

### Total Served
Number of customers who have completed service since system startup.

### Average Wait Time
Mean time customers waited from arrival to start of service.

### Average Service Time
Mean duration of service for each customer.

### System Uptime
Total time the system has been running since initialization.

### Service Breakdown
Count of customers served for each service type.

## Performance Characteristics

- **Real-time Updates**: Display refreshes every 1 second
- **Scalability**: Can handle hundreds of customers efficiently
- **Priority Handling**: Customers with higher priority are always served first
- **Concurrent Service**: Multiple customers can be served simultaneously

## Common Use Cases

### Morning Operations
1. Start the system
2. Add customers as they arrive
3. System automatically manages queue and counter assignments

### Peak Hours
- System handles unlimited queue size
- Multiple counters serve simultaneously
- Real-time statistics help identify bottlenecks

### End of Day
- Review statistics to analyze performance
- Identify service type patterns
- Plan resource allocation for next day

## Tips & Best Practices

1. **Ensure Accurate Priority**: Set correct priority when adding customers
2. **Monitor Counters**: Keep an eye on counter utilization
3. **Regular Service Completion**: Ensure counters are cleared promptly
4. **Review Statistics**: Use end-of-day statistics to improve efficiency
5. **Fair Service**: System automatically ensures fair FIFO service within priority levels

## Troubleshooting

### No customers in queue?
- Ensure you've added customers using the "Add New Customer" panel

### Counter showing as busy but no customer?
- This shouldn't happen; try completing the service at that counter

### Display not updating?
- Auto-refresh happens every second; changes should appear shortly

### Performance issues with many customers?
- System is optimized for 100+ customers but may slow if over 1000
- Consider running a new session to clear completed customer history

## Future Enhancements

Potential improvements for future versions:
- Customer notification system
- Estimated wait time calculation
- Peak hour analysis and forecasting
- Customer satisfaction ratings
- Integration with bank database
- Advanced reporting and data export
- Multi-branch support
- Machine learning for optimization

## System Requirements

| Requirement | Specification |
|-------------|--------------|
| Python Version | 3.6+ |
| Memory | Minimal (~50MB) |
| Disk Space | <1MB |
| OS Compatibility | Windows, macOS, Linux |
| GUI Framework | tkinter (built-in) |

## Code Example

```python
from queue import BankQMS, ServiceType, CustomerPriority

# Initialize system
qms = BankQMS(num_counters=3)

# Add customer
customer, ticket = qms.add_customer(
    "Jane Doe",
    ServiceType.LOAN_APPLICATION,
    CustomerPriority.VIP
)

# Serve next customer
customer, counter = qms.assign_customer_to_counter()

# Complete service
served_customer = qms.complete_service(counter_id=1)

# Get statistics
stats = qms.get_statistics()
print(f"Total served: {stats['total_served']}")
```

## License

This is a demonstration system for educational purposes.

## Support

For issues or questions, please refer to the code comments and class docstrings included in each module.

---

**Last Updated**: 2024
**Version**: 1.0
**Status**: Production Ready
