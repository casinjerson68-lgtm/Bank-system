"""
Bank Queue Management System - Tkinter GUI
Main graphical interface for the bank queue management system
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from queue import BankQMS, ServiceType, CustomerPriority
from datetime import datetime


class BankQMSGUI:
    """Tkinter GUI for Bank Queue Management System"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Queue Management System")
        self.root.geometry("1400x800")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize QMS with 3 counters
        self.qms = BankQMS(num_counters=3)
        
        # Set up styles
        self.setup_styles()
        
        # Create GUI components
        self.create_widgets()
        
        # Start auto-refresh
        self.auto_refresh()
    
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use("clam")
        
        # Define colors
        self.primary_color = "#2E86AB"
        self.success_color = "#06A77D"
        self.warning_color = "#D62828"
        self.info_color = "#F77F00"
        self.bg_color = "#f0f0f0"
        
        # Configure styles
        style.configure("Title.TLabel", font=("Arial", 16, "bold"), background=self.bg_color)
        style.configure("Header.TLabel", font=("Arial", 12, "bold"), background=self.bg_color)
        style.configure("Normal.TLabel", font=("Arial", 10), background=self.bg_color)
        style.configure("Button.TButton", font=("Arial", 10))
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Title
        title_label = ttk.Label(self.root, text="Bank Queue Management System", style="Title.TLabel")
        title_label.pack(pady=10, fill="x")
        
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Left panel - Add Customer
        left_frame = ttk.LabelFrame(main_frame, text="Add New Customer", padding=10)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        self.create_add_customer_panel(left_frame)
        
        # Middle panel - Queue Display
        middle_frame = ttk.LabelFrame(main_frame, text="Current Queue", padding=10)
        middle_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5, rowspan=2)
        
        self.create_queue_display_panel(middle_frame)
        
        # Right panel - Counter Status
        right_frame = ttk.LabelFrame(main_frame, text="Counter Status", padding=10)
        right_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        
        self.create_counter_status_panel(right_frame)
        
        # Statistics panel
        stats_frame = ttk.LabelFrame(main_frame, text="Statistics", padding=10)
        stats_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        self.create_statistics_panel(stats_frame)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=2)
        main_frame.columnconfigure(2, weight=1)
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
    
    def create_add_customer_panel(self, parent):
        """Create the add customer panel"""
        # Name
        ttk.Label(parent, text="Name:", style="Normal.TLabel").grid(row=0, column=0, sticky="w", pady=5)
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(parent, textvariable=self.name_var, width=25)
        name_entry.grid(row=0, column=1, sticky="w", pady=5)
        
        # Service Type
        ttk.Label(parent, text="Service Type:", style="Normal.TLabel").grid(row=1, column=0, sticky="w", pady=5)
        self.service_var = tk.StringVar(value=ServiceType.DEPOSIT.value)
        service_combo = ttk.Combobox(
            parent,
            textvariable=self.service_var,
            values=[s.value for s in ServiceType],
            state="readonly",
            width=22
        )
        service_combo.grid(row=1, column=1, sticky="w", pady=5)
        
        # Priority
        ttk.Label(parent, text="Priority:", style="Normal.TLabel").grid(row=2, column=0, sticky="w", pady=5)
        self.priority_var = tk.StringVar(value=CustomerPriority.STANDARD.name)
        priority_combo = ttk.Combobox(
            parent,
            textvariable=self.priority_var,
            values=[p.name for p in CustomerPriority],
            state="readonly",
            width=22
        )
        priority_combo.grid(row=2, column=1, sticky="w", pady=5)
        
        # Add Button
        add_button = ttk.Button(parent, text="Add Customer", command=self.add_customer)
        add_button.grid(row=3, column=0, columnspan=2, sticky="ew", pady=15)
        
        # Status message
        self.status_label = ttk.Label(parent, text="", style="Normal.TLabel", foreground="green")
        self.status_label.grid(row=4, column=0, columnspan=2, sticky="w")
    
    def create_queue_display_panel(self, parent):
        """Create the queue display panel"""
        # Create treeview
        columns = ("Pos", "Ticket", "Name", "Service", "Priority", "Status")
        self.queue_tree = ttk.Treeview(parent, columns=columns, height=15, show="headings")
        
        # Define column headings and widths
        self.queue_tree.heading("Pos", text="Pos")
        self.queue_tree.heading("Ticket", text="Ticket")
        self.queue_tree.heading("Name", text="Name")
        self.queue_tree.heading("Service", text="Service")
        self.queue_tree.heading("Priority", text="Priority")
        self.queue_tree.heading("Status", text="Status")
        
        self.queue_tree.column("Pos", width=30)
        self.queue_tree.column("Ticket", width=50)
        self.queue_tree.column("Name", width=100)
        self.queue_tree.column("Service", width=100)
        self.queue_tree.column("Priority", width=80)
        self.queue_tree.column("Status", width=60)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.queue_tree.yview)
        self.queue_tree.configure(yscroll=scrollbar.set)
        
        # Pack
        self.queue_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Queue info label
        self.queue_info_label = ttk.Label(parent, text="Customers waiting: 0", style="Normal.TLabel")
        self.queue_info_label.pack(pady=5)
    
    def create_counter_status_panel(self, parent):
        """Create the counter status panel"""
        self.counter_labels = {}
        
        for i in range(1, 4):
            frame = ttk.Frame(parent)
            frame.pack(fill="x", pady=5)
            
            # Counter number
            ttk.Label(frame, text=f"Counter {i}:", style="Header.TLabel", width=15).pack(side="left")
            
            # Status label
            status_label = ttk.Label(frame, text="AVAILABLE", style="Normal.TLabel", foreground="green")
            status_label.pack(side="left", padx=5)
            
            self.counter_labels[i] = status_label
        
        # Serve button
        ttk.Button(parent, text="Serve Next Customer", command=self.serve_next_customer).pack(fill="x", pady=10)
        
        # Complete service section
        ttk.Label(parent, text="Complete Service At:", style="Header.TLabel").pack(pady=(20, 5))
        
        for i in range(1, 4):
            ttk.Button(
                parent,
                text=f"Complete Counter {i}",
                command=lambda counter_id=i: self.complete_service(counter_id)
            ).pack(fill="x", pady=2)
    
    def create_statistics_panel(self, parent):
        """Create the statistics panel"""
        columns = ("Metric", "Value")
        self.stats_tree = ttk.Treeview(parent, columns=columns, height=8, show="headings")
        
        self.stats_tree.heading("Metric", text="Metric")
        self.stats_tree.heading("Value", text="Value")
        
        self.stats_tree.column("Metric", width=150)
        self.stats_tree.column("Value", width=150)
        
        self.stats_tree.pack(fill="both", expand=True)
    
    def add_customer(self):
        """Add a customer to the queue"""
        name = self.name_var.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Please enter customer name")
            return
        
        # Get service type
        service_name = self.service_var.get()
        service_type = next(s for s in ServiceType if s.value == service_name)
        
        # Get priority
        priority_name = self.priority_var.get()
        priority = next(p for p in CustomerPriority if p.name == priority_name)
        
        # Add customer
        customer, ticket_num = self.qms.add_customer(name, service_type, priority)
        
        # Update status
        self.status_label.config(
            text=f"✓ {name} added (Ticket: {ticket_num}, Position: {self.qms.bank_queue.get_queue_size()})",
            foreground="green"
        )
        
        # Clear input
        self.name_var.set("")
        
        # Refresh display
        self.refresh_display()
    
    def serve_next_customer(self):
        """Serve the next customer"""
        customer, counter = self.qms.assign_customer_to_counter()
        
        if customer and counter:
            messagebox.showinfo(
                "Customer Assigned",
                f"{customer.name} is now being served at Counter {counter.counter_id}"
            )
        elif not customer:
            messagebox.showinfo("Queue Empty", "No customers waiting in queue")
        else:
            messagebox.showinfo("All Busy", "All counters are currently busy")
        
        self.refresh_display()
    
    def complete_service(self, counter_id):
        """Complete service at a counter"""
        customer = self.qms.complete_service(counter_id)
        
        if customer:
            wait_time = customer.wait_time / 60  # Convert to minutes
            service_time = customer.service_time / 60  # Convert to minutes
            
            messagebox.showinfo(
                "Service Completed",
                f"Service completed for {customer.name}\n"
                f"Wait Time: {wait_time:.1f} minutes\n"
                f"Service Time: {service_time:.1f} minutes"
            )
        else:
            messagebox.showinfo("Counter Available", f"Counter {counter_id} is not serving anyone")
        
        self.refresh_display()
    
    def refresh_display(self):
        """Refresh all display panels"""
        self.update_queue_display()
        self.update_counter_status()
        self.update_statistics()
    
    def update_queue_display(self):
        """Update the queue display"""
        # Clear existing items
        for item in self.queue_tree.get_children():
            self.queue_tree.delete(item)
        
        # Add customers
        customers = self.qms.bank_queue.view_queue()
        for i, customer in enumerate(customers, 1):
            self.queue_tree.insert(
                "",
                "end",
                values=(
                    i,
                    customer.ticket_number,
                    customer.name,
                    customer.service_type.value,
                    customer.priority.name,
                    customer.status
                )
            )
        
        # Update queue info
        queue_size = self.qms.bank_queue.get_queue_size()
        self.queue_info_label.config(text=f"Customers waiting: {queue_size}")
    
    def update_counter_status(self):
        """Update counter status display"""
        counter_status = self.qms.get_counter_status()
        
        for status in counter_status:
            counter_id = status['counter_id']
            label = self.counter_labels[counter_id]
            
            if status['is_busy']:
                wait_time = status['wait_time'] / 60  # Convert to minutes
                label.config(
                    text=f"BUSY - {status['customer_name']} ({wait_time:.1f}m)",
                    foreground="orange"
                )
            else:
                label.config(text="AVAILABLE", foreground="green")
    
    def update_statistics(self):
        """Update statistics display"""
        stats = self.qms.get_statistics()
        
        # Clear existing items
        for item in self.stats_tree.get_children():
            self.stats_tree.delete(item)
        
        # Add statistics
        self.stats_tree.insert("", "end", values=("Total Served", stats['total_served']))
        self.stats_tree.insert("", "end", values=("Avg Wait Time", f"{stats['avg_wait_time']/60:.2f} min"))
        self.stats_tree.insert("", "end", values=("Avg Service Time", f"{stats['avg_service_time']/60:.2f} min"))
        self.stats_tree.insert("", "end", values=("System Uptime", f"{stats['total_time']/60:.1f} min"))
        
        # Service breakdown
        for service, count in stats['service_breakdown'].items():
            self.stats_tree.insert("", "end", values=(f"{service}", count))
    
    def auto_refresh(self):
        """Automatically refresh the display every second"""
        self.refresh_display()
        self.root.after(1000, self.auto_refresh)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = BankQMSGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
