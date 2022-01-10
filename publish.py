import io
from avro.io import DatumReader, BinaryDecoder
from confluent_kafka.cimpl import Producer, Consumer
from confluent_kafka.avro import AvroProducer
from confluent_kafka import avro


class Producer:
    """
    An AVRO producer in charge of publishing/consuming events based on schema
    registry running in with docker ("docker compose up" to be able to run).
    """

    def __init__(self):
        """
        Initialisation of the AVRO producer along with AVRO schemas.
        """
        # This is what we need to think about. Opinion: simple for now.
        self.key_schema = avro.loads("""{"type": "string"}""")
        self.value_schema = avro.loads(
            """{"type": "map",
                "name": "event",
                "fields": [
                    {"name": "source_request_id", "type": "string"}]
                }
            """)
        config = {'bootstrap.servers': '0.0.0.0:9092',
                  'schema.registry.url': 'http://0.0.0.0:8081'}
        self.avro_producer = AvroProducer(
            config,
            default_key_schema=self.key_schema,
            default_value_schema=self.value_schema)

    def produce(self):
        """
        Produce an over-simplified event encoded with AVRO.
        """
        # This is the event that should match the schemas defined in init.
        key = "test"
        value = {"source_request_id": "527549db-c058-43e3-90d6-65dab31e40a1"}

        print("Producing ...")
        self.avro_producer.produce(
            topic="cust-perso-phoenix-recommendations-eventcollector-activity",
            key=key,
            value=value)
        print("... Message produced")

    def deserialize(self, msg_value):
        """
        Deserialize AVRO message consumed.
        :param obj msg_value: the messaged consumed.
        :return dict event_dict: the event in a dict format.
        """
        reader = DatumReader(self.value_schema)
        message_bytes = io.BytesIO(msg_value)
        decoder = BinaryDecoder(message_bytes)
        event_dict = reader.read(decoder)
        return event_dict

    def consume(self):
        """
        Consume the AVRO-serialised event.
        """
        config_producer = {"bootstrap.servers": "0.0.0.0:9092",
                           "group.id": "test1",
                           'auto.offset.reset': 'earliest'}
        kafka_consumer = Consumer(config_producer)
        kafka_consumer.subscribe(
            ["cust-perso-phoenix-recommendations-eventcollector-activity"])
        while True:
            msg = kafka_consumer.poll(timeout=0.1)
            if msg is None:
                continue
            print("Deserialize...")
            msg_value = self.deserialize(msg.value())
            print(msg_value)

if __name__ == "__main__":
    producer = Producer()
    producer.produce()
    producer.consume()

