import dash
from dash import dcc
from dash import html
import plotly.express as px
import psycopg2

# Database connection parameters
db_params = {
    'host': 'localhost',
    'port': '5432',
    'user': 'postgres',
    'password': 'postgres',
    'options': '-c search_path=paper_monitoring'
}

# Connect to the PostgreSQL database
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Retrieve the data from the database
select_data_query = """
SELECT date_trunc('day', published) AS publication_date, primary_category, COUNT(*) AS paper_count
FROM papers
GROUP BY publication_date, primary_category
ORDER BY publication_date, primary_category
"""
cursor.execute(select_data_query)
data = cursor.fetchall()

# Close the database connection
cursor.close()
conn.close()

# Prepare the data for plotting
dates = []
categories = []
paper_counts = []
for row in data:
    dates.append(row[0])
    categories.append(row[1])
    paper_counts.append(row[2])

# Create a Dash application
app = dash.Dash(__name__)

# Define the layout of the application
app.layout = html.Div(
    children=[
        html.H1("Papers Published in Each Category Each Day"),
        dcc.Graph(
            figure=px.line(
                x=dates,
                y=paper_counts,
                color=categories,
                labels={"x": "Date", "y": "Paper Count", "color": "Category"},
                title="Papers Published in Each Category Each Day",
            ),
        ),
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
