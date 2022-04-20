import pickle, logging, hashlib
import argparse

# For locks: RSM_UNLOCKED=0 , RSM_LOCKED=1 
RSM_UNLOCKED = bytearray(b'\x00') * 1
RSM_LOCKED = bytearray(b'\x01') * 1

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

SERVER_REQUESTS = 0
# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
  rpc_paths = ('/RPC2',)

class DiskBlocks():
  def __init__(self, total_num_blocks, block_size):
    # This class stores the raw block array
    self.block = []
    #checksum data structure to store the data checksum hash
    self.checksum_datastructure = []                                            
    # Initialize raw blocks 
    for i in range (0, total_num_blocks):
      putdata = bytearray(block_size)
      self.block.insert(i,putdata)
      csm = hashlib.md5(bytes(putdata)).hexdigest()
      self.checksum_datastructure.append(csm)   
    
if __name__ == "__main__":

  # Construct the argument parser
  ap = argparse.ArgumentParser()

  ap.add_argument('-nb', '--total_num_blocks', type=int, help='an integer value')
  ap.add_argument('-bs', '--block_size', type=int, help='an integer value')
  ap.add_argument('-port', '--port', type=int, help='an integer value')
  ap.add_argument('-sid', '--serverid', type=int, help='an integer value')
  ap.add_argument('-cblk', '--corrupt_block', type=int, help='an integer value')

  args = ap.parse_args()

  if args.total_num_blocks:
    TOTAL_NUM_BLOCKS = args.total_num_blocks
  else:
    print('Must specify total number of blocks') 
    quit()

  if args.block_size:
    BLOCK_SIZE = args.block_size
  else:
    print('Must specify block size')
    quit()

  if args.port:
    PORT = args.port
  else:
    print('Must specify port number')
    quit()
    
  if args.serverid != None:
    SID = args.serverid
  else:
    print('Must specify server ID')
    quit()
  
  if args.corrupt_block != None:
    CBLK = args.corrupt_block
  else:
    CBLK = -1
    
  # initialize blocks
  RawBlocks = DiskBlocks(TOTAL_NUM_BLOCKS, BLOCK_SIZE)

  # Create server
  server = SimpleXMLRPCServer(("127.0.0.1", PORT), requestHandler=RequestHandler) 
          
  def Get(block_number):
    global SERVER_REQUESTS
    SERVER_REQUESTS += 1
    print("\n Server hits:- ", SERVER_REQUESTS)
    result = RawBlocks.block[block_number]
    csm = GetNewChecksum(bytes(result))
    if csm == RawBlocks.checksum_datastructure[block_number]:
        return result
    else:
        return -1

  server.register_function(Get)
    
  def GetNewChecksum(data):
    csm = hashlib.md5(data)
    return csm.hexdigest()
  
  def Put(block_number, data):
    global SERVER_REQUESTS
    SERVER_REQUESTS += 1
    print("\n Server hits:- ", SERVER_REQUESTS)
    #handling the corrupt block
    if CBLK != -1:
      if block_number == CBLK:
          stringbyte = bytearray("Block_Corrupted","utf-8")
          corrupt_data = bytearray(stringbyte.ljust(BLOCK_SIZE,b'\x00'))
          RawBlocks.block[CBLK] = corrupt_data
      else:
        RawBlocks.block[block_number] = bytearray(data.data)
    else:
        RawBlocks.block[block_number] = bytearray(data.data)
    try:
        #Checksum indexes
        csm = GetNewChecksum(data.data)
        RawBlocks.checksum_datastructure[block_number] = csm
    except Exception as e:
      print("Exception in put",e)
    return 0

  server.register_function(Put)
#RSM is not used in this implementation
  def RSM(block_number):
    result = RawBlocks.block[block_number]
    RawBlocks.block[block_number] = bytearray(RSM_LOCKED.ljust(BLOCK_SIZE,b'\x01'))
    return result

  server.register_function(RSM)
  # Run the server's main loop
  print ("Running block server with nb=" + str(TOTAL_NUM_BLOCKS) + ", bs=" + str(BLOCK_SIZE) + " on port " + str(PORT))
  server.serve_forever()

