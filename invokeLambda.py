import RPi.GPIO as GPIO
import sys
sys.path.append('/home/pi/MFRC522-python')
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

def invoke_function():
    """ Invokes the function. """

    #Enter region name (ex: us-east-1), access key, and access key ID inside ''
    lam = boto3.client('lambda', region_name='', aws_secret_access_key='', aws_access_key_id='')
    #Enter function name inside '' (ex: arn:aws:lambda:[region]:[numbers]:function:[function name]
    resp = lam.invoke(
        FunctionName='',
        InvocationType='RequestResponse',
        LogType='Tail')

    print(resp)
    return resp

print("Hold a tag near the reader")

try:
    id, text = reader.read()
    print(id)
    print(text)

finally:
    GPIO.cleanup()
