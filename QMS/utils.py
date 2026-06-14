"""
Advanced utilities for the Bank QMS
"""

from datetime import datetime
import json
from queue import BankQMS


class QMSExporter:
    """Export QMS data and generate reports"""
    
    @staticmethod
    def export_statistics_to_json(qms: BankQMS, filename: str = "qms_stats.json"):
        """Export statistics to JSON file"""
        stats = qms.get_statistics()
        
        data = {
            "timestamp": datetime.now().isoformat(),
            "statistics": {
                "total_served": stats['total_served'],
                "avg_wait_time_seconds": stats['avg_wait_time'],
                "avg_service_time_seconds": stats['avg_service_time'],
                "system_uptime_seconds": stats['total_time'],
                "service_breakdown": stats['service_breakdown']
            },
            "counters": []
        }
        
        # Add counter statistics
        for counter in qms.counters:
            data["counters"].append({
                "counter_id": counter.counter_id,
                "customers_served": counter.customers_served,
                "avg_service_time": counter.get_average_service_time()
            })
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        return filename
    
    @staticmethod
    def generate_text_report(qms: BankQMS):
        """Generate a text report of system status"""
        stats = qms.get_statistics()
        counter_status = qms.get_counter_status()
        
        report = []
        report.append("\n" + "="*70)
        report.append("BANK QUEUE MANAGEMENT SYSTEM - REPORT")
        report.append("="*70)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Overall Statistics
        report.append("OVERALL STATISTICS")
        report.append("-"*70)
        report.append(f"Total Customers Served:        {stats['total_served']}")
        report.append(f"Average Wait Time:             {stats['avg_wait_time']/60:.2f} minutes")
        report.append(f"Average Service Time:          {stats['avg_service_time']/60:.2f} minutes")
        report.append(f"System Uptime:                 {stats['total_time']/60:.2f} minutes\n")
        
        # Service Breakdown
        if stats['service_breakdown']:
            report.append("SERVICE BREAKDOWN")
            report.append("-"*70)
            for service, count in stats['service_breakdown'].items():
                percentage = (count / stats['total_served'] * 100) if stats['total_served'] > 0 else 0
                report.append(f"{service:<30} {count:>5} ({percentage:>5.1f}%)")
            report.append()
        
        # Counter Performance
        report.append("COUNTER PERFORMANCE")
        report.append("-"*70)
        total_served = sum(c.customers_served for c in qms.counters)
        
        for counter in qms.counters:
            status = "BUSY" if counter.is_busy else "AVAILABLE"
            report.append(f"Counter {counter.counter_id}:")
            report.append(f"  Status:                   {status}")
            report.append(f"  Customers Served:         {counter.customers_served}")
            report.append(f"  Average Service Time:     {counter.get_average_service_time()/60:.2f} minutes")
            report.append()
        
        # Queue Status
        report.append("QUEUE STATUS")
        report.append("-"*70)
        report.append(f"Customers Waiting:             {qms.bank_queue.get_queue_size()}")
        report.append(f"Busy Counters:                 {sum(1 for s in counter_status if s['is_busy'])}/{len(qms.counters)}")
        report.append(f"Available Counters:            {sum(1 for s in counter_status if not s['is_busy'])}/{len(qms.counters)}\n")
        
        report.append("="*70)
        
        return "\n".join(report)
    
    @staticmethod
    def get_performance_summary(qms: BankQMS):
        """Get a quick performance summary"""
        stats = qms.get_statistics()
        counter_status = qms.get_counter_status()
        
        busy_counters = sum(1 for s in counter_status if s['is_busy'])
        
        summary = {
            "queue_length": qms.bank_queue.get_queue_size(),
            "total_served": stats['total_served'],
            "busy_counters": busy_counters,
            "available_counters": len(qms.counters) - busy_counters,
            "avg_wait_minutes": stats['avg_wait_time'] / 60,
            "avg_service_minutes": stats['avg_service_time'] / 60,
        }
        
        return summary


def demo_advanced_features():
    """Demonstrate advanced features"""
    from queue import ServiceType, CustomerPriority
    
    qms = BankQMS(num_counters=3)
    
    # Add test data
    qms.add_customer("Test User 1", ServiceType.DEPOSIT, CustomerPriority.STANDARD)
    qms.add_customer("Test User 2", ServiceType.WITHDRAWAL, CustomerPriority.VIP)
    
    qms.assign_customer_to_counter()
    
    # Generate reports
    print(QMSExporter.generate_text_report(qms))
    
    # Get performance summary
    summary = QMSExporter.get_performance_summary(qms)
    print("\nPERFORMANCE SUMMARY:")
    for key, value in summary.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    demo_advanced_features()
