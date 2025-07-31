"""
AxoDen Client - Core API client for AI-powered development guidance
"""

import os
import json
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid

from .config import AxoDenConfig
from .exceptions import AxoDenError, AuthenticationError, MethodologyNotFoundError
from .models import (
    AgentProfile, 
    MethodologyRequest,
    MethodologyRecommendation,
    ProjectContext
)


class AxoDenClient:
    """Main client for interacting with AxoDen's AI guidance system"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """Initialize AxoDen client
        
        Args:
            api_key: AxoDen API key (optional, can use env var AXODEN_API_KEY)
            base_url: API base URL (optional, defaults to https://api.axoden.com)
        """
        self.config = AxoDenConfig()
        self.api_key = api_key or self.config.api_key
        self.base_url = base_url or self.config.base_url
        self.agent_id = self.config.agent_id or self._generate_agent_id()
        
        if not self.api_key:
            raise AuthenticationError(
                "No API key found. Set AXODEN_API_KEY environment variable or pass api_key parameter"
            )
        
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": f"AxoDen-Client/{self.config.version}"
        })
        
        # Auto-register agent on initialization
        self._ensure_agent_registered()
    
    def _generate_agent_id(self) -> str:
        """Generate unique agent ID for this client"""
        hostname = os.uname().nodename
        username = os.environ.get("USER", "unknown")
        return f"claude-code-{username}-{hostname}-{uuid.uuid4().hex[:8]}"
    
    def _ensure_agent_registered(self):
        """Ensure this client's agent is registered with AxoDen"""
        try:
            # Check if agent exists
            response = self.session.get(f"{self.base_url}/api/v1/agents/{self.agent_id}")
            if response.status_code == 404:
                # Register new agent
                self._register_agent()
        except Exception as e:
            # Non-critical - agent registration can fail without blocking client
            print(f"Warning: Could not verify agent registration: {e}")
    
    def _register_agent(self):
        """Register this client as an agent"""
        agent_data = {
            "agent_id": self.agent_id,
            "name": f"Claude Code Client ({os.environ.get('USER', 'User')})",
            "cognitive_profile": {
                "processing": 0.7,  # Default profile for developers
                "focus": 0.8,
                "flexibility": 0.6,
                "abstraction": 0.7
            },
            "capabilities": [
                "claude_code_integration",
                "methodology_application",
                "development",
                "debugging",
                "analysis"
            ]
        }
        
        response = self.session.post(
            f"{self.base_url}/api/v1/agents/register",
            json=agent_data
        )
        
        if response.status_code != 200:
            print(f"Warning: Agent registration failed: {response.text}")
    
    def recommend(self, 
                  problem: str,
                  context: Optional[Dict[str, Any]] = None,
                  format: str = "claude") -> MethodologyRecommendation:
        """Get methodology recommendation for a problem
        
        Args:
            problem: Description of the problem or challenge
            context: Optional project context (language, framework, etc)
            format: Output format ('claude' for Claude Code optimized, 'json' for raw)
            
        Returns:
            MethodologyRecommendation object
        """
        # Detect project context if not provided
        if not context:
            context = self._detect_project_context()
        
        request_data = {
            "problem_description": problem,
            "project_context": context,
            "constraints": {
                "format": format,
                "agent_type": "claude_code"
            }
        }
        
        # Make request to assignment endpoint
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/assignments/request?agent_id={self.agent_id}",
                json=request_data
            )
            
            if response.status_code == 200:
                response_data = response.json()
                # Check if we got actual methodology data or just generic response
                if "methodology" in response_data or "steps" in response_data:
                    return self._parse_recommendation(response_data, format)
                else:
                    # API returned success but no methodology data
                    raise MethodologyNotFoundError(
                        f"API returned success but no methodology recommendations available. "
                        f"The deployed system may be missing the knowledge base. "
                        f"Response: {response_data}"
                    )
            else:
                # API returned error status
                raise MethodologyNotFoundError(
                    f"API request failed with status {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            raise MethodologyNotFoundError(
                f"Could not connect to AxoDen API or get methodology recommendation for: {problem}. "
                f"Error: {e}. Please check if the deployed system has the complete knowledge base."
            )
    
    def _detect_project_context(self) -> Dict[str, Any]:
        """Auto-detect project context from current directory"""
        context = {
            "language": "unknown",
            "framework": "unknown",
            "project_type": "general"
        }
        
        # Simple detection based on files in current directory
        files = os.listdir(".")
        
        # Language detection
        if "package.json" in files:
            context["language"] = "javascript"
            if "next.config.js" in files:
                context["framework"] = "nextjs"
            elif "vue.config.js" in files:
                context["framework"] = "vue"
        elif "requirements.txt" in files or "setup.py" in files:
            context["language"] = "python"
            if "manage.py" in files:
                context["framework"] = "django"
            elif "app.py" in files or "application.py" in files:
                context["framework"] = "flask"
        elif "Cargo.toml" in files:
            context["language"] = "rust"
        elif "go.mod" in files:
            context["language"] = "go"
        
        return context
    
    def _parse_recommendation(self, response_data: Dict, format: str) -> MethodologyRecommendation:
        """Parse API response into MethodologyRecommendation"""
        # This will need to adapt based on actual API response structure
        recommendation = MethodologyRecommendation(
            methodology_name=response_data.get("methodology", "Unknown"),
            description=response_data.get("description", ""),
            confidence=response_data.get("confidence", 0.5),
            steps=response_data.get("steps", []),
            reasoning=response_data.get("reasoning", ""),
            alternatives=response_data.get("alternatives", [])
        )
        
        if format == "claude":
            recommendation.format_for_claude_code()
        
        return recommendation
    
    # Fallback method removed - client now requires working API with real methodology database
    
    def list_methodologies(self, domain: Optional[str] = None) -> List[Dict[str, str]]:
        """List available methodologies, optionally filtered by domain"""
        # This would query the API for available methodologies
        # For now, return placeholder
        return [
            {"name": "Test-Driven Development", "domain": "software_development"},
            {"name": "Root Cause Analysis", "domain": "debugging"},
            {"name": "Design Thinking", "domain": "innovation"}
        ]
    
    def analyze_project(self, project_path: str = ".") -> Dict[str, Any]:
        """Analyze project and get methodology recommendations"""
        context = self._detect_project_context()
        
        # Would integrate with actual AxoDen analysis
        return {
            "project_context": context,
            "recommended_methodologies": [
                "Code Review Process",
                "Continuous Integration",
                "Documentation-Driven Development"
            ],
            "confidence": 0.8
        }