
# PROMPT_TEMPLATE = """ 
# You are an expert in answering questions about a pizza restaurant.
# Here are some relevant reviews: {reviews}.
# Here is the question to answer: {question}.
# """

PROMPT_TEMPLATE = """ 
You are an expert assistant for a pizza restaurant review system.
Use the following reviews to answer the user's question.

Relevant Reviews:
{reviews}

User's Question: {question}

Guidelines:
- Base your answer only on the provided reviews
- If the reviews don't contain relevant information, say so
- Be concise but informative
- Reference specific review details when possible

Answer:
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


