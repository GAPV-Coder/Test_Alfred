from geographiclib.geodesic import Geodesic

class DistanceCalculator:
    """
    Class to calculate the distance and estimated time between two geographic points.
    """
    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        """
        Calculate the distance in kilometers between two points using Haversine's formula.
        """
        from math import radians, sin, cos, sqrt, atan2
        R = 6371
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        return R * c
    
    @staticmethod
    def calculate_estimated_time(distance: float) -> float:
        """
        Calculates the estimated time of arrival in minutes based on distance.
        """
        speed_kmh = 40
        time_hours = distance / speed_kmh
        return time_hours * 60