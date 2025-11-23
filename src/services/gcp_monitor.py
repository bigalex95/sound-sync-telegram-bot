from datetime import datetime, timezone
from typing import Optional
import logging

try:
    from google.cloud import monitoring_v3
    from google.api_core.exceptions import GoogleAPIError
    GCP_AVAILABLE = True
except ImportError:
    GCP_AVAILABLE = False

logger = logging.getLogger(__name__)


class GCPMonitor:
    """
    Service to fetch network egress metrics from GCP Cloud Monitoring.
    Uses Application Default Credentials (ADC) when running on GCP.
    """
    
    def __init__(self, project_id: Optional[str] = None, 
                 instance_id: Optional[str] = None, 
                 zone: Optional[str] = None):
        """
        Initialize GCP Monitor.
        
        Args:
            project_id: GCP project ID
            instance_id: Compute Engine instance ID
            zone: Instance zone (e.g., 'us-west1-a')
        """
        self.project_id = project_id
        self.instance_id = instance_id
        self.zone = zone
        self._client = None
        
    def is_configured(self) -> bool:
        """
        Check if GCP monitoring is properly configured.
        
        Returns:
            True if all required configuration is present and library is available
        """
        if not GCP_AVAILABLE:
            logger.debug("google-cloud-monitoring library not available")
            return False
            
        if not all([self.project_id, self.instance_id, self.zone]):
            logger.debug("GCP configuration incomplete: project_id=%s, instance_id=%s, zone=%s",
                        self.project_id, self.instance_id, self.zone)
            return False
            
        return True
    
    def _get_client(self):
        """
        Get or create the monitoring client.
        Uses Application Default Credentials automatically.
        """
        if self._client is None:
            if GCP_AVAILABLE:
                self._client = monitoring_v3.MetricServiceClient()
        return self._client
    
    def get_network_egress(self, start_time: Optional[datetime] = None, 
                          end_time: Optional[datetime] = None) -> Optional[int]:
        """
        Fetch total network egress (sent bytes) for the instance.
        
        Args:
            start_time: Start of time range (defaults to start of current month UTC)
            end_time: End of time range (defaults to now UTC)
            
        Returns:
            Total bytes sent, or None if unable to fetch
        """
        if not self.is_configured():
            logger.warning("GCP monitoring not configured, cannot fetch network egress")
            return None
        
        # Default to current month
        if end_time is None:
            end_time = datetime.now(timezone.utc)
        
        if start_time is None:
            start_time = end_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        try:
            client = self._get_client()
            project_name = f"projects/{self.project_id}"
            
            # Build the metric filter
            # Metric: compute.googleapis.com/instance/network/sent_bytes_count
            metric_filter = (
                f'metric.type = "compute.googleapis.com/instance/network/sent_bytes_count" '
                f'AND resource.labels.instance_id = "{self.instance_id}" '
                f'AND resource.labels.zone = "{self.zone}"'
            )
            
            # Create time interval
            interval = monitoring_v3.TimeInterval(
                {
                    "end_time": {"seconds": int(end_time.timestamp())},
                    "start_time": {"seconds": int(start_time.timestamp())},
                }
            )
            
            # Request time series data
            results = client.list_time_series(
                request={
                    "name": project_name,
                    "filter": metric_filter,
                    "interval": interval,
                    "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
                }
            )
            
            # Sum up all data points
            total_bytes = 0
            for result in results:
                for point in result.points:
                    # The value is a delta (bytes sent in the interval)
                    total_bytes += point.value.int64_value
            
            logger.info("Fetched GCP network egress: %d bytes from %s to %s", 
                       total_bytes, start_time, end_time)
            return total_bytes
            
        except GoogleAPIError as e:
            logger.error("GCP API error fetching network metrics: %s", e)
            return None
        except Exception as e:
            logger.error("Unexpected error fetching network metrics: %s", e)
            return None
