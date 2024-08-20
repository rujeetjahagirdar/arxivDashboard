import urllib.request
import feedparser
import datetime
import psycopg2

# Database connection parameters
db_params = {
    'host': 'localhost',
    'port': '5432',
    'user': 'postgres',
    'password': 'postgres',
    'options': '-c search_path=paper_monitoring'
}

# Base API query URL
base_url = 'http://export.arxiv.org/api/query?'

# Search parameters
search_query = 'cat:cs.*'  # search for papers in the Computer Vision category
max_results = 5000  # retrieve the first 5 results
start=0
# Calculate the time range for the last 5 minutes
current_time = datetime.datetime.now()
start_time = current_time - datetime.timedelta(days=20)
# start_time = datetime.datetime.strptime('2023-04-05T00:00:00','%Y-%m-%dT%H:%M:%S')
# Convert start_time to the format required by the Arxiv API
start_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%S') + 'Z'
query = 'search_query={}&sortBy=submittedDate&start={}&sortOrder=descending&max_results={}&submittedDate:{}/'.format(
    search_query, start, max_results, start_time_str)

# Perform a GET request using the base_url and query
response = urllib.request.urlopen(base_url + query).read()

# Parse the response using feedparser
feed = feedparser.parse(response)

# Connect to the PostgreSQL database
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Run through each entry and save data to the database
for entry in feed.entries:
    arxiv_id = entry.id.split('/abs/')[-1]
    published = entry.published
    title = entry.title
    abstract = entry.summary
    abs_link = None
    pdf_link = None
    journal_ref = None
    comment = None
    primary_category = None
    authors = []
    categories = []
    tags = []
    affiliations = []

    # Get the links to the abs page and pdf for this paper
    for link in entry.links:
        if link.rel == 'alternate':
            abs_link = link.href
        elif link.title == 'pdf':
            pdf_link = link.href

    # The journal reference, comments, and primary_category sections live under the arxiv namespace
    if 'arxiv_journal_ref' in entry:
        journal_ref = entry.arxiv_journal_ref
    if 'arxiv_comment' in entry:
        comment = entry.arxiv_comment
    if 'tags' in entry:
        primary_category = entry.tags[0]['term']
        categories = [tag['term'] for tag in entry.tags]
        tags = [tag['term'] for tag in entry.tags if tag['scheme'] == 'http://arxiv.org/schemas/atom/keywords']

    # Get the authors and affiliations
    if 'authors' in entry:
        for author in entry.authors:
            author_name = author.name
            authors.append(author_name)
            # if author.affiliation:
            #     affiliations.append(author.affiliation)

    # Check if the paper already exists in the database
    select_paper_query = "SELECT id FROM papers WHERE arxiv_id = %s"
    cursor.execute(select_paper_query, (arxiv_id,))
    existing_paper = cursor.fetchone()

    if existing_paper:
        print(f"Skipping insertion for paper with arxiv_id '{arxiv_id}' (already exists in the database)")
        continue

    # Insert paper data into the database
    insert_paper_query = """
    INSERT INTO papers (arxiv_id, published, title, abstract, abs_link, pdf_link, journal_ref, comment, primary_category)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id
    """
    cursor.execute(insert_paper_query, (arxiv_id, published, title, abstract, abs_link, pdf_link, journal_ref, comment,
                                        primary_category))
    paper_id = cursor.fetchone()[0]

    # Insert author data into the database
    for author in authors:
        insert_author_query = "INSERT INTO authors (paper_id, name) VALUES (%s, %s) ON CONFLICT DO NOTHING"
        cursor.execute(insert_author_query, (paper_id, author))

    # Insert category data into the database
    for category in categories:
        insert_category_query = "INSERT INTO categories (paper_id, category) VALUES (%s, %s) ON CONFLICT DO NOTHING"
        cursor.execute(insert_category_query, (paper_id, category))

    # Insert tag data into the database
    for tag in tags:
        insert_tag_query = "INSERT INTO tags (paper_id, tag) VALUES (%s, %s) ON CONFLICT DO NOTHING"
        cursor.execute(insert_tag_query, (paper_id, tag))

    # Insert affiliation data into the database
    # for affiliation in affiliations:
    #     insert_affiliation_query = "INSERT INTO affiliations (paper_id, affiliation) VALUES (%s, %s) ON CONFLICT DO NOTHING"
    #     cursor.execute(insert_affiliation_query, (paper_id, affiliation))

    print(f"Inserted data for paper with arxiv_id '{arxiv_id}' into the database")

# Commit the transaction and close the database connection
conn.commit()
cursor.close()
conn.close()
