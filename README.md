# ntl-metrics-ingest

This is script that takes data from a specific CSV file format and uploads data to a specific Google Sheets document.

## Getting Started

### Prerequisites

- Python 3
- Google Sheets

### Installing

1. Set your credentials and Google Sheets ID in `config.yml`. See `config.template.yml` for filler values.
1. Open up the "views" file in Atom and save it as `views.csv` in the repository folder.
1. Open up the "downloads" file in Atom and save it as `downloads.csv` in the repository folder.
1. Activate virtualenv: `virtualenv -p python3 virtualenv && source virtualenv/bin/activate`
1. Install Python package requirements: `pip install -r requirements`
1. Run the script: `python metrics_ntl.py --csv`

## Contributing

Please contribute to this repository using GitHub Pull Requests and GitHub Issues.

## Authors

The Developers of ITS DataHub.

## License

This project is licensed under the Apache 2.0 License.

## Code.gov Registration Info

Agency: DOT
Short Description: NTL metrics upload convenience script.
Status: Beta
Tags: transportation, connected vehicles, intelligent transportation systems, python
Labor Hours: 0
Contact Name: Brian Brotsos
Contact Phone: 