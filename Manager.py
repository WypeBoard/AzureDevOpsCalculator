import csv

from calculations import Calculation
from model import PullRequests


class Manager:
    def __init__(self, raw_data: list[PullRequests]):
        self.raw_data = raw_data
        self.calculations = []
        
    def register_calculation(self, calculation_class: Calculation) -> None:
        calculation = calculation_class()
        calculation.prepare_data(self.raw_data)
        self.calculations.append(calculation)
        
    def execute(self) -> None:
        for calculation in self.calculations:
            results = calculation.calculate()
            filename = calculation.export_file_name()
            print(results)
            self.save_to_csv(filename, results)
            
    def save_to_csv(self, filename: str, data: dict) -> None:
        if not data:
            return
        with open(f'{filename}.csv', 'w', newline='', encoding='utf-8') as csvFile:
            write = csv.DictWriter(csvFile, fieldnames=data[0].keys())
            write.writeheader()
            write.writerows(data)