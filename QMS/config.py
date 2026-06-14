"""
Bank Queue Management System - Configuration & Utilities
"""

# System Configuration
CONFIG = {
    "NUM_COUNTERS": 3,
    "AUTO_REFRESH_INTERVAL": 1000,  # milliseconds
    "WINDOW_WIDTH": 1400,
    "WINDOW_HEIGHT": 800,
    "APP_TITLE": "Bank Queue Management System",
}

# Color Theme
COLORS = {
    "PRIMARY": "#2E86AB",
    "SUCCESS": "#06A77D",
    "WARNING": "#D62828",
    "INFO": "#F77F00",
    "BACKGROUND": "#f0f0f0",
    "TEXT": "#333333",
    "BORDER": "#cccccc",
}

# Sample customer names for testing
SAMPLE_NAMES = [
    "John Smith", "Mary Johnson", "Robert Brown", "Patricia Davis",
    "Michael Wilson", "Jennifer Taylor", "William Anderson", "Barbara Thomas",
    "David Moore", "Susan Jackson", "Richard White", "Jessica Harris",
    "Joseph Martin", "Sarah Thompson", "Thomas Garcia", "Karen Martinez",
]

# Sample services distribution
SAMPLE_SERVICES = [
    "Deposit", "Withdrawal", "Loan Application", "Account Opening", "General Query"
]
