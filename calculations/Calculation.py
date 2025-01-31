from abc import ABC, abstractmethod

from model import PullRequests


class Calculation(ABC):
    
    @abstractmethod
    def prepare_data(self, data: list[PullRequests]) -> None:
        """
        Prepare and preprocess the data for calculations.
        """
        pass
    
    @abstractmethod    
    def calculate(self) -> list:
        """
        Perform the calculation and return results as a dictionary.
        """
        pass

    @abstractmethod
    def export_file_name(self) -> str:
        """
        Return the name of the file to save the results.
        """
        pass