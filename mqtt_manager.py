from simple import MQTTClient
import mqtt_setup_conf
import time

mqtt_host = "io.adafruit.com"

def setup_mqtt():
    """
    This function sets up the MQTT client and connects it to the Adafruit IO broker.

    Returns:
        client: The MQTT client instance.
    """
    try:
        client = MQTTClient(client_id=mqtt_setup_conf.ada_id, server=mqtt_host, user=mqtt_setup_conf.username, password=mqtt_setup_conf.key, keepalive=60)
        client.connect()
        print("Connected to Adafruit IO")
        return client
    except Exception as e:
        print(f"Failed to connect to Adafruit IO, error: {str(e)}")
        time.sleep(5)
        
    print("Unable to connect to Adafruit IO after retries.")
    return None


def publish_mqtt(client, topic, message):
    """
    This function publishes a message to a specified MQTT topic.
    
    Args:
        client: The MQTT client instance.
        topic: The MQTT topic to publish the message to.
        message: The message to publish.
        
    Returns:
        Returns _true_ if the message is published successfully, _false_ otherwise.
    """
    if None in [client, topic, message]:
        print(f"Cannot publish due to None value - Client: {client}, Topic: {topic}, Message: {message}")
        return False
    try:
        print(f"Publishing message to topic {topic}: {message}")
        client.publish(topic, message)
        print("Message published successfully.")
        return True
    except Exception as e:
        print(f"Failed to publish message. Error: {str(e)}")
        return False
