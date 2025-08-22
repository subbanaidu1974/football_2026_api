
import enum


class PageStatus(str, enum.Enum):
    
    DRAFT = "DRAFT"
    
    PUBLISHED = "PUBLISHED"
    


class StageType(str, enum.Enum):
    
    GROUP = "GROUP"
    
    KO = "KO"
    


class MatchStatus(str, enum.Enum):
    
    SCHEDULED = "SCHEDULED"
    
    LIVE = "LIVE"
    
    FT = "FT"
    
    POSTPONED = "POSTPONED"
    
    CANCELED = "CANCELED"
    


class PartnerKind(str, enum.Enum):
    
    HOTEL = "HOTEL"
    
    FLIGHT = "FLIGHT"
    
    TOUR = "TOUR"
    
    TICKET = "TICKET"
    
    STREAMING = "STREAMING"
    


class TopicType(str, enum.Enum):
    
    TEAM = "TEAM"
    
    CITY = "CITY"
    
    COMPETITION = "COMPETITION"
    

