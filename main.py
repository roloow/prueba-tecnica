from google.cloud import storage, kms
import pandas as pd
import gcsfs

# Variables
proyecto = 'prueba-tecnica'
bucket = '2020-11-10'
key = 'GlobalLandTemperaturesByCountry.csv'
encrypted_columns = ['Latitude', 'Longitude']
group = 'Country'
path = 'gs://{0}/{1}'
out = 'output-falabella'

def encrypt_symmetric(plaintext, project_id='prueba-tecnica-295209', location_id='global', key_ring_id='prueba', key_id='clave'):
    """
    Encrypt plaintext using a symmetric key.

    Args:
        project_id (string): Google Cloud project ID (e.g. 'my-project').
        location_id (string): Cloud KMS location (e.g. 'us-east1').
        key_ring_id (string): ID of the Cloud KMS key ring (e.g. 'my-key-ring').
        key_id (string): ID of the key to use (e.g. 'my-key').
        plaintext (string): message to encrypt

    Returns:
        bytes: Encrypted ciphertext.

    """

    # Import base64 for printing the ciphertext.
    import base64

    # Convert the plaintext to bytes.
    plaintext_bytes = plaintext.encode('utf-8')

    # Create the client.
    client = kms.KeyManagementServiceClient()

    # Build the key name.
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # Call the API.
    encrypt_response = client.encrypt(request={'name': key_name, 'plaintext': plaintext_bytes})
    #print('Ciphertext: {}'.format(base64.b64encode(encrypt_response.ciphertext)))
    return encrypt_response

encrypt = lambda x: encrypt_symmetric(x).ciphertext

fs = gcsfs.GCSFileSystem(project=proyecto, token='cloud')

df = pd.read_csv(path.format(bucket, key), dtype=str)

for column in set(df.columns).intersection(set(encrypted_columns)):
    df[column] = df[column].apply(encrypt)

for country, df_country in df.groupby(group):
    df_country.to_csv(path.format(out, country + '.csv'))
