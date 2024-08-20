# arxivDashboard

## Project Overview
This project involves creating an interactive dashboard using DASH to visualize data from the ArXiv preprint server. The dashboard extracts project data from ArXiv, categorizes the papers, and displays a chart showing the number of papers published over time, categorized by paper type.

## Features
- **Data Extraction**: Retrieves project data from the ArXiv API.
- **Data Visualization**: Presents a chart showing the number of papers published over days, categorized by their type.
- **Interactive Dashboard**: Built using DASH for an interactive and user-friendly experience.

## Installation
1. **Clone the repository**:
    ```bash
    git clone https://github.com/rujeetjahagirdar/arxivDashboard.git
    cd arxiv-dashboard
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. **Run the DASH application**:
    ```bash
    python app.py
    ```

    Open your web browser and go to `http://127.0.0.1:8050/` to view the dashboard.

## Implementation Details
1. **Data Extraction**:
    - Uses the ArXiv API to fetch paper data.
    - Parses and categorizes the papers based on their fields.

2. **Data Visualization**:
    - Uses Plotly to create a chart displaying the number of papers published over time.
    - Categorizes papers by their subject areas for better insights.

## Contributing
Feel free to fork the repository and submit pull requests with improvements or additional features.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## References
1. [ArXiv API Documentation](https://arxiv.org/help/api/user-manual)
2. [DASH Documentation](https://dash.plotly.com/introduction)
3. [Plotly Documentation](https://plotly.com/python/)
