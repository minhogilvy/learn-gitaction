from datetime import datetime, timezone, timedelta
from typing import Optional


class DateTimeUtils:
    @staticmethod
    def parse_datetime(date_str: str, fmt: str = "%Y-%m-%d %H:%M:%S", tz: Optional[timezone] = None) -> datetime:
        """
        Parse a datetime string into a datetime object.

        :param date_str: The datetime string.
        :param fmt: The format of the datetime string.
        :param tz: The timezone to localize the datetime object.
        :return: A datetime object.
        """
        dt = datetime.strptime(date_str, fmt)
        if tz:
            dt = dt.replace(tzinfo=tz)
        return dt
    
    @staticmethod
    def format_datetime(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S", tz: Optional[timezone] = None) -> str:
        """
        Format a datetime object into a string.

        :param dt: The datetime object.
        :param fmt: The format to output the datetime string.
        :param tz: The timezone to convert the datetime object to before formatting.
        :return: A formatted datetime string.
        """
        if tz:
            dt = dt.astimezone(tz)
        return dt.strftime(fmt)
    
    @staticmethod
    def convert_timezone(dt: datetime, to_tz: timezone) -> datetime:
        """
        Convert a datetime object to a different timezone.

        :param dt: The datetime object.
        :param to_tz: The timezone to convert to.
        :return: A datetime object in the target timezone.
        """
        return dt.astimezone(to_tz)
    
    @staticmethod
    def get_current_datetime(tz: Optional[timezone] = None) -> datetime:
        """
        Get the current datetime. Optionally, localize it to a specific timezone.

        :param tz: The timezone to localize the current datetime.
        :return: A datetime object.
        """
        dt = datetime.now(timezone.utc)
        if tz:
            dt = dt.astimezone(tz)
        return dt
    
    @staticmethod
    def format_to_readable(dt: datetime, tz: Optional[timezone] = None) -> str:
        """
        Format a datetime object into a human-readable string like.

        :param dt: The datetime object.
        :param tz: The timezone to convert to before formatting.
        :return: A formatted datetime string.
        """
        if tz:
            dt = dt.astimezone(tz)
        return dt.strftime("%B %d, %Y at %I:%M:%S %p %Z")
    
    @staticmethod
    def get_current_timestamp() -> int:
        """
        Get the current timestamp in seconds since the epoch (January 1, 1970, 00:00:00 UTC).

        :return: The current timestamp as an integer.
        """
        return int(datetime.now(timezone.utc).timestamp())
    
    @staticmethod
    def get_current_time_readable(tz: Optional[timezone] = None) -> str:
        """
        Get the current time in a human-readable format like.

        :param tz: The timezone to localize the current time.
        :return: A human-readable string of the current time.
        """
        dt = DateTimeUtils.get_current_datetime(tz)
        return DateTimeUtils.format_to_readable(dt)
