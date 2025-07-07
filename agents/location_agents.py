"""
Multi-Agent System for News Location Extraction and Mapping
Using CrewAI for hierarchical agent coordination
"""

from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from anthropic import Anthropic
from openai import OpenAI
from geopy.geocoders import Nominatim
import requests
from bs4 import BeautifulSoup
import json
import os
from typing import List, Dict, Any
import folium
import time
from dataclasses import dataclass


@dataclass
class LocationData:
    """Data class for location information"""
    name: str
    type: str
    confidence: str
    context: str
    latitude: float = None
    longitude: float = None
    full_address: str = None
    event_summary: str = None


class ArticleExtractorTool(BaseTool):
    """Tool for extracting article content from URLs"""
    
    name: str = "article_extractor"
    description: str = "Extracts clean article content from news URLs"
    
    def _run(self, url: str) -> str:
        """Extract article content from URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                element.decompose()
            
            # Try multiple strategies to find article content
            content = ""
            
            # Strategy 1: Look for article tags
            article_tags = soup.find_all(['article'])
            if article_tags:
                content = article_tags[0].get_text()
            
            # Strategy 2: Look for content divs
            elif soup.find('div', class_=lambda x: x and any(keyword in str(x).lower() for keyword in ['content', 'article', 'story', 'post-content'])):
                content_div = soup.find('div', class_=lambda x: x and any(keyword in str(x).lower() for keyword in ['content', 'article', 'story', 'post-content']))
                content = content_div.get_text()
            
            # Strategy 3: Look for main content area
            elif soup.find('main'):
                content = soup.find('main').get_text()
            
            # Strategy 4: Use the whole body
            else:
                content = soup.get_text()
            
            # Clean up the text
            lines = (line.strip() for line in content.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            clean_content = '\n'.join(chunk for chunk in chunks if chunk and len(chunk) > 10)
            
            return clean_content[:5000]  # Limit to first 5000 characters
            
        except Exception as e:
            return f"Error extracting content: {str(e)}"


class LocationExtractionTool(BaseTool):
    """Tool for extracting locations using Claude"""
    
    name: str = "location_extractor"
    description: str = "Extracts geographical locations from text using Claude AI"
    
    def _run(self, text: str) -> str:
        """Extract locations from text using Claude"""
        try:
            client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1500,
                messages=[
                    {
                        "role": "user",
                        "content": f"""
                        You are an expert geographical location extractor. Analyze the following news article text and extract ALL geographical locations mentioned.
                        
                        For each location, provide:
                        1. The exact location name as mentioned in the text
                        2. The type of location (city, state, country, landmark, region, neighborhood, etc.)
                        3. Your confidence level (high, medium, low)
                        4. The context/sentence where this location appears
                        
                        Return the results as a JSON array with this structure:
                        [
                            {{
                                "location": "exact location name",
                                "type": "city/state/country/landmark/region/neighborhood",
                                "confidence": "high/medium/low",
                                "context": "the sentence or phrase where this location appears"
                            }}
                        ]
                        
                        Be thorough - include:
                        - Cities, towns, villages
                        - States, provinces, regions
                        - Countries
                        - Landmarks, buildings, venues
                        - Neighborhoods, districts
                        - Geographical features (rivers, mountains, etc.)
                        
                        Article text:
                        {text}
                        
                        Return only valid JSON, no other text.
                        """
                    }
                ]
            )
            
            content = response.content[0].text.strip()
            
            # Clean up response to ensure valid JSON
            if content.startswith('```json'):
                content = content[7:-3]
            elif content.startswith('```'):
                content = content[3:-3]
            
            return content
            
        except Exception as e:
            return f"Error extracting locations: {str(e)}"


class GeocodingTool(BaseTool):
    """Tool for converting location names to coordinates"""
    
    name: str = "geocoding_tool"
    description: str = "Converts location names to latitude/longitude coordinates"
    
    def _run(self, location_name: str) -> str:
        """Geocode a location name to coordinates"""
        try:
            # Add a small delay to respect rate limits
            time.sleep(1)
            
            geolocator = Nominatim(user_agent="news_location_mapper_v1.0")
            result = geolocator.geocode(location_name)
            
            if result:
                return json.dumps({
                    "location": location_name,
                    "latitude": result.latitude,
                    "longitude": result.longitude,
                    "full_address": result.address,
                    "success": True
                })
            else:
                return json.dumps({
                    "location": location_name,
                    "error": "Location not found",
                    "success": False
                })
                
        except Exception as e:
            return json.dumps({
                "location": location_name,
                "error": str(e),
                "success": False
            })


class EventSummarizationTool(BaseTool):
    """Tool for generating event summaries for locations"""
    
    name: str = "event_summarizer"
    description: str = "Generates concise event summaries for specific locations"
    
    def _run(self, location: str, context: str, full_article: str) -> str:
        """Generate event summary for a specific location"""
        try:
            client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=150,
                messages=[
                    {
                        "role": "user",
                        "content": f"""
                        Based on this news article, provide a brief 1-2 sentence summary of what happened at or involves "{location}".
                        
                        Context where location appears: {context}
                        
                        Full article (first 2000 chars):
                        {full_article[:2000]}
                        
                        Keep the summary:
                        - Very concise (1-2 sentences max)
                        - Factual and specific
                        - Focused on events at this location
                        - Easy to understand
                        
                        If no specific event is mentioned for this location, describe its role in the story.
                        """
                    }
                ]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            return f"Events at {location}: {context[:100]}..."


class NewsLocationMappingCrew:
    """CrewAI-based multi-agent system for news location mapping"""
    
    def __init__(self):
        self.setup_tools()
        self.setup_agents()
    
    def setup_tools(self):
        """Initialize all tools"""
        self.article_extractor = ArticleExtractorTool()
        self.location_extractor = LocationExtractionTool()
        self.geocoding_tool = GeocodingTool()
        self.event_summarizer = EventSummarizationTool()
    
    def setup_agents(self):
        """Setup CrewAI agents"""
        
        # Content Extraction Agent
        self.content_agent = Agent(
            role="Senior Content Analyst",
            goal="Extract and clean article content from URLs and text inputs with high accuracy",
            backstory="""You are a seasoned digital content analyst with 10 years of experience in 
            extracting clean, readable content from various news sources. You excel at identifying 
            the main article content while filtering out advertisements, navigation menus, and other 
            non-essential elements.""",
            tools=[self.article_extractor],
            verbose=True,
            allow_delegation=False
        )
        
        # Location Extraction Agent
        self.location_agent = Agent(
            role="Geographic Intelligence Specialist",
            goal="Identify and extract all geographical locations from news content with precision",
            backstory="""You are a geographic intelligence expert with extensive knowledge of world 
            geography, political boundaries, and location naming conventions. You have a keen eye for 
            identifying not just obvious locations like cities and countries, but also landmarks, 
            neighborhoods, and geographical features mentioned in news articles.""",
            tools=[self.location_extractor],
            verbose=True,
            allow_delegation=False
        )
        
        # Geocoding Agent
        self.geocoding_agent = Agent(
            role="Cartographic Coordinator",
            goal="Convert location names to precise geographical coordinates",
            backstory="""You are a professional cartographer and GIS specialist with expertise in 
            global coordinate systems and geocoding services. You ensure that every location is 
            accurately mapped to its correct latitude and longitude coordinates.""",
            tools=[self.geocoding_tool],
            verbose=True,
            allow_delegation=False
        )
        
        # Event Analysis Agent
        self.event_agent = Agent(
            role="News Event Analyst",
            goal="Analyze and summarize events that occurred at specific locations",
            backstory="""You are an experienced news analyst and journalist with a talent for 
            distilling complex news stories into clear, concise summaries. You focus on the key 
            events, their significance, and their connection to specific geographical locations.""",
            tools=[self.event_summarizer],
            verbose=True,
            allow_delegation=False
        )
        
        # Visualization Coordinator
        self.viz_agent = Agent(
            role="Data Visualization Director",
            goal="Coordinate the creation of interactive maps and visualizations",
            backstory="""You are a senior data visualization specialist who excels at creating 
            compelling, interactive maps that tell stories through geographical data. You ensure 
            that complex geographical information is presented in an accessible and engaging way.""",
            verbose=True,
            allow_delegation=False
        )
    
    def create_tasks(self, input_data: Dict[str, Any]) -> List[Task]:
        """Create tasks for the crew"""
        
        tasks = []
        
        # Task 1: Content Extraction
        content_task = Task(
            description=f"""
            Extract clean article content from the provided input:
            Input type: {input_data.get('type', 'text')}
            Content: {input_data.get('content', '')[:200]}...
            
            If input type is 'url', extract content from the URL.
            If input type is 'text', clean and prepare the text.
            
            Return clean, readable article content suitable for location extraction.
            """,
            agent=self.content_agent,
            expected_output="Clean article text without ads, navigation, or irrelevant content"
        )
        tasks.append(content_task)
        
        # Task 2: Location Extraction
        location_task = Task(
            description="""
            Analyze the cleaned article content and extract ALL geographical locations mentioned.
            Use the location extraction tool to identify:
            - Cities, towns, villages
            - States, provinces, regions
            - Countries
            - Landmarks, buildings, venues
            - Neighborhoods, districts
            - Geographical features
            
            Return a comprehensive list of locations with their types, confidence levels, and context.
            """,
            agent=self.location_agent,
            expected_output="JSON array of extracted locations with type, confidence, and context",
            dependencies=[content_task]
        )
        tasks.append(location_task)
        
        # Task 3: Geocoding
        geocoding_task = Task(
            description="""
            Convert all extracted location names to precise latitude/longitude coordinates.
            Use the geocoding tool for each location identified in the previous task.
            
            Handle any geocoding failures gracefully and report which locations couldn't be geocoded.
            """,
            agent=self.geocoding_agent,
            expected_output="Geocoded location data with coordinates and addresses",
            dependencies=[location_task]
        )
        tasks.append(geocoding_task)
        
        # Task 4: Event Summarization
        event_task = Task(
            description="""
            For each successfully geocoded location, generate a concise summary of events 
            that occurred at or involve that location based on the article content.
            
            Use the event summarization tool to create 1-2 sentence summaries that will 
            be displayed when users interact with map markers.
            """,
            agent=self.event_agent,
            expected_output="Event summaries for each location",
            dependencies=[geocoding_task]
        )
        tasks.append(event_task)
        
        # Task 5: Visualization Coordination
        viz_task = Task(
            description="""
            Coordinate the final data preparation for map visualization.
            Ensure all location data is properly formatted and ready for interactive mapping.
            
            Provide a summary of the entire process and recommendations for map display.
            """,
            agent=self.viz_agent,
            expected_output="Final location data formatted for visualization with processing summary",
            dependencies=[event_task]
        )
        tasks.append(viz_task)
        
        return tasks
    
    def process_article(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process article through the multi-agent system"""
        
        # Create tasks
        tasks = self.create_tasks(input_data)
        
        # Create crew
        crew = Crew(
            agents=[
                self.content_agent,
                self.location_agent,
                self.geocoding_agent,
                self.event_agent,
                self.viz_agent
            ],
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
        
        # Execute the crew
        try:
            result = crew.kickoff()
            return {
                "success": True,
                "result": result,
                "message": "Processing completed successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Processing failed"
            }
    
    def extract_and_process_locations(self, article_text: str) -> List[LocationData]:
        """Extract and process locations from article text"""
        try:
            # Extract locations
            locations_json = self.location_extractor._run(article_text)
            locations = json.loads(locations_json)
            
            location_data = []
            
            for loc in locations:
                # Geocode the location
                geocode_result = self.geocoding_tool._run(loc['location'])
                geocode_data = json.loads(geocode_result)
                
                if geocode_data.get('success', False):
                    # Generate event summary
                    event_summary = self.event_summarizer._run(
                        loc['location'], 
                        loc['context'], 
                        article_text
                    )
                    
                    # Create LocationData object
                    location_obj = LocationData(
                        name=loc['location'],
                        type=loc['type'],
                        confidence=loc['confidence'],
                        context=loc['context'],
                        latitude=geocode_data['latitude'],
                        longitude=geocode_data['longitude'],
                        full_address=geocode_data['full_address'],
                        event_summary=event_summary
                    )
                    
                    location_data.append(location_obj)
            
            return location_data
            
        except Exception as e:
            print(f"Error processing locations: {e}")
            return []
    
    def create_folium_map(self, locations: List[LocationData]) -> folium.Map:
        """Create a Folium map with location markers"""
        if not locations:
            return None
        
        # Calculate center point
        center_lat = sum(loc.latitude for loc in locations) / len(locations)
        center_lon = sum(loc.longitude for loc in locations) / len(locations)
        
        # Create map
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=8,
            tiles='OpenStreetMap'
        )
        
        # Color mapping for different location types
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
        for loc in locations:
            color = color_map.get(loc.type, 'gray')
            
            # Create popup content
            popup_html = f"""
            <div style="width: 300px;">
                <h4>{loc.name}</h4>
                <p><b>Type:</b> {loc.type.title()}</p>
                <p><b>Confidence:</b> {loc.confidence.title()}</p>
                <p><b>Address:</b> {loc.full_address}</p>
                <hr>
                <p><b>Events:</b></p>
                <p>{loc.event_summary}</p>
            </div>
            """
            
            folium.Marker(
                [loc.latitude, loc.longitude],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"{loc.name} ({loc.type})",
                icon=folium.Icon(color=color, icon='info-sign')
            ).add_to(m)
        
        return m