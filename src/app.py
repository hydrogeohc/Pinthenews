"""
Pinthenews - Interactive News Location Analysis
Main Streamlit application with AI-powered location extraction and mapping
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import json
import os
from datetime import datetime
from typing import List, Dict
import requests
from bs4 import BeautifulSoup
import uuid

# Import custom modules
from agents.location_agents import NewsLocationMappingCrew, LocationData
try:
    from src.mcp_integration import MCPNewsLocationClient
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    MCPNewsLocationClient = None

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Pinthenews",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced keep-alive and connection settings for no timeout
if 'keep_alive' not in st.session_state:
    st.session_state.keep_alive = True

# Configure longer timeouts for better connectivity
import socket
socket.setdefaulttimeout(60)  # 60 second timeout for socket operations

# ============================================================================
# STYLING AND CSS
# ============================================================================

st.markdown("""
<style>
    /* Main container styling */
    .main-container {
        display: flex;
        height: 100vh;
        gap: 1rem;
    }
    
    /* Map panel styling */
    .map-panel {
        flex: 1.2;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 1rem;
        overflow: hidden;
    }
    
    /* Chat panel styling */
    .chat-panel {
        flex: 0.8;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 1rem;
        display: flex;
        flex-direction: column;
        max-height: 100vh;
    }
    
    /* Header styling */
    .app-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Chat messages styling */
    .chat-message {
        margin: 0.5rem 0;
        padding: 0.75rem;
        border-radius: 8px;
        max-width: 85%;
    }
    
    .user-message {
        background: #e3f2fd;
        color: #1565c0;
        margin-left: auto;
        text-align: right;
    }
    
    .assistant-message {
        background: #f3e5f5;
        color: #4a148c;
        margin-right: auto;
    }
    
    /* Chat input styling */
    .chat-input {
        position: sticky;
        bottom: 0;
        background: white;
        padding: 1rem;
        border-top: 1px solid #e0e0e0;
        margin-top: auto;
    }
    
    /* Location card styling */
    .location-card {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .location-card:hover {
        background: #e9ecef;
        border-color: #667eea;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Status indicators */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        margin: 0.25rem;
    }
    
    .status-success {
        background: #d4edda;
        color: #155724;
    }
    
    .status-processing {
        background: #fff3cd;
        color: #856404;
    }
    
    .status-error {
        background: #f8d7da;
        color: #721c24;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-container {
            flex-direction: column;
            height: auto;
        }
        
        .map-panel, .chat-panel {
            flex: none;
            height: 50vh;
        }
    }
    
    /* Custom scrollbar */
    .chat-messages::-webkit-scrollbar {
        width: 4px;
    }
    
    .chat-messages::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    .chat-messages::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 10px;
    }
    
    .chat-messages::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def initialize_session_state():
    """Initialize all session state variables"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [{
            'role': 'assistant',
            'content': """👋 Welcome to Pinthenews! I'm your AI assistant for location analysis and news interpretation.

**What I can help you with:**
• 🔍 **Analyze URLs** - Extract and map locations from news articles
• 📝 **Analyze Text** - Find locations in any text you provide
• 📄 **Summarize Text** - Get concise summaries of articles or documents
• 💬 **Answer Questions** - Ask me about locations, patterns, or events

**How to get started:**
1. Choose an input type from the dropdown below
2. Provide a news article URL or paste some text
3. Watch as I analyze and map the locations for you!
4. Ask me questions about what I find

Ready to explore? Let's start mapping the news! 🗺️""",
            'timestamp': datetime.now().isoformat()
        }]
    
    if 'current_locations' not in st.session_state:
        st.session_state.current_locations = []
    if 'map_center' not in st.session_state:
        st.session_state.map_center = [39.8283, -98.5795]  # Center of USA
    if 'processing_status' not in st.session_state:
        st.session_state.processing_status = "ready"
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

# Initialize session state
initialize_session_state()

# ============================================================================
# SYSTEM INITIALIZATION
# ============================================================================

@st.cache_resource
def initialize_systems():
    """Initialize and cache the AI systems"""
    try:
        crew_system = NewsLocationMappingCrew()
        mcp_client = MCPNewsLocationClient() if MCP_AVAILABLE else None
        return crew_system, mcp_client, True
    except Exception as e:
        st.error(f"Failed to initialize systems: {str(e)}")
        return None, None, False

# ============================================================================
# CORE CLASSES
# ============================================================================

class NewsLocationChatbot:
    """Enhanced chatbot for news location analysis"""
    
    def __init__(self, crew_system, mcp_client):
        self.crew_system = crew_system
        self.mcp_client = mcp_client
        
    def _location_to_dict(self, location: LocationData) -> Dict:
        """Convert LocationData to dictionary"""
        return {
            'name': location.name,
            'type': location.type,
            'confidence': location.confidence,
            'context': location.context,
            'latitude': location.latitude,
            'longitude': location.longitude,
            'full_address': location.full_address,
            'event_summary': location.event_summary
        }
    
    def extract_article_from_url(self, url: str) -> str:
        """Extract article content from URL with improved error handling"""
        try:
            # Validate URL format
            if not url.strip():
                return "Error: Empty URL provided"
            
            if not (url.startswith('http://') or url.startswith('https://')):
                url = 'https://' + url
            
            # Check for common invalid URLs
            invalid_patterns = ['localhost', '127.0.0.1', 'example.com', 'test.com']
            if any(pattern in url.lower() for pattern in invalid_patterns):
                return f"Error: Invalid URL pattern detected: {url}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            response = requests.get(url, headers=headers, timeout=60)
            response.raise_for_status()
            
            # Check content type
            content_type = response.headers.get('content-type', '').lower()
            if 'text/html' not in content_type:
                return f"Error: URL does not contain HTML content (content-type: {content_type})"
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'iframe', 'form', 'button']):
                element.decompose()
            
            # Try multiple strategies to extract main content
            content = ""
            
            # Strategy 1: Look for article tags
            article_tags = soup.find_all(['article'])
            if article_tags:
                content = article_tags[0].get_text()
            
            # Strategy 2: Look for common content classes
            elif soup.find('div', class_=lambda x: x and any(keyword in str(x).lower() for keyword in ['content', 'article', 'story', 'post', 'entry'])):
                content_div = soup.find('div', class_=lambda x: x and any(keyword in str(x).lower() for keyword in ['content', 'article', 'story', 'post', 'entry']))
                content = content_div.get_text()
            
            # Strategy 3: Look for main tags
            elif soup.find('main'):
                content = soup.find('main').get_text()
            
            # Strategy 4: Look for the largest text block
            else:
                all_divs = soup.find_all('div')
                if all_divs:
                    largest_div = max(all_divs, key=lambda div: len(div.get_text()))
                    content = largest_div.get_text()
                else:
                    content = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in content.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            clean_content = '\n'.join(chunk for chunk in chunks if chunk and len(chunk) > 10)
            
            # Additional validation
            if len(clean_content.strip()) < 50:
                return "Error: Extracted content is too short (less than 50 characters). This may not be a valid news article."
            
            # Check for common error pages
            error_indicators = ['404 not found', 'page not found', 'access denied', 'forbidden']
            if any(indicator in clean_content.lower() for indicator in error_indicators):
                return "Error: The URL appears to lead to an error page or inaccessible content."
            
            return clean_content[:5000]  # Increased limit to 5000 characters
            
        except requests.exceptions.Timeout:
            # Retry with longer timeout
            try:
                response = requests.get(url, headers=headers, timeout=120)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                content = soup.get_text()
                return content[:5000] if content else "Error: No content found after retry"
            except:
                return "Error: Request timed out even after retry. The website may be slow or unresponsive."
        except requests.exceptions.ConnectionError:
            return "Error: Could not connect to the website. Please check the URL and your internet connection."
        except requests.exceptions.HTTPError as e:
            return f"Error: HTTP error occurred: {e.response.status_code} - {e.response.reason}"
        except requests.exceptions.RequestException as e:
            return f"Error: Request failed: {str(e)}"
        except Exception as e:
            return f"Error extracting article: {str(e)}"

# ============================================================================
# MAPPING FUNCTIONS
# ============================================================================

def create_interactive_map(locations: List[Dict]) -> folium.Map:
    """Create interactive Folium map"""
    if not locations:
        # Default map centered on USA
        m = folium.Map(
            location=st.session_state.map_center,
            zoom_start=4,
            tiles='OpenStreetMap'
        )
        return m
    
    # Filter valid locations
    valid_locations = [loc for loc in locations if loc.get('latitude') and loc.get('longitude')]
    
    if not valid_locations:
        m = folium.Map(
            location=st.session_state.map_center,
            zoom_start=4,
            tiles='OpenStreetMap'
        )
        return m
    
    # Calculate center
    center_lat = sum(loc['latitude'] for loc in valid_locations) / len(valid_locations)
    center_lon = sum(loc['longitude'] for loc in valid_locations) / len(valid_locations)
    
    # Update session state
    st.session_state.map_center = [center_lat, center_lon]
    
    # Create map
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=8,
        tiles='OpenStreetMap'
    )
    
    # Color mapping
    color_map = {
        'city': 'blue',
        'state': 'green', 
        'country': 'red',
        'landmark': 'purple',
        'region': 'orange',
        'neighborhood': 'darkblue',
        'building': 'pink',
        'venue': 'gray'
    }
    
    # Add markers
    for loc in valid_locations:
        color = color_map.get(loc['type'], 'gray')
        
        # Create popup content
        popup_html = f"""
        <div style="width: 250px; font-family: Arial, sans-serif;">
            <h4 style="margin: 0 0 10px 0; color: #333;">{loc['name']}</h4>
            <p><strong>Type:</strong> {loc['type'].title()}</p>
            <p><strong>Confidence:</strong> {loc['confidence'].title()}</p>
            {f"<p><strong>Address:</strong> {loc['full_address']}</p>" if loc.get('full_address') else ""}
            <hr style="margin: 10px 0;">
            <p><strong>Events:</strong></p>
            <p style="font-size: 0.9em; color: #666;">{loc.get('event_summary', 'No summary available')}</p>
        </div>
        """
        
        folium.Marker(
            [loc['latitude'], loc['longitude']],
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"{loc['name']} ({loc['type']})",
            icon=folium.Icon(color=color, icon='info-sign')
        ).add_to(m)
    
    return m

# ============================================================================
# UI COMPONENTS
# ============================================================================

def render_chat_interface():
    """Render the chat interface"""
    # Header with clear button
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### 🤖 Pinthenews AI Assistant")
    with col2:
        if st.button("🗑️ Clear Chat", key="clear_chat"):
            st.session_state.chat_history = [
                {
                    'role': 'assistant',
                    'content': """👋 Chat cleared! I'm ready to help you analyze locations and news articles.

What would you like to explore today?""",
                    'timestamp': datetime.now().isoformat()
                }
            ]
            st.session_state.current_locations = []
            st.rerun()
    
    # Chat history container
    chat_container = st.container()
    
    with chat_container:
        # Display chat history
        for i, message in enumerate(st.session_state.chat_history):
            if message['role'] == 'user':
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>You:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>Assistant:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    st.markdown("---")
    
    # Input options
    input_type = st.selectbox(
        "What would you like to do?",
        ["💬 Ask Question", "📰 Analyze URL", "📝 Analyze Text", "📄 Summarize Text"],
        key="input_type"
    )
    
    if input_type == "💬 Ask Question":
        # Show example questions
        st.markdown("**💡 Example questions:**")
        example_questions = [
            "What locations were mentioned in the article?",
            "Which areas have the highest concentration of events?",
            "Are there any patterns in the geographic distribution?",
            "What's the significance of these locations?",
            "How are these locations connected to current events?"
        ]
        
        # Create buttons for example questions
        cols = st.columns(2)
        for i, example in enumerate(example_questions):
            with cols[i % 2]:
                if st.button(f"💡 {example}", key=f"example_{i}"):
                    handle_user_question(example)
        
        st.markdown("---")
        
        user_question = st.text_input(
            "Or ask your own question:",
            placeholder="Type your question about locations, events, or analysis..."
        )
        
        if st.button("💬 Ask", key="ask_btn"):
            if user_question:
                handle_user_question(user_question)
    
    elif input_type == "📰 Analyze URL":
        url = st.text_input("Enter news article URL:", placeholder="https://example.com/news-article")
        
        if st.button("🔍 Analyze URL", key="analyze_url_btn"):
            if url:
                handle_url_analysis(url)
    
    elif input_type == "📝 Analyze Text":
        article_text = st.text_area(
            "Paste article text:",
            placeholder="Enter or paste the news article text here...",
            height=150
        )
        
        if st.button("🔍 Analyze Text", key="analyze_text_btn"):
            if article_text:
                handle_text_analysis(article_text)
    
    elif input_type == "📄 Summarize Text":
        text_to_summarize = st.text_area(
            "Paste text to summarize:",
            placeholder="Enter any text you'd like me to summarize...",
            height=150
        )
        
        if st.button("📋 Summarize", key="summarize_btn"):
            if text_to_summarize:
                handle_text_summarization(text_to_summarize)

# ============================================================================
# EVENT HANDLERS
# ============================================================================

def handle_user_question(question: str):
    """Handle user questions about current locations"""
    # Add user message to history
    st.session_state.chat_history.append({
        'role': 'user',
        'content': question,
        'timestamp': datetime.now().isoformat()
    })
    
    # Process question
    try:
        if not st.session_state.current_locations:
            response = """I don't have any locations to analyze yet. Please first analyze a news article by providing a URL or text.

**Try these options:**
• 📰 **Analyze URL** - Paste a news article link
• 📝 **Analyze Text** - Copy and paste article text
• 📄 **Summarize Text** - Get a summary of any content

Once I find locations, I can answer questions like:
• "What locations were mentioned?"
• "Which areas are most significant?"
• "Are there any geographic patterns?"
• "What events happened in each location?"

Ready to help you explore the news! 🗺️"""
        else:
            # Generate response based on current locations
            response = generate_contextual_response(question, st.session_state.current_locations)
        
        # Add assistant response
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        error_msg = f"Sorry, I encountered an error while processing your question: {str(e)}"
        if "API" in str(e) or "key" in str(e).lower():
            error_msg += "\n\n💡 This might be an API configuration issue. Please check your ANTHROPIC_API_KEY in the .env file."
        
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': error_msg,
            'timestamp': datetime.now().isoformat()
        })
    
    st.rerun()

def handle_url_analysis(url: str):
    """Handle URL analysis"""
    # Add user message
    st.session_state.chat_history.append({
        'role': 'user',
        'content': f"🔍 Analyzing URL: {url}",
        'timestamp': datetime.now().isoformat()
    })
    
    # Update processing status
    st.session_state.processing_status = "processing"
    
    try:
        # Extract article content
        crew_system, mcp_client, _ = initialize_systems()
        chatbot = NewsLocationChatbot(crew_system, mcp_client)
        
        article_text = chatbot.extract_article_from_url(url)
        
        if article_text.startswith("Error"):
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': f"❌ {article_text}",
                'timestamp': datetime.now().isoformat()
            })
        else:
            # Process locations
            locations = process_article_sync(article_text)
            
            if locations:
                # Update current locations
                st.session_state.current_locations = locations
                
                # Generate response
                response = f"✅ Successfully analyzed the article! Found {len(locations)} locations:\n\n"
                for loc in locations[:5]:  # Show first 5
                    response += f"• **{loc['name']}** ({loc['type']}) - {loc['confidence']} confidence\n"
                
                if len(locations) > 5:
                    response += f"• ... and {len(locations) - 5} more locations\n"
                
                response += f"\nThe map has been updated with all {len(locations)} locations. Click on markers for detailed information!"
                
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': response,
                    'timestamp': datetime.now().isoformat()
                })
            else:
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': "❌ No locations found in the article. Please try a different article.",
                    'timestamp': datetime.now().isoformat()
                })
        
    except Exception as e:
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': f"❌ Error processing URL: {str(e)}",
            'timestamp': datetime.now().isoformat()
        })
    
    st.session_state.processing_status = "ready"
    st.rerun()

def handle_text_analysis(text: str):
    """Handle text analysis"""
    # Add user message
    st.session_state.chat_history.append({
        'role': 'user',
        'content': f"📝 Analyzing article text... ({len(text)} characters)",
        'timestamp': datetime.now().isoformat()
    })
    
    # Update processing status
    st.session_state.processing_status = "processing"
    
    try:
        # Process locations
        locations = process_article_sync(text)
        
        if locations:
            # Update current locations
            st.session_state.current_locations = locations
            
            # Generate response
            response = f"✅ Successfully analyzed the article! Found {len(locations)} locations:\n\n"
            for loc in locations[:5]:  # Show first 5
                response += f"• **{loc['name']}** ({loc['type']}) - {loc['confidence']} confidence\n"
            
            if len(locations) > 5:
                response += f"• ... and {len(locations) - 5} more locations\n"
            
            response += f"\nThe map has been updated with all {len(locations)} locations. Click on markers for detailed information!"
            
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': response,
                'timestamp': datetime.now().isoformat()
            })
        else:
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': "❌ No locations found in the article. Please try a different article.",
                'timestamp': datetime.now().isoformat()
            })
        
    except Exception as e:
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': f"❌ Error processing text: {str(e)}",
            'timestamp': datetime.now().isoformat()
        })
    
    st.session_state.processing_status = "ready"
    st.rerun()

def handle_text_summarization(text: str):
    """Handle text summarization"""
    # Add user message
    st.session_state.chat_history.append({
        'role': 'user',
        'content': f"📄 Summarizing text... ({len(text)} characters)",
        'timestamp': datetime.now().isoformat()
    })
    
    # Update processing status
    st.session_state.processing_status = "processing"
    
    try:
        # Generate summary using Claude
        summary = generate_text_summary(text)
        
        # Add assistant response
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': f"📋 **Summary:**\n\n{summary}",
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': f"❌ Error generating summary: {str(e)}",
            'timestamp': datetime.now().isoformat()
        })
    
    st.session_state.processing_status = "ready"
    st.rerun()

def generate_text_summary(text: str) -> str:
    """Generate text summary using Claude AI"""
    try:
        from anthropic import Anthropic
        
        client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=800,
            timeout=120,  # 2 minute timeout
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    Please provide a comprehensive summary of the following text. 
                    Focus on the key points, main events, and important details.
                    Make it concise but informative:

                    {text}
                    """
                }
            ]
        )
        
        return response.content[0].text
        
    except Exception as e:
        return f"Error generating summary: {str(e)}"

# ============================================================================
# PROCESSING FUNCTIONS
# ============================================================================

def process_article_sync(article_text: str) -> List[Dict]:
    """Process article synchronously with improved error handling"""
    try:
        # Input validation
        if not article_text or not article_text.strip():
            return []
        
        # Check for minimum content length
        if len(article_text.strip()) < 10:
            st.warning("⚠️ Text is too short for meaningful location analysis.")
            return []
        
        # Check for very long text and truncate if necessary
        if len(article_text) > 10000:
            article_text = article_text[:10000]
            st.info("ℹ️ Text was truncated to 10,000 characters for processing.")
        
        crew_system, mcp_client, _ = initialize_systems()
        
        # Use CrewAI system for processing
        locations_data = crew_system.extract_and_process_locations(article_text)
        
        # Convert to dictionary format with validation
        locations = []
        seen_locations = set()  # To avoid duplicates
        
        for loc in locations_data:
            # Skip if this is a duplicate location
            location_key = f"{loc.name.lower()}_{loc.type}"
            if location_key in seen_locations:
                continue
            
            # Basic validation of location data
            if not loc.name or len(loc.name.strip()) < 2:
                continue
            
            # Filter out obvious non-locations
            non_location_words = {
                'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
                'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after',
                'above', 'below', 'between', 'among', 'through', 'during', 'before',
                'after', 'above', 'below', 'up', 'down', 'out', 'off', 'over', 'under',
                'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where',
                'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most',
                'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same',
                'so', 'than', 'too', 'very', 'can', 'will', 'just', 'should', 'now'
            }
            
            if loc.name.lower().strip() in non_location_words:
                continue
            
            # Filter out numbers and dates
            if loc.name.strip().isdigit() or any(char.isdigit() for char in loc.name) and len(loc.name) < 5:
                continue
            
            # Create location dictionary
            location_dict = {
                'name': loc.name.strip(),
                'type': loc.type if loc.type else 'unknown',
                'confidence': loc.confidence if loc.confidence else 'medium',
                'context': loc.context if loc.context else '',
                'latitude': loc.latitude,
                'longitude': loc.longitude,
                'full_address': loc.full_address if loc.full_address else '',
                'event_summary': loc.event_summary if loc.event_summary else ''
            }
            
            locations.append(location_dict)
            seen_locations.add(location_key)
        
        # Sort by confidence and geocoding status
        def sort_key(loc):
            confidence_order = {'high': 3, 'medium': 2, 'low': 1}
            has_coords = 1 if loc.get('latitude') and loc.get('longitude') else 0
            confidence_score = confidence_order.get(loc.get('confidence', 'medium'), 2)
            return (has_coords, confidence_score, loc.get('name', ''))
        
        locations.sort(key=sort_key, reverse=True)
        
        # Limit to reasonable number of locations
        if len(locations) > 50:
            st.info(f"ℹ️ Found {len(locations)} locations. Showing top 50 most relevant.")
            locations = locations[:50]
        
        return locations
        
    except Exception as e:
        error_msg = f"Processing error: {str(e)}"
        st.error(error_msg)
        
        # Provide helpful error messages
        if "API" in str(e) or "key" in str(e).lower():
            st.error("💡 This appears to be an API configuration issue. Please check your ANTHROPIC_API_KEY in the .env file.")
        elif "timeout" in str(e).lower():
            st.error("⏱️ The request timed out. Try with shorter text or check your internet connection.")
        elif "rate limit" in str(e).lower():
            st.error("🚦 API rate limit reached. Please wait a moment before trying again.")
        
        return []

def generate_contextual_response(question: str, locations: List[Dict]) -> str:
    """Generate contextual response based on question and locations"""
    try:
        from anthropic import Anthropic
        
        client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        # Create context from locations
        locations_context = ""
        for loc in locations:
            locations_context += f"- {loc['name']} ({loc['type']}, {loc['confidence']} confidence): {loc.get('event_summary', 'No summary')}\n"
        
        # Enhanced system prompt for better conversation
        system_prompt = """
        You are Pinthenews AI Assistant, a helpful and knowledgeable assistant specializing in location analysis and news interpretation.
        Your role is to provide insightful analysis of locations mentioned in news articles and answer questions about geographic patterns, events, and trends.
        
        Be conversational, informative, and helpful. When analyzing locations, consider:
        - Geographic patterns and clustering
        - Event significance and context
        - Potential relationships between locations
        - Historical or cultural significance
        - Current events and news relevance
        
        Always provide specific, actionable insights when possible.
        """
        
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=700,
            timeout=120,  # 2 minute timeout
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    Based on the following locations extracted from a news article, please answer this question: "{question}"
                    
                    Locations found:
                    {locations_context}
                    
                    Please provide a helpful, detailed, and conversational response. If the question asks for specific analysis, 
                    provide relevant details about the locations, events, patterns, or insights you can identify.
                    """
                }
            ]
        )
        
        return response.content[0].text
        
    except Exception as e:
        return f"I encountered an error while processing your question: {str(e)}"

# ============================================================================
# SIDEBAR COMPONENTS
# ============================================================================

def render_location_sidebar():
    """Render location information sidebar"""
    if st.session_state.current_locations:
        st.sidebar.markdown("### 📍 Current Locations")
        
        # Summary statistics
        total_locations = len(st.session_state.current_locations)
        geocoded_locations = len([loc for loc in st.session_state.current_locations if loc.get('latitude')])
        
        st.sidebar.metric("Total Locations", total_locations)
        st.sidebar.metric("Geocoded", geocoded_locations)
        
        # Location type distribution
        location_types = {}
        for loc in st.session_state.current_locations:
            loc_type = loc['type']
            location_types[loc_type] = location_types.get(loc_type, 0) + 1
        
        st.sidebar.markdown("**Location Types:**")
        for loc_type, count in location_types.items():
            st.sidebar.markdown(f"• {loc_type.title()}: {count}")
        
        # Export options
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📤 Export Data")
        
        if st.sidebar.button("📥 Download JSON"):
            json_data = json.dumps(st.session_state.current_locations, indent=2)
            st.sidebar.download_button(
                label="Download",
                data=json_data,
                file_name=f"locations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application function"""
    # Validate configuration
    if not os.getenv("ANTHROPIC_API_KEY"):
        st.error("⚠️ ANTHROPIC_API_KEY not found. Please set up your .env file.")
        st.stop()
    
    # Initialize AI systems
    crew_system, mcp_client, systems_ready = initialize_systems()
    if not systems_ready:
        st.error("⚠️ Failed to initialize systems. Please check your configuration.")
        st.stop()
    
    # Header
    st.markdown("""
    <div class="app-header">
        <h1>🌍 Pinthenews</h1>
        <p>Interactive Map + AI Assistant for Real-Time Location Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main layout: Two columns
    col1, col2 = st.columns([1.4, 1.0])
    
    with col1:
        # Map panel
        st.markdown("### 🗺️ Interactive Location Map")
        
        # Processing status
        if st.session_state.processing_status == "processing":
            st.info("🔄 Processing article...")
        
        # Create and display map
        map_obj = create_interactive_map(st.session_state.current_locations)
        
        # Display map with interaction
        map_data = st_folium(
            map_obj,
            width=700,
            height=600,
            returned_objects=["last_clicked", "last_object_clicked"]
        )
        
        # Handle map interactions
        if map_data['last_clicked']:
            clicked_lat = map_data['last_clicked']['lat']
            clicked_lng = map_data['last_clicked']['lng']
            
            # Find nearest location
            if st.session_state.current_locations:
                nearest_location = None
                min_distance = float('inf')
                
                for loc in st.session_state.current_locations:
                    if loc.get('latitude') and loc.get('longitude'):
                        distance = ((clicked_lat - loc['latitude']) ** 2 + (clicked_lng - loc['longitude']) ** 2) ** 0.5
                        if distance < min_distance:
                            min_distance = distance
                            nearest_location = loc
                
                if nearest_location and min_distance < 0.1:  # Within reasonable distance
                    st.info(f"📍 Clicked near: **{nearest_location['name']}**")
        
        # Location statistics
        if st.session_state.current_locations:
            st.markdown("### 📊 Quick Statistics")
            
            col1_stats, col2_stats, col3_stats = st.columns(3)
            
            with col1_stats:
                st.metric("Total Locations", len(st.session_state.current_locations))
            
            with col2_stats:
                geocoded = len([loc for loc in st.session_state.current_locations if loc.get('latitude')])
                st.metric("Geocoded", geocoded)
            
            with col3_stats:
                high_confidence = len([loc for loc in st.session_state.current_locations if loc.get('confidence') == 'high'])
                st.metric("High Confidence", high_confidence)
    
    with col2:
        # Chat panel
        render_chat_interface()
    
    # Sidebar for detailed location information
    render_location_sidebar()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: gray;">
        <p>🌍 Pinthenews - Real-time location analysis with AI assistance</p>
        <p>Powered by CrewAI Multi-Agent System + Claude AI</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()