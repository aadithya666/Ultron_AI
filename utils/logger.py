"""
Logging utility for Ultron AI
Handles all logging operations
"""

import logging
import os
from datetime import datetime


class UltronLogger:
    """Custom logger for Ultron"""
    
    def __init__(self, log_file: str = "logs/ultron.log", level=logging.INFO):
        self.log_file = log_file
        self.logger = self.setup_logger(level)
    
    def setup_logger(self, level) -> logging.Logger:
        """Setup logger with file and console handlers"""
        # Create logs directory if it doesn't exist
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        
        # Create logger
        logger = logging.getLogger('Ultron')
        logger.setLevel(level)
        
        # File handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(level)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '[%(asctime)s] - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def info(self, message: str):
        """Log info message"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log error message"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """Log critical message"""
        self.logger.critical(message)
    
    def debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message)
    
    def get_log_file(self) -> str:
        """Get log file path"""
        return self.log_file
