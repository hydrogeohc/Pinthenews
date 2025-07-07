"""
MCP (Model Context Protocol) Integration for News Location Mapping
Provides advanced Claude API integration with context management
"""

import os
import json
import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from anthropic import Anthropic
from mcp import Client, ServerTransport
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class MCPContext:
    """Context data for MCP operations"""
    session_id: str
    article_content: str
    extracted_locations: List[Dict]
    geocoded_locations: List[Dict]
    processing_status: str
    error_messages: List[str]
    metadata: Dict[str, Any]


class MCPNewsLocationClient:
    """MCP client for news location mapping operations"""
    
    def __init__(self, anthropic_api_key: str = None):
        self.anthropic_client = Anthropic(
            api_key=anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
        )
        self.contexts: Dict[str, MCPContext] = {}
        self.current_session_id = None
    
    def create_session(self, session_id: str = None) -> str:
        """Create a new MCP session"""
        if session_id is None:
            import uuid
            session_id = str(uuid.uuid4())
        
        self.contexts[session_id] = MCPContext(
            session_id=session_id,
            article_content="",
            extracted_locations=[],
            geocoded_locations=[],
            processing_status="initialized",
            error_messages=[],
            metadata={}
        )
        
        self.current_session_id = session_id
        logger.info(f"Created MCP session: {session_id}")
        return session_id
    
    def get_session_context(self, session_id: str = None) -> Optional[MCPContext]:
        """Get session context"""
        session_id = session_id or self.current_session_id
        return self.contexts.get(session_id)
    
    def update_session_status(self, status: str, session_id: str = None):
        """Update session processing status"""
        session_id = session_id or self.current_session_id
        if session_id in self.contexts:
            self.contexts[session_id].processing_status = status
            logger.info(f"Session {session_id} status updated to: {status}")
    
    def add_error(self, error_message: str, session_id: str = None):
        """Add error message to session"""
        session_id = session_id or self.current_session_id
        if session_id in self.contexts:
            self.contexts[session_id].error_messages.append(error_message)
            logger.error(f"Session {session_id} error: {error_message}")
    
    async def enhanced_location_extraction(self, article_text: str, session_id: str = None) -> List[Dict]:
        """Enhanced location extraction with MCP context management"""
        session_id = session_id or self.current_session_id
        context = self.get_session_context(session_id)
        
        if not context:
            raise ValueError(f"No active session found: {session_id}")
        
        try:
            self.update_session_status("extracting_locations", session_id)
            context.article_content = article_text
            
            # Enhanced prompt with context awareness
            system_prompt = """
            You are an expert geographical intelligence analyst with access to comprehensive 
            global geographical databases. Your task is to perform advanced location extraction 
            with high precision and contextual understanding.
            
            Capabilities:
            - Identify both explicit and implicit geographical references
            - Recognize colloquial and alternative names for locations
            - Understand geographical relationships and hierarchies
            - Distinguish between different types of geographical entities
            - Provide confidence assessments based on context
            """
            
            user_prompt = f"""
            Perform advanced geographical entity extraction from this news article. 
            
            Extract ALL geographical locations with the following enhanced analysis:
            
            1. **Primary Locations**: Cities, towns, villages, settlements
            2. **Administrative Regions**: States, provinces, counties, districts
            3. **Countries and Territories**: Nations, territories, autonomous regions
            4. **Landmarks and POIs**: Buildings, monuments, venues, facilities
            5. **Geographical Features**: Mountains, rivers, lakes, parks, beaches
            6. **Transportation Hubs**: Airports, ports, train stations, highways
            7. **Neighborhoods and Districts**: Local areas, suburbs, quarters
            8. **Implicit Locations**: Referenced through context or relationships
            
            For each location, provide:
            {{
                "location": "exact name as mentioned",
                "standardized_name": "standard geographical name",
                "type": "specific type (city/state/country/landmark/etc.)",
                "confidence": "high/medium/low with reasoning",
                "context": "sentence/phrase where mentioned",
                "coordinates_hint": "any coordinate clues if mentioned",
                "related_locations": ["other locations mentioned nearby"],
                "importance": "primary/secondary/tertiary role in the article"
            }}
            
            Article text:
            {article_text}
            
            Return only valid JSON array, no other text.
            """
            
            response = await self._call_claude_async(system_prompt, user_prompt)
            
            # Parse and validate response
            locations = self._parse_location_response(response)
            context.extracted_locations = locations
            
            self.update_session_status("locations_extracted", session_id)
            logger.info(f"Extracted {len(locations)} locations for session {session_id}")
            
            return locations
            
        except Exception as e:
            error_msg = f"Location extraction failed: {str(e)}"
            self.add_error(error_msg, session_id)
            self.update_session_status("error", session_id)
            raise
    
    async def intelligent_geocoding(self, locations: List[Dict], session_id: str = None) -> List[Dict]:
        """Intelligent geocoding with MCP context and fallback strategies"""
        session_id = session_id or self.current_session_id
        context = self.get_session_context(session_id)
        
        if not context:
            raise ValueError(f"No active session found: {session_id}")
        
        try:
            self.update_session_status("geocoding_locations", session_id)
            
            geocoded_locations = []
            
            for location in locations:
                try:
                    # Try primary geocoding
                    geocoded = await self._geocode_with_context(location, context)
                    if geocoded:
                        geocoded_locations.append(geocoded)
                    else:
                        # Try fallback strategies
                        fallback_geocoded = await self._geocode_with_fallbacks(location, context)
                        if fallback_geocoded:
                            geocoded_locations.append(fallback_geocoded)
                        else:
                            logger.warning(f"Failed to geocode: {location['location']}")
                            
                except Exception as e:
                    logger.error(f"Geocoding error for {location['location']}: {str(e)}")
                    continue
            
            context.geocoded_locations = geocoded_locations
            self.update_session_status("geocoding_complete", session_id)
            
            return geocoded_locations
            
        except Exception as e:
            error_msg = f"Geocoding failed: {str(e)}"
            self.add_error(error_msg, session_id)
            self.update_session_status("error", session_id)
            raise
    
    async def generate_contextual_summaries(self, locations: List[Dict], session_id: str = None) -> List[Dict]:
        """Generate contextual event summaries with MCP enhancement"""
        session_id = session_id or self.current_session_id
        context = self.get_session_context(session_id)
        
        if not context:
            raise ValueError(f"No active session found: {session_id}")
        
        try:
            self.update_session_status("generating_summaries", session_id)
            
            enhanced_locations = []
            
            for location in locations:
                try:
                    # Generate enhanced summary
                    summary = await self._generate_enhanced_summary(location, context)
                    location['event_summary'] = summary
                    enhanced_locations.append(location)
                    
                except Exception as e:
                    logger.error(f"Summary generation error for {location['location']}: {str(e)}")
                    location['event_summary'] = f"Events at {location['location']}: {location.get('context', 'Information available in article')}"
                    enhanced_locations.append(location)
            
            self.update_session_status("summaries_complete", session_id)
            return enhanced_locations
            
        except Exception as e:
            error_msg = f"Summary generation failed: {str(e)}"
            self.add_error(error_msg, session_id)
            self.update_session_status("error", session_id)
            raise
    
    async def _call_claude_async(self, system_prompt: str, user_prompt: str) -> str:
        """Async call to Claude API"""
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=2000,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Claude API call failed: {str(e)}")
            raise
    
    def _parse_location_response(self, response: str) -> List[Dict]:
        """Parse and validate location extraction response"""
        try:
            # Clean response
            if response.startswith('```json'):
                response = response[7:-3]
            elif response.startswith('```'):
                response = response[3:-3]
            
            locations = json.loads(response)
            
            # Validate structure
            validated_locations = []
            for loc in locations:
                if isinstance(loc, dict) and 'location' in loc:
                    validated_locations.append(loc)
            
            return validated_locations
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Location parsing error: {str(e)}")
            return []
    
    async def _geocode_with_context(self, location: Dict, context: MCPContext) -> Optional[Dict]:
        """Geocode location with context awareness"""
        from geopy.geocoders import Nominatim
        import asyncio
        
        geolocator = Nominatim(user_agent="news_location_mapper_mcp")
        
        try:
            # Try primary location name
            location_name = location.get('standardized_name', location['location'])
            
            # Add context hints if available
            if 'coordinates_hint' in location and location['coordinates_hint']:
                location_name += f" {location['coordinates_hint']}"
            
            # Add related locations for context
            if 'related_locations' in location and location['related_locations']:
                for related in location['related_locations'][:2]:  # Use first 2 related locations
                    location_name += f" near {related}"
            
            # Geocode with delay to respect rate limits
            await asyncio.sleep(1)
            result = geolocator.geocode(location_name)
            
            if result:
                return {
                    **location,
                    'latitude': result.latitude,
                    'longitude': result.longitude,
                    'full_address': result.address,
                    'geocoding_method': 'primary',
                    'geocoding_confidence': 'high'
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Geocoding error: {str(e)}")
            return None
    
    async def _geocode_with_fallbacks(self, location: Dict, context: MCPContext) -> Optional[Dict]:
        """Geocode with fallback strategies"""
        from geopy.geocoders import Nominatim
        import asyncio
        
        geolocator = Nominatim(user_agent="news_location_mapper_mcp_fallback")
        
        fallback_strategies = [
            location['location'],  # Original name
            location.get('standardized_name', location['location']),  # Standardized name
            f"{location['location']}, {location.get('type', 'place')}",  # With type
        ]
        
        # Add related locations as context
        if 'related_locations' in location and location['related_locations']:
            for related in location['related_locations'][:1]:
                fallback_strategies.append(f"{location['location']}, {related}")
        
        for strategy in fallback_strategies:
            try:
                await asyncio.sleep(1)
                result = geolocator.geocode(strategy)
                
                if result:
                    return {
                        **location,
                        'latitude': result.latitude,
                        'longitude': result.longitude,
                        'full_address': result.address,
                        'geocoding_method': 'fallback',
                        'geocoding_confidence': 'medium'
                    }
                    
            except Exception as e:
                continue
        
        return None
    
    async def _generate_enhanced_summary(self, location: Dict, context: MCPContext) -> str:
        """Generate enhanced event summary with context"""
        try:
            system_prompt = """
            You are an expert news analyst specializing in location-based event summarization.
            Create concise, informative summaries of events at specific locations.
            """
            
            user_prompt = f"""
            Create a brief, engaging summary (1-2 sentences) of events at "{location['location']}" 
            based on this news article.
            
            Location details:
            - Name: {location['location']}
            - Type: {location.get('type', 'location')}
            - Context: {location.get('context', 'N/A')}
            - Importance: {location.get('importance', 'secondary')}
            
            Article excerpt (first 1500 characters):
            {context.article_content[:1500]}
            
            Requirements:
            - Focus on events/activities at this specific location
            - Be concise but informative
            - Use active voice
            - Include key details (who, what, when if available)
            - Make it engaging for map popup display
            """
            
            response = await self._call_claude_async(system_prompt, user_prompt)
            return response.strip()
            
        except Exception as e:
            logger.error(f"Summary generation error: {str(e)}")
            return f"Events at {location['location']}: {location.get('context', 'Information available in article')}"
    
    def get_session_summary(self, session_id: str = None) -> Dict[str, Any]:
        """Get complete session summary"""
        session_id = session_id or self.current_session_id
        context = self.get_session_context(session_id)
        
        if not context:
            return {"error": "Session not found"}
        
        return {
            "session_id": session_id,
            "status": context.processing_status,
            "locations_extracted": len(context.extracted_locations),
            "locations_geocoded": len(context.geocoded_locations),
            "errors": context.error_messages,
            "metadata": context.metadata
        }
    
    def export_session_data(self, session_id: str = None) -> Dict[str, Any]:
        """Export complete session data"""
        session_id = session_id or self.current_session_id
        context = self.get_session_context(session_id)
        
        if not context:
            return {"error": "Session not found"}
        
        return asdict(context)


class MCPNewsLocationServer:
    """MCP server for news location mapping"""
    
    def __init__(self):
        self.client = MCPNewsLocationClient()
        self.active_sessions = {}
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP requests"""
        try:
            method = request.get('method')
            params = request.get('params', {})
            
            if method == 'create_session':
                session_id = self.client.create_session()
                return {"session_id": session_id, "status": "created"}
            
            elif method == 'process_article':
                session_id = params.get('session_id')
                article_text = params.get('article_text')
                
                if not session_id or not article_text:
                    return {"error": "Missing session_id or article_text"}
                
                # Process through MCP pipeline
                locations = await self.client.enhanced_location_extraction(article_text, session_id)
                geocoded = await self.client.intelligent_geocoding(locations, session_id)
                enhanced = await self.client.generate_contextual_summaries(geocoded, session_id)
                
                return {
                    "session_id": session_id,
                    "locations": enhanced,
                    "summary": self.client.get_session_summary(session_id)
                }
            
            elif method == 'get_session_data':
                session_id = params.get('session_id')
                return self.client.export_session_data(session_id)
            
            else:
                return {"error": f"Unknown method: {method}"}
                
        except Exception as e:
            return {"error": str(e)}


# Example usage
async def main():
    """Example usage of MCP integration"""
    
    # Initialize MCP client
    mcp_client = MCPNewsLocationClient()
    
    # Create session
    session_id = mcp_client.create_session()
    print(f"Created session: {session_id}")
    
    # Example article text
    article_text = """
    A major earthquake struck near Los Angeles, California yesterday, causing significant damage 
    in downtown areas. The epicenter was located about 30 miles east of the city, near Riverside County. 
    Emergency services responded to multiple locations including the Hollywood area, Santa Monica, 
    and Beverly Hills. The Los Angeles International Airport temporarily suspended operations 
    while engineers inspected the runways for damage.
    """
    
    try:
        # Process article
        locations = await mcp_client.enhanced_location_extraction(article_text, session_id)
        geocoded = await mcp_client.intelligent_geocoding(locations, session_id)
        enhanced = await mcp_client.generate_contextual_summaries(geocoded, session_id)
        
        # Get session summary
        summary = mcp_client.get_session_summary(session_id)
        
        print("\nSession Summary:")
        print(json.dumps(summary, indent=2))
        
        print("\nEnhanced Locations:")
        for location in enhanced:
            print(f"- {location['location']}: {location.get('event_summary', 'N/A')}")
            
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())