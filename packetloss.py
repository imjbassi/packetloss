import logging
from ping3 import ping, verbose_ping
import time
from datetime import datetime

# Configuration
target = 'google.com'
timeout = 1
interval = 0.5  # Monitor more frequently
alert_threshold = 20  # Percentage of packet loss at which to alert
log_file = 'internet_monitor.log'

# Setup logging to capture everything, including print statements
logging.basicConfig(filename=log_file, level=logging.INFO,
                    format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def log_event(message):
    # Now, only use logging to record events. Removed print to avoid console clutter.
    logging.info(message)

def monitor_packet_loss(target, timeout, interval, alert_threshold):
    log_event(f"Monitoring packet loss to {target} every {interval} seconds. Alert threshold: {alert_threshold}%.")
    packet_sent = 0
    packet_lost = 0

    try:
        while True:
            result = ping(target, timeout=timeout)
            packet_sent += 1
            if result is False:
                packet_lost += 1
                log_event("Packet lost.")

            # Calculate and log packet loss percentage every 10 packets
            if packet_sent % 10 == 0:
                loss_percentage = (packet_lost / packet_sent) * 100
                log_event(f"Packet sent: {packet_sent}, Packet lost: {packet_lost}, Loss percentage: {loss_percentage:.2f}%")

                if loss_percentage >= alert_threshold:
                    log_event(f"ALERT: Packet loss exceeded threshold with {loss_percentage:.2f}% loss.")

            time.sleep(interval)
    except KeyboardInterrupt:
        # Final calculation before exiting
        loss_percentage = (packet_lost / packet_sent) * 100 if packet_sent else 0
        log_event(f"Monitoring ended. Final packet sent: {packet_sent}, Packet lost: {packet_lost}, Final loss percentage: {loss_percentage:.2f}%.")

if __name__ == "__main__":
    monitor_packet_loss(target, timeout, interval, alert_threshold)
