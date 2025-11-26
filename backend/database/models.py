"""
MongoDB Database Models
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from bson import ObjectId

class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic v2"""
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema
        return core_schema.union_schema([
            core_schema.is_instance_schema(ObjectId),
            core_schema.chain_schema([
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(cls.validate),
            ])
        ])
    
    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class CriminalRecord(BaseModel):
    """Criminal Record Model"""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    record_id: str = Field(..., description="Unique record identifier")
    name: str = Field(..., description="Full name")
    age: Optional[int] = Field(None, description="Age")
    gender: Optional[str] = Field(None, description="Gender")
    height: Optional[float] = Field(None, description="Height in cm")
    weight: Optional[float] = Field(None, description="Weight in kg")
    eye_color: Optional[str] = Field(None, description="Eye color")
    hair_color: Optional[str] = Field(None, description="Hair color")
    
    # Criminal Information
    crime_type: Optional[str] = Field(None, description="Type of crime")
    crime_date: Optional[datetime] = Field(None, description="Date of crime")
    location: Optional[str] = Field(None, description="Location")
    status: Optional[str] = Field("active", description="Status: active, caught, inactive")
    
    # Images and Features
    photo_url: Optional[str] = Field(None, description="Photo file path")
    sketch_url: Optional[str] = Field(None, description="Sketch file path")
    feature_vector: Optional[List[float]] = Field(None, description="CNN extracted features")
    
    # Additional Information
    description: Optional[str] = Field(None, description="Additional details")
    aliases: Optional[List[str]] = Field(default_factory=list, description="Known aliases")
    tattoos: Optional[List[str]] = Field(default_factory=list, description="Tattoo descriptions")
    scars: Optional[List[str]] = Field(default_factory=list, description="Scar descriptions")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[str] = Field(None, description="User who created record")
    
    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True

class SketchRecord(BaseModel):
    """Sketch Record Model"""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    sketch_id: str = Field(..., description="Unique sketch identifier")
    sketch_url: str = Field(..., description="Sketch file path")
    sketch_type: str = Field(..., description="Type: manual, ai-generated")
    
    # Generation Details
    prompt: Optional[str] = Field(None, description="Text prompt for AI generation")
    components: Optional[Dict[str, Any]] = Field(None, description="Drag-drop components used")
    
    # Processing Results
    feature_vector: Optional[List[float]] = Field(None, description="Extracted features")
    enhanced_sketch_url: Optional[str] = Field(None, description="GAN enhanced sketch")
    face_detected: Optional[bool] = Field(False, description="Face detection result")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[str] = Field(None, description="User identifier")
    
    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True

class SearchResult(BaseModel):
    """Search Result Model"""
    record_id: str
    name: str
    photo_url: Optional[str]
    confidence_score: float
    feature_similarity: float
    rank: int

class SearchHistory(BaseModel):
    """Search History Model"""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    sketch_id: str = Field(..., description="Sketch used for search")
    sketch_url: str = Field(..., description="Sketch file path")
    
    # Search Results
    results: List[SearchResult] = Field(default_factory=list)
    total_matches: int = Field(0, description="Number of matches found")
    search_time: float = Field(..., description="Search execution time in seconds")
    
    # Metadata
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[str] = Field(None, description="User identifier")
    
    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True

class FacialComponent(BaseModel):
    """Facial Component for Drag & Drop"""
    component_id: str
    category: str  # eyes, nose, mouth, hair, etc.
    image_url: str
    position: Dict[str, float]  # x, y coordinates
    scale: float
    rotation: float
