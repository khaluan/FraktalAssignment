from abc import ABC, abstractmethod
class SizeRateController(ABC):
    @abstractmethod
    def dissect(self, payload: str | bytes) -> list[str | bytes]:
        """
        Dissect the payload into smaller parts.

        Args:
            payload (str | bytes): The payload to dissect.

        Returns:
            list[str | bytes]: The dissected parts.
        """
        pass

class TimeRateController():
    @abstractmethod
    def get_pauses(self, request_no: int) -> list[float]:
        """
        Get the pauses between requests.

        Args:
            request_no (int): The number of requests to make.
        
        Returns:
            list[float]: The pauses between requests.
        """      
        pass