import multiprocessing as mp
from multiprocessing.shared_memory import SharedMemory
import time

# shm = SharedMemory(create = True, )
dorkdir = ""
def read_from_disk_to_memory(res):
    with open(f"/dev/shm/{res['filename']}", mode = "wb") as file_workdir:
    # with open(f"/home/julio/sd/f/{res['filename']}", mode = "wb") as file_workdir:
        with open(res['file'], mode = "rb") as file:
            data = file.read(res['size'])
            # file_workdir.write(data)
            print(data.decode('utf-8'))


if __name__ == '__main__':
    # response = metadata_extractor("/home/julio/objects")
    # response = read_from_disk_to_memory("/home/julio/objects/one/one.txt")
    # response = dirs("/home/julio/objects")
    # print()
    start = time.time()
    mo = {
        'filename': 'f.txt',
        'size': 16,
        'file': '/home/julio/objects/one/f.txt'
    }
    read_from_disk_to_memory(mo)
    end = time.time()
    exec_time = end - start;
    print("Tiempo de ejecución: ", exec_time)


