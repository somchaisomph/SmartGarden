import microgear.client as netpie
import time
import base64
from PIL import Image
from io import BytesIO
import zlib

key = '<your key>'
secret = '<your secret key>'
app = 'your application name>'

netpie.create(key,secret,app,{'debugmode': True})
connected = False

def connection():
 global connected
 connected = True
 print("Connected")
 
def subscription(topic,msg):
 global this_role,ready_to_receive 
 if this_role == 'receiver' :
  if not ready_to_receive :
   if msg=='ruok' :
    netpie.chat(those_name,'iamok')
    ready_to_receive = True
    
  else : 
   print "recieving image data."
   decode_base64(msg,None) # don't need to save on disk
   print "process is done"
 else :
  print(topic+":"+msg)

def callback_error(msg) :
    print(msg)

def callback_reject(msg) :
    print (msg)
    print ("Script exited")
    exit(0)

def encode_base64(img_data):
 encoded = None

 try:
  #compress it first.
  compressed_data = zlib.compress(img_data.getvalue(),9)
  #encode it to base64 string
  encoded = base64.b64encode(compressed_data)  
 except:
  pass 
  
 return encoded
  
def decode_base64(compressed_b64str=None,save_to_file=None): 
 try :
  #firstly, decode it
  decoded = base64.decodestring(compressed_b64str)
  decompr = zlib.decompress(decoded)
  #save it if is needed.
  if save_to_file is not None:
   with open(save_to_file,"wb") as fh:
    fh.write(decompr)
  else:
   #just display on screen
   w,h = 640,480
   image = Image.open(BytesIO(decompr))
   image.show()
 except:
  pass   


this_name = 'n3a1'     
those_name = 'n3a2'
this_role = 'receiver'
running = True
ready_to_receive = False 

netpie.setname(this_name)
netpie.on_reject = callback_reject
netpie.on_connect = connection
netpie.on_message = subscription
netpie.on_error = callback_error
netpie.subscribe("/test")
netpie.connect(False)


try :
 while running:
  pass
except KeyboardInterrupt :
 running=False 
