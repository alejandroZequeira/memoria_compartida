from multiprocessing import shared_memory, resource_tracker, Pool
import uuid

def loadData(md):
    for segment in md:
        # print("SEGMENTO: ", segment, "\n")
        # SE ABRE EL SEGMENTO DE MEMORIA.
        shm = shared_memory.SharedMemory(name = segment['shm'], create=False)
		# ABRE EL ARCHIVO ORIGINAL COMO BINARIO.
        with open(segment['file'], mode = "rb") as file:
            # SE POSICIONA EN EL LUGAR DE LECTURA INICIAL.
            file.seek(segment['start_position'])
			# AGREGA DATOS AL BUFFER DE MEMORIA.
            shm.buf[segment['start_position']:segment['end_position']] = file.read(segment['chunk_size'])
            # print("BUFFER: ", bytes(shm.buf[:]).decode(), "\n")
				# print("*"*200, bytes(shm.buf[x['start_position']:x['end_position']]).decode())
        # SE CIERRA EL SEGMENTO DE MEMORIA
        shm.close()
    return True

def saveFile(file, extension):
    with open(f"files/{uuid.uuid4()}{extension}", "wb") as nf:
        nf.write(file)
    # shm.close()
    # shm = shared_memory.SharedMemory(name = md['shm'], create=False)
    # with open("latesis.pdf", "wb") as file:
    #     file.write(bytes(shm.buf[:]))
    # shm.close()
    return True

def retrieveData(m):
    shm = shared_memory.SharedMemory(name = m, create=False)
    file = bytes(shm.buf[:])
    shm.close()
    return file