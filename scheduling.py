from datetime import datetime
class QuoteScheduler:
    def __init__(self, interval_days: int):
        self._date = None
        self._interval_days = interval_days
        self._is_recurring = True if interval_days > 0 else False
    
    def is_valid_interval(self) -> bool:
        return self._interval_days >= 0
        
    def is_valid_schedule(self, schedule: str) -> bool:
        format = "%m-%d-%y %H:%M"    
        try:    
            self._date = datetime.strptime(schedule, format)
            return True
        except ValueError:
            return False

    def calculate_delay(self, now: datetime) -> datetime:
        return (self._date - now).total_seconds()
        
    def to_string(self) -> str:
        return datetime.strftime(self._date, "%m-%d-%Y %H:%M")