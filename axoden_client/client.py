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
        
        # Try new assignment endpoint first
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/assignments/request?agent_id={self.agent_id}",
                json=request_data
            )
            
            if response.status_code == 200:
                return self._parse_recommendation(response.json(), format)
        except Exception as e:
            print(f"Assignment endpoint failed: {e}")
        
        # Fallback to orchestration status for methodology info
        try:
            response = self.session.get(f"{self.base_url}/api/v1/orchestration/status")
            if response.status_code == 200:
                data = response.json()
                # Create synthetic recommendation from available data
                return self._create_fallback_recommendation(problem, data, format)
        except Exception:
            pass
        
        raise MethodologyNotFoundError(
            f"Could not get methodology recommendation for: {problem}"
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
    
    def _create_fallback_recommendation(self, 
                                       problem: str, 
                                       orchestration_data: Dict,
                                       format: str) -> MethodologyRecommendation:
        """Create recommendation from orchestration status when assignment fails"""
        # Extract methodology info from orchestration status
        axoden_info = orchestration_data.get("axoden", {})
        total_methodologies = axoden_info.get("total_methodologies", 0)
        
        # Create a generic but helpful recommendation
        recommendation = MethodologyRecommendation(
            methodology_name="Systematic Problem Analysis",
            description=f"Apply systematic analysis from AxoDen's {total_methodologies} methodologies",
            confidence=0.7,
            steps=[
                "1. Define the problem scope and constraints",
                "2. Analyze root causes systematically", 
                "3. Apply domain-specific best practices",
                "4. Iterate and validate solutions"
            ],
            reasoning=f"Based on '{problem}' and AxoDen's methodology database",
            alternatives=["Root Cause Analysis", "Design Thinking", "Test-Driven Development"]
        )
        
        if format == "claude":
            recommendation.format_for_claude_code()
            
        return recommendation
    
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