
PROMPT_TEMPLATE = """ 
You are an expert in answering questions about a pizza restaurant.
Here are some relevant reviews: {reviews}.
Here is the question to answer: {question}.
"""

UI_SEPARATOR = "\n\n" + "-" * 37 
PROMPT_MESSAGE = "Ask your question (q to quit): "
EXIT_COMMAND = "q"

# Column names for CSV
CSV_COLUMNS = {
    "TITLE": "Title",
    "REVIEW": "Review", 
    "RATING": "Rating",
    "DATE": "Date"
}