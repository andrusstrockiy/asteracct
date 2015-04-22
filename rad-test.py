import pyrad.packet
from pyrad.client import Client
from pyrad.dictionary import Dictionary

srv = Client(server="192.168.6.254", secret="secret",
             dict=Dictionary("dicts/dictionary", "dictionary.acc"))

req = srv.CreateAuthPacket(code=pyrad.packet.AccessRequest, User_Name="wichert", NAS_Identifier="127.0.0.1")

req["User-Password"] = req.PwCrypt("password")

reply = srv.SendPacket(req)
if reply.code == pyrad.packet.AccessAccept:
    print("access accepted")
else:
    print("access denied")

print("Attributes returned by server:")

for i in reply.keys():
    print("%s: %s") % (i, reply[i])