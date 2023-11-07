

# def create_commit_postgres_data(batch_data, model, device, pg_session):
#     for row in batch_data:
#         try:
#             # Create a corresponding record in the PostgreSQL database
#             postgres_data = model()
#             for register_info in device["registers"]:
#                 col_name = register_info["column_name"]
#                 setattr(postgres_data, col_name, getattr(row, col_name))
#             postgres_data.timestamp = row.timestamp
#             PostgresSQL_session.add(postgres_data)
#         except IntegrityError as e:
#             pg_session.rollback()

#     # Commit the changes to the PostgreSQL database
#     pg_session.commit()

# # -------------------------------------------------------------------------
# # mqtt
# # -------------------------------------------------------------------------

import paho.mqtt.client as mqtt
import json

def mqtt_publish(data, mqtt_broker_host, mqtt_broker_port, mqtt_topic):
    try:
        mqtt_client = mqtt.Client()
        mqtt_client.connect(mqtt_broker_host, mqtt_broker_port)
        mqtt_client.publish(mqtt_topic, json.dumps(data))
        mqtt_client.disconnect()
        print(f"Published data to MQTT: {data}")
    except Exception as e:
        print(f"Error publishing data to MQTT: {e}")
