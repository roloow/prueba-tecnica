import os
from google.cloud import pubsub_v1


def publish (path_file, topic, project):
    publisher = pubsub_v1.PublisherClient()
    topic_name = 'projects/{project_id}/topics/{topic}'.format(
        project_id=os.getenv(project),
        topic=topic,  # Set this to something appropriate.
    )
    #publisher.create_topic(topic_name)
    publisher.publish(topic_name, path_file, spam='prueba-tecnica')

def hello_gcs(event, context):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    bucket = event['bucket']
    key = event['name']
    topico = 'prueba'
    projectid = 'prueba-tecnica-295209'
    msg = bucket +'/'+ key
    publish(msg.encode('utf-8'), topico, project_id)