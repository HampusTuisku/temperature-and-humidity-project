from machine import Pin, reset
from utime import sleep
import dht
import mqtt_setup
import mqtt_setup_conf
import json
import wifi_setup

wifi_setup.connect_wifi()
collect_data = False
led = Pin("LED", Pin.OUT)

def button_callback(topic, msg):
    """
    This function is called when a message is received on the subscribed topic.
    It updates the global variable `collect_data` based on the received message.
    
    Args:
    topic: The topic on which the message was received.
    msg: The message received on the topic.
    """
    global collect_data
    global led
    msg = msg.decode().upper()
    topic = topic.decode()
    print(f"Topic: {topic}, Message: {msg}")
    if topic == mqtt_setup_conf.control_topic:
        if msg =='ON':
            led.value(1)
            print('STARTING DATA COLLECTION...')
            collect_data = True
        elif msg == 'OFF':
            print('DATA COLLECTION STOPPED.')
            led = Pin("LED", Pin.OUT)
            led.value(0)
            collect_data = False
    

def ensure_mqtt_connection(client):
    """
    This function ensures that the MQTT client is connected to the broker.
    
    Args: 
    client: The MQTT client instance.
    
    Returns:
    client: The MQTT client instance.
    """
    if client is None:
        client = mqtt.setup_mqtt()
        if client is not None:
            client.set_callback(button_callback)
            # Subscribe to the control topic and convert it to bytes to be compatible with the MQTT library.
            client.subscribe(bytes(mqtt_setup_conf.control_topic, 'utf-8'))
            print(f'Subsrcibed to: {mqtt_setup_conf.control_topic}')
        else:
            print('Failed to connect to MQTT broker.')
    return client


client = mqtt.setup_mqtt()
if client:
    client.set_callback(button_callback)
    client.subscribe(bytes(mqtt_setup_conf.control_topic, 'utf-8'))
    print(f'Subscribed to: {mqtt_setup_conf.control_topic}')

dht11_sensor = dht.DHT11(Pin(14, Pin.IN, Pin.PULL_UP))

while True:
    client = ensure_mqtt_connection(client)
    try:
        # Check for new MQTT messages if client is connected.
        if client is not None:
            client.check_msg()
        
        dht11_sensor.measure()
        if collect_data:
            temperature_value = dht11_sensor.temperature()
            temp_message = json.dumps({"value": temperature_value})
            mqtt.publish_mqtt(client, mqtt_setup_conf.temp_topic, temp_message)
            
            humidity_value = dht11_sensor.humidity()
            humidity_message = json.dumps({"value": humidity_value})
            mqtt.publish_mqtt(client, mqtt_setup_conf.humidity_topic, humidity_message)
        
        # Sleep for 6 seconds before taking another measurement.
        sleep(6)  
    except Exception as e:
        print(f'Error during main loop: {str(e)}')
        # Reset the client to ensure that the connection is re-established.
        client = None
        sleep(2)
