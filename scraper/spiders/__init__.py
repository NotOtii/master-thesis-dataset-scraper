def __init__(self, config=None, config_path=None, run_id="run_001", *args, **kwargs):
    super().__init__(*args, **kwargs)

    if config is None:
        raise ValueError("A config dictionary must be provided to BooksSpider.")

    self.config = config
    self.config_path = config_path
    self.run_id = run_id
    self.source_name = config["source_name"]
    self.start_urls = config["start_urls"]
    self.allowed_domains = config["allowed_domains"]

