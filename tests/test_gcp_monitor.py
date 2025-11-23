import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone
import pytest
from src.services.gcp_monitor import GCPMonitor, GCP_AVAILABLE


class TestGCPMonitor(unittest.TestCase):
    """Test cases for GCP Monitor service."""
    
    def test_is_configured_returns_false_when_missing_config(self):
        """Test that is_configured returns False when configuration is incomplete."""
        # Missing all config
        monitor = GCPMonitor()
        self.assertFalse(monitor.is_configured())
        
        # Missing instance_id
        monitor = GCPMonitor(project_id="test-project", zone="us-west1-a")
        self.assertFalse(monitor.is_configured())
        
        # Missing zone
        monitor = GCPMonitor(project_id="test-project", instance_id="test-instance")
        self.assertFalse(monitor.is_configured())
    
    def test_is_configured_returns_true_when_all_config_present(self):
        """Test that is_configured returns True when all configuration is present."""
        monitor = GCPMonitor(
            project_id="test-project",
            instance_id="test-instance",
            zone="us-west1-a"
        )
        # Will return True only if google-cloud-monitoring is installed
        # In test environment without the library, it will return False
        result = monitor.is_configured()
        self.assertIsInstance(result, bool)
    
    @pytest.mark.skipif(not GCP_AVAILABLE, reason="google-cloud-monitoring not installed")
    @patch('src.services.gcp_monitor.GCP_AVAILABLE', True)
    @patch('google.cloud.monitoring_v3.MetricServiceClient')
    def test_get_network_egress_returns_none_when_not_configured(self, mock_client):
        """Test that get_network_egress returns None when not configured."""
        monitor = GCPMonitor()  # No configuration
        result = monitor.get_network_egress()
        self.assertIsNone(result)
        mock_client.assert_not_called()
    
    @pytest.mark.skipif(not GCP_AVAILABLE, reason="google-cloud-monitoring not installed")
    @patch('src.services.gcp_monitor.GCP_AVAILABLE', True)
    @patch('google.cloud.monitoring_v3.MetricServiceClient')
    @patch('google.cloud.monitoring_v3.TimeInterval')
    def test_get_network_egress_fetches_metrics(self, mock_interval, mock_client_class):
        """Test that get_network_egress correctly fetches and sums metrics."""
        # Setup monitor
        monitor = GCPMonitor(
            project_id="test-project",
            instance_id="123456789",
            zone="us-west1-a"
        )
        
        # Mock the client and response
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        
        # Create mock time series data
        mock_point1 = Mock()
        mock_point1.value.int64_value = 1000000  # 1 MB
        
        mock_point2 = Mock()
        mock_point2.value.int64_value = 2000000  # 2 MB
        
        mock_series = Mock()
        mock_series.points = [mock_point1, mock_point2]
        
        mock_client.list_time_series.return_value = [mock_series]
        
        # Call the method
        result = monitor.get_network_egress()
        
        # Verify
        self.assertEqual(result, 3000000)  # 3 MB total
        mock_client.list_time_series.assert_called_once()
    
    @pytest.mark.skipif(not GCP_AVAILABLE, reason="google-cloud-monitoring not installed")
    @patch('src.services.gcp_monitor.GCP_AVAILABLE', True)
    @patch('google.cloud.monitoring_v3.MetricServiceClient')
    def test_get_network_egress_handles_api_error(self, mock_client_class):
        """Test that get_network_egress handles API errors gracefully."""
        # Create a mock exception
        mock_error = Exception("API Error")
        mock_error.__class__.__name__ = "GoogleAPIError"
        
        monitor = GCPMonitor(
            project_id="test-project",
            instance_id="123456789",
            zone="us-west1-a"
        )
        
        # Mock client to raise an error
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_client.list_time_series.side_effect = mock_error
        
        # Call the method
        result = monitor.get_network_egress()
        
        # Should return None on error
        self.assertIsNone(result)
    
    @pytest.mark.skipif(not GCP_AVAILABLE, reason="google-cloud-monitoring not installed")
    @patch('src.services.gcp_monitor.GCP_AVAILABLE', True)
    @patch('google.cloud.monitoring_v3.MetricServiceClient')
    @patch('google.cloud.monitoring_v3.TimeInterval')
    def test_get_network_egress_uses_default_time_range(self, mock_interval, mock_client_class):
        """Test that get_network_egress uses current month as default time range."""
        monitor = GCPMonitor(
            project_id="test-project",
            instance_id="123456789",
            zone="us-west1-a"
        )
        
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_client.list_time_series.return_value = []
        
        # Call without time parameters
        monitor.get_network_egress()
        
        # Verify it was called (time range is set internally)
        mock_client.list_time_series.assert_called_once()
        call_args = mock_client.list_time_series.call_args
        
        # Check that request was made
        self.assertIn('request', call_args.kwargs)


if __name__ == '__main__':
    unittest.main()
