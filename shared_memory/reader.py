import shared_resources as sr
from multiprocessing import shared_memory

path = "/home/julio/objects/one/f.txt"
# path = "/home/julio/objects"

res = sr.make_shm(path)

print(res)