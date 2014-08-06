#!/usr/bin/env bash

scrapy crawl companies -o temp_companies.json
python3 review.py merge