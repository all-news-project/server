# Build folder
rm -r scrapers_build
mkdir scrapers_build

# Scrapers
mkdir scrapers_build/scrapers
cp -r ../scraper_drivers scrapers_build/scrapers
cp -r ../websites_scrapers scrapers_build/scrapers
cp ../__init__.py scrapers_build/scrapers
cp ../logic_scraper.py scrapers_build/scrapers
cp ../run.py scrapers_build/scrapers

# Utils
cp -r ../../../server_utils/* scrapers_build/scrapers
