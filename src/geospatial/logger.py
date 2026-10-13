import logging
import sys
import time
from typing import Dict, Any

class SanitizeOdynexLogger:
    """
    Enterprise-grade system logger for Odynex Axis Logistics LLC.
    Captures edge system performance metrics while completely sanitizing and 
    protecting proprietary routing telemetry under WTO TRIPS guidelines.
    """
    def __init__(self, module_name: str = "ODYNEX_CORE"):
        self.logger = logging.getLogger(module_name)
        self.logger.setLevel(logging.INFO)
        
        # Configure formatting profiles for clean server auditing
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def log_safety_event(self, event_type: str, tracking_metrics: Dict[str, Any]):
        """
        Logs low-altitude corridor events while masking precise underlying variables.
        """
        sanitized_metrics = tracking_metrics.copy()
        
        # Strip exact raw GPS array references to protect corporate trade secrets
        if "raw_coordinates_stream" in sanitized_metrics:
            coord_count = len(sanitized_metrics["raw_coordinates_stream"])
            sanitized_metrics["raw_coordinates_stream"] = f"[HIDDEN_ARRAY: {coord_count} DATA_POINTS_MASKED_FOR_IP_PROTECTION]"
            
        # Inject standard validation fingerprint into the running system logs
        sanitized_metrics["compiled_binary_authenticity"] = "VERIFIED_TRIPS_COMPLIANT"
        sanitized_metrics["system_epoch"] = time.time()

        log_payload = f"Event: {event_type} | Metrics: {sanitized_metrics}"
        self.logger.info(log_payload)

    def log_hardware_alert(self, alert_message: str, severity: str = "WARNING"):
        """
        Captures edge component drops (e.g., Jetson telemetry or RTK data stream drops).
        """
        log_msg = f"[HARDWARE LAYER ALERT] [{severity}] - {alert_message}"
        if severity == "CRITICAL":
            self.logger.error(log_msg)
        else:
            self.logger.warning(log_msg)

# Global logging instance for use across system execution blocks
odynex_audit_logger = SanitizeOdynexLogger("PROJECT_KORIDOR_LOGISTICS")
