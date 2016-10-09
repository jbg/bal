from __future__ import print_function

__version__ = "0.1.5"

import argparse
import binascii
from decimal import Decimal
import sys

import dns.resolver


alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
if bytes == str:  # python2
  iseq = lambda s: map(ord, s)
  bseq = lambda s: ''.join(map(chr, s))
  buffer = lambda s: s
else:  # python3
  iseq = lambda s: s
  bseq = bytes
  buffer = lambda s: s.buffer

def b58decode(v):
  if not isinstance(v, str):
    v = v.decode('ascii')
  origlen = len(v)
  v = v.lstrip(alphabet[0])
  newlen = len(v)
  p, acc = 1, 0
  for c in v[::-1]:
    acc += p * alphabet.index(c)
    p *= 58
  result = []
  while acc > 0:
    acc, mod = divmod(acc, 256)
    result.append(mod)
  return (bseq(result) + b'\0' * (origlen - newlen))[::-1]

def main():
  parser = argparse.ArgumentParser(epilog="If no addresses are provided on the command line, newline-delimited addresses are read from stdin.")
  parser.add_argument("addresses", metavar="address", type=str, nargs="*", help="base58check-encoded Bitcoin address")
  parser.add_argument("-s", "--satoshis", action="store_true", default=False, help="report the balance in satoshis rather than bitcoins")
  args = parser.parse_args()

  if not args.addresses:
    args.addresses = (line.strip() for line in sys.stdin)

  seen = set()
  resolver = dns.resolver.Resolver()
  resolver.timeout = 4.0
  resolver.lifetime = 4.0

  for address in args.addresses:
    if address not in seen:
      seen.add(address)
      if not hasattr(args.addresses, "__len__") or len(args.addresses) > 1:
        print(address, end=': ')
      try:
        hex_encoded = binascii.hexlify(b58decode(address))
      except:
        print("invalid")
      else:
        try:
          record = resolver.query(hex_encoded.decode("ascii") + ".bal.dnscoin.nz", "TXT").response.answer[0]
        except Exception as e:
          print("failed: %s" % e)
        else:
          balance = record.items[0].strings[0].decode("ascii")
          if not args.satoshis:
            balance = format(Decimal(balance) / Decimal("100000000"), "f")
          print(balance)
