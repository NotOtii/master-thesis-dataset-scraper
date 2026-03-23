import json
import csv
from pathlib import Path
from scraper.validators import validate_book_item


class DatasetWriterPipeline:
    def open_spider(self, spider):
        self.output_dir = Path("data/output")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.items = []
        self.valid_count = 0
        self.invalid_count = 0
        self.invalid_items = []

    def close_spider(self, spider):
        json_path = self.output_dir / f"{spider.name}_output.json"
        csv_path = self.output_dir / f"{spider.name}_output.csv"
        report_path = self.output_dir / f"{spider.name}_run_report.json"

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(self.items, f, ensure_ascii=False, indent=2)

        if self.items:
            fieldnames = list(self.items[0].keys())
            with open(csv_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.items)

        report = {
            "run_id": getattr(spider, "run_id", "unknown"),
            "source_name": getattr(spider, "source_name", "unknown"),
            "records_extracted": self.valid_count + self.invalid_count,
            "records_valid": self.valid_count,
            "records_invalid": self.invalid_count,
            "invalid_examples": self.invalid_items[:5],
        }

        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

    def process_item(self, item, spider):
        item_dict = dict(item)
        is_valid, errors = validate_book_item(item_dict)

        if is_valid:
            self.items.append(item_dict)
            self.valid_count += 1
        else:
            self.invalid_count += 1
            self.invalid_items.append({
                "item": item_dict,
                "errors": errors,
            })

        return item