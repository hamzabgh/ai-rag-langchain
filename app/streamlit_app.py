"""
Premium Streamlit Interface for Pizza RAG System
"""
import streamlit as st
from streamlit_chat import message
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.vector_store import retriever
from models.llm_chain import invoke_chain
from config import settings
from core import constants


st.set_page_config(
    page_title="🍕 Pizza Review Assistant",
    page_icon="🍕",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Main theme */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FF6B6B 0%, #4ECDC4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    
    .sub-header {
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    /* Chat containers */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        margin: 10px 0;
    }
    
    .assistant-message {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 15px;
        margin: 10px 0;
        border-left: 5px solid #4ECDC4;
    }
    
    /* Sidebar */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2d3436 0%, #000000 100%);
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #FF6B6B 0%, #4ECDC4 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    
    /* Cards */
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    /* Metrics */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    
    /* Sample question buttons */
    .sample-question-btn {
        width: 100%;
        text-align: left;
        margin: 5px 0;
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        background: white;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .sample-question-btn:hover {
        background: #f0f2f6;
        transform: translateX(5px);
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'reviews_retrieved' not in st.session_state:
        st.session_state.reviews_retrieved = []
    
    if 'total_questions' not in st.session_state:
        st.session_state.total_questions = 0
    
    if 'start_time' not in st.session_state:
        st.session_state.start_time = datetime.now()
    
    if 'sample_question_clicked' not in st.session_state:
        st.session_state.sample_question_clicked = None


def display_welcome():
    """Display welcome section."""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<h1 class="main-header">🍕 Pizza Review Assistant</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">AI-powered insights from restaurant reviews. Ask anything about pizza places!</p>', unsafe_allow_html=True)
        
        # Stats cards
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🍽️</h3>
                <h2>{len(st.session_state.reviews_retrieved)}</h2>
                <p>Reviews Analyzed</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_b:
            st.markdown(f"""
            <div class="metric-card">
                <h3>💬</h3>
                <h2>{st.session_state.total_questions}</h2>
                <p>Questions Asked</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_c:
            duration = datetime.now() - st.session_state.start_time
            mins = duration.seconds // 60
            st.markdown(f"""
            <div class="metric-card">
                <h3>⏱️</h3>
                <h2>{mins}</h2>
                <p>Minutes Active</p>
            </div>
            """, unsafe_allow_html=True)


def display_sidebar():
    """Display sidebar with controls and info."""
    with st.sidebar:
        st.markdown("## ⚙️ Settings")
        
        # Model selection
        st.markdown("### Model Configuration")
        model_option = st.selectbox(
            "Select LLM Model",
            ["phi", "llama2", "mistral", "neural-chat"],
            index=0,
            key="model_select"
        )
        
        # Search parameters
        st.markdown("### Search Parameters")
        k_value = st.slider(
            "Number of reviews to retrieve",
            min_value=1,
            max_value=10,
            value=5,
            key="k_value_slider"
        )
        
        # Review filters
        st.markdown("### Filter Reviews")
        min_rating = st.slider(
            "Minimum Rating",
            min_value=1,
            max_value=5,
            value=3,
            key="min_rating_slider"
        )
        
        # Sample questions - using a different approach
        st.markdown("### 💡 Sample Questions")
        st.markdown("Click any question below to use it:")
        
        sample_questions = [
            "What's the best pizza place in town?",
            "Which restaurant has the best crust?",
            "Where can I find vegetarian pizza options?",
            "Which place has the fastest delivery?",
            "What are customers saying about the service?",
            "Which pizza place is most family-friendly?"
        ]
        
        # Create buttons for sample questions
        clicked_question = None
        for i, question in enumerate(sample_questions):
            if st.button(f"💬 {question}", key=f"sample_btn_{i}"):
                clicked_question = question
        
        # Store clicked question in session state
        if clicked_question:
            st.session_state.sample_question_clicked = clicked_question
            st.rerun()
        
        # Clear chat button
        st.markdown("---")
        if st.button("🗑️ Clear Chat History", type="secondary", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.reviews_retrieved = []
            st.session_state.total_questions = 0
            st.rerun()
        
        # System info
        st.markdown("---")
        st.markdown("### ℹ️ System Info")
        st.info(f"""
        **Database**: {len(st.session_state.reviews_retrieved)} reviews loaded
        **Model**: {model_option}
        **Embeddings**: {settings.EMBEDDING_MODEL}
        **Version**: 1.0.0
        """)
        
        # Debug info (optional)
        with st.expander("Debug Info"):
            st.write(f"Session state keys: {list(st.session_state.keys())}")


def display_chat_interface():
    """Display main chat interface."""
    st.markdown("## 💬 Chat with Pizza Assistant")
    
    chat_container = st.container()
    
    with chat_container:
        if st.session_state.chat_history:
            for i, chat in enumerate(st.session_state.chat_history):
                if chat["role"] == "user":
                    message(
                        chat["message"],
                        is_user=True,
                        key=f"user_{i}",
                        avatar_style="identicon"
                    )
                else:
                    # Create a nice assistant message with metadata
                    with st.expander(f"🤖 Assistant's Response", expanded=True):
                        st.markdown(f"**Answer:** {chat['message']}")
                        
                        if chat.get('reviews'):
                            st.markdown("**📊 Sources Used:**")
                            for j, review in enumerate(chat['reviews']):
                                rating = review.metadata.get('rating', 'N/A')
                                date = review.metadata.get('date', 'N/A')
                                with st.container():
                                    st.markdown(f"""
                                    <div style="background:#f0f2f6;padding:10px;border-radius:10px;margin:5px 0;">
                                    <strong>Source {j+1}:</strong> ⭐ Rating: {rating}/5 | 📅 Date: {date}
                                    <br>
                                    {review.page_content[:200]}...
                                    </div>
                                    """, unsafe_allow_html=True)
        else:
            # Welcome message when no chat history
            st.markdown("""
            <div class="card">
                <h3>👋 Welcome to Pizza Review Assistant!</h3>
                <p>I can help you find information about pizza restaurants based on customer reviews.</p>
                <p>Try asking questions like:</p>
                <ul>
                    <li>"What's the best pizza place in town?"</li>
                    <li>"Which restaurant has the best crust?"</li>
                    <li>"Where can I find vegetarian options?"</li>
                </ul>
                <p>Or click on the sample questions in the sidebar! 🍕</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Input area
    st.markdown("---")
    
    # Check if a sample question was clicked
    default_value = ""
    if st.session_state.sample_question_clicked:
        default_value = st.session_state.sample_question_clicked
        # Clear it after use
        st.session_state.sample_question_clicked = None
    
    col1, col2 = st.columns([6, 1])
    
    with col1:
        user_input = st.text_input(
            "Type your question about pizza restaurants:",
            value=default_value,
            placeholder="E.g., 'What's the best pizza place for families?'",
            key="user_input",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("🚀 Ask", use_container_width=True, type="primary")
    
    # Process input
    if send_button and user_input:
        process_user_input(user_input)


def process_user_input(question):
    """Process user question and generate response."""
    st.session_state.chat_history.append({
        "role": "user",
        "message": question,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })
    
    with st.spinner("🔍 Searching through reviews..."):
        # Retrieve relevant reviews
        reviews = retriever.invoke(question)
        st.session_state.reviews_retrieved.extend(reviews)
        
        # Generate response
        response = invoke_chain(reviews=reviews, question=question)
    
    # Add assistant response to history
    st.session_state.chat_history.append({
        "role": "assistant",
        "message": response,
        "reviews": reviews[:3],  # Show top 3 sources
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })
    
    st.session_state.total_questions += 1
    st.rerun()


def display_analytics():
    """Display analytics dashboard."""
    st.markdown("---")
    st.markdown("## 📊 Analytics Dashboard")
    
    if st.session_state.reviews_retrieved:
        reviews_data = []
        for review in st.session_state.reviews_retrieved:
            reviews_data.append({
                "rating": review.metadata.get('rating', 0),
                "content": review.page_content[:100] + "..."
            })
        
        df = pd.DataFrame(reviews_data)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_rating = df['rating'].mean() if not df.empty else 0
            st.metric("Average Rating", f"{avg_rating:.1f} ⭐")
        
        with col2:
            st.metric("Total Reviews", len(df))
        
        with col3:
            positive = len(df[df['rating'] >= 4]) if not df.empty else 0
            st.metric("Positive Reviews", positive)
        
        with col4:
            st.metric("Response Time", "2-3s")
        
        # Rating distribution chart
        st.markdown("### 📈 Rating Distribution")
        if not df.empty and 'rating' in df.columns:
            rating_counts = df['rating'].value_counts().sort_index()
            
            fig = go.Figure(data=[
                go.Bar(
                    x=[str(x) for x in rating_counts.index],
                    y=rating_counts.values,
                    marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'],
                    text=rating_counts.values,
                    textposition='auto',
                )
            ])
            
            fig.update_layout(
                title="Review Ratings Distribution",
                xaxis_title="Rating",
                yaxis_title="Count",
                template="plotly_white",
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### 💭 Conversation Insights")
    if st.session_state.chat_history:
        user_questions = [chat['message'] for chat in st.session_state.chat_history 
                         if chat['role'] == 'user']
        
        if user_questions:
            st.markdown(f"""
            <div class="card">
                <h4>Recent Questions:</h4>
                <ul>
                    {"".join([f"<li>❓ {q}</li>" for q in user_questions[-3:]])}
                </ul>
            </div>
            """, unsafe_allow_html=True)


def display_footer():
    """Display footer."""
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align:center;color:#666;padding:2rem;">
            <p>🍕 <strong>Pizza Review Assistant v1.0</strong></p>
            <p>Powered by Ollama LLM & Chroma Vector DB</p>
            <p>For the love of pizza! 🍕</p>
        </div>
        """, unsafe_allow_html=True)


def main():
    """Main app function."""
    initialize_session_state()
    
    display_welcome()
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        display_chat_interface()
        display_analytics()
    
    with col2:
        display_sidebar()
    
    display_footer()


if __name__ == "__main__":
    main()