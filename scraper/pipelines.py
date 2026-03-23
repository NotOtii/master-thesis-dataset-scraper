import json
import csv
import shutil
from pathlib import Path
from datetime import datetime, timezone

from scraper.validators import validate_book_item


class DatasetWriterPipeline:
    def open_spider(self, spider):
        self.output_dir = Path("data/output")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.items = []
        self.valid_count = 0
        self.invalid_count = 0
        self.duplicates_removed = 0
        self.invalid_items = []
        self.seen_record_ids = set()

        self.started_at = datetime.now(timezone.utc)

        config_path = getattr(spider, "config_path", None)
        if config_path:
            destination = self.output_dir / f"{spider.name}_run_config.yaml"
            shutil.copyfile(config_path, destination)

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

        finished_at = datetime.now(timezone.utc)
        duration_seconds = (finished_at - self.started_at).total_seconds()

        report = {
            "run_id": getattr(spider, "run_id", "unknown"),
            "source_name": getattr(spider, "source_name", "unknown"),
            "started_at": self.started_at.isoformat(),
            "finished_at": finished_at.isoformat(),
            "duration_seconds": duration_seconds,
            "records_extracted": self.valid_count + self.invalid_count + self.duplicates_removed,
            "records_valid": self.valid_count,
            "records_invalid": self.invalid_count,
            "duplicates_removed": self.duplicates_removed,
            "output_json": str(json_path),
            "output_csv": str(csv_path),
            "invalid_examples": self.invalid_items[:5],
        }

        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

    def process_item(self, item, spider):
        item_dict = dict(item)
        is_valid, errors = validate_book_item(item_dict)

        if not is_valid:
            self.invalid_count += 1
            self.invalid_items.append({
                "item": item_dict,
                "errors": errors,
            })
            return item

        record_id = item_dict.get("record_id")
        if record_id in self.seen_record_ids:
            self.duplicates_removed += 1
            return item

        self.seen_record_ids.add(record_id)
        self.items.append(item_dict)
        self.valid_count += 1
        return item