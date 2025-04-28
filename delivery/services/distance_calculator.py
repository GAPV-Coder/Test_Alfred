from geographiclib.geodesic import Geodesic

class DistanceCalculator:
    """
    Class to calculate the distance and estimated time between two geographic points.
    """
    
    AVERAGE_SPEED_KMH = 40
    
    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate the distance in kilometers between two points using Haversine's formula.
        """
        geod = Geodesic.WGS84
        result = geod.Inverse(lat1, lon1, lat2, lon2)
        return result['s12'] / 100
    
    @staticmethod
    def calculate_estimated_time(distance: float) -> float:
        """
        Calculates the estimated time of arrival in minutes based on distance.
        """
        return (distance / DistanceCalculator.AVERAGE_SPEED_KMH) * 60