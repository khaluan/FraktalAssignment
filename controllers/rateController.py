from controllers.interface import SizeRateController, TimeRateController

import random

class NormalSizeRateController(SizeRateController):
    def __init__(self):
        pass

    def dissect(self, payload: str | bytes) -> list[str | bytes]:
        return [payload]

class NormalTimeRateController(TimeRateController):
    def __init__(self):
        pass

    def get_pauses(self, request_no: int) -> list[float]:
        return [0 for i in range(request_no - 1)]


class RandomBalanceRateController(SizeRateController):
    def __init__(self, avg_rate: int):
        """
        Initialize the RandomBalanceRateController with the average size of payload per packet
        This controller will randomly select a chunk size around the average size with deviation of 0.2 average rate.
        
        Args:
            average_rate (int): The average size of payload per packet, e.g., 180 bytes
        """
        self.avg_rate = avg_rate

    def dissect(self, payload: str | bytes) -> list[str | bytes]:
        total_length = len(payload)
        num_chunks = total_length // self.avg_rate  # Estimate the number of chunks
        
        chunks = []
        current_position = 0

        for i in range(num_chunks):
            # Randomly select a chunk size around avg_chunk_size
            chunk_size = random.randint(int(0.8 * self.avg_rate), int(1.2 * self.avg_rate))  # Random with deviation 0.2
            chunk_size = min(chunk_size, total_length - current_position)  # Avoid exceeding string length

            chunk = payload[current_position:current_position + chunk_size]
            chunks.append(chunk)

            current_position += chunk_size

        # Handle remaining bytes (if any)
        if current_position < total_length:
            remaining_chunk = payload[current_position:]
            chunks.append(remaining_chunk)

        return chunks
    
class TimeBaseController(TimeRateController):
    def __init__(self, max_connections: int):
        """
        Initialize the TimeBaseController with the maximum number of connections per second
        This controller will returns a list of random pauses based on the number of connections, and the average connection rate        
        Args:
            max_connections (int): The maximum number of connections per second, e.g., 10 or 0.5 if 2 seconds per connection
        """
        self.max_connections = max_connections

    def get_pauses(self, request_no: int) -> list[float]:

        # Calculate the time pauses based on the number of connections
        pauses = [random.random() * (1 / self.max_connections) for _ in range(request_no - 1)]
        return pauses