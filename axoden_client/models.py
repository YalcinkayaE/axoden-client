"""
AxoDen Client - Data models for API interactions
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class CognitiveProfile:
    """Cognitive profile for methodology matching"""
    processing: float = 0.5
    focus: float = 0.5  
    flexibility: float = 0.5
    abstraction: float = 0.5


@dataclass
class AgentProfile:
    """Agent profile for AxoDen registration"""
    agent_id: str
    name: str
    cognitive_profile: CognitiveProfile
    capabilities: List[str] = field(default_factory=list)
    

@dataclass
class ProjectContext:
    """Project context for methodology recommendations"""
    language: str = "unknown"
    framework: str = "unknown"
    team_size: int = 1
    project_type: str = "general"
    complexity: str = "medium"
    

@dataclass
class MethodologyRequest:
    """Request for methodology recommendation"""
    problem_description: str
    project_context: ProjectContext
    constraints: Dict[str, Any] = field(default_factory=dict)
    

@dataclass 
class MethodologyRecommendation:
    """Methodology recommendation from AxoDen"""
    methodology_name: str
    description: str
    confidence: float
    steps: List[str]
    reasoning: str
    alternatives: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def format_for_claude_code(self) -> str:
        """Format recommendation for Claude Code consumption"""
        output = f"🎯 **Recommended Methodology: {self.methodology_name}**\n\n"
        output += f"📊 Confidence: {self.confidence:.0%}\n\n"
        output += f"📝 Description: {self.description}\n\n"
        
        if self.steps:
            output += "📋 **Implementation Steps:**\n"
            for i, step in enumerate(self.steps, 1):
                output += f"{i}. {step}\n"
            output += "\n"
        
        if self.reasoning:
            output += f"💡 **Reasoning:** {self.reasoning}\n\n"
            
        if self.alternatives:
            output += "🔄 **Alternative Approaches:**\n"
            for alt in self.alternatives:
                output += f"- {alt}\n"
        
        output += "\n---\n"
        output += "💭 *To apply this methodology, explain to Claude Code what you want to implement using these principles.*"
        
        return output
    
    def to_json(self) -> Dict[str, Any]:
        """Convert to JSON format"""
        return {
            "methodology": self.methodology_name,
            "description": self.description,
            "confidence": self.confidence,
            "steps": self.steps,
            "reasoning": self.reasoning,
            "alternatives": self.alternatives,
            "timestamp": self.timestamp.isoformat()
        }