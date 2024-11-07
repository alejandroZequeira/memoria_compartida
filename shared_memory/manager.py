import json
import metadata_extractor as me
import segmenter as seg
import shared_resources as sr
import worker as w
from multiprocessing import shared_memory, resource_tracker

segments_size = 1048576

# Carga los datos en memoria y retorna la metadata
def load_data(request):
    segments = {"segments": []}
    if request['context']['type'] == "local":
        data_control = get_metadata_and_segments(request)
        w.loadData(data_control['segments'])
    elif request['context']['type'] == "externo":
        print("Es externo")
    return data_control

# Carga la metadata, pone los datos en memoria y recupera los datos a partir de la metadata
def load_data_and_retrieve(request):
    response = load_data(request)
    files = []
    for r in response['metadata']['resources']:
        files.append([w.retrieveData(r['shm']), r])
    return files

# Recupera el recurso de la memoria
def retrieveData(shm):
    return w.retrieveData(shm)

# Se obtiene la metadata y los segmentos que componen los archivos
def get_metadata_and_segments(request):
    request['metadata'] = me.get_metadata(request['context']['path'])
    request['segments'] = []
    for f in request['metadata']['resources']:
        f['shm'] = sr.make_shm(f['size'])
        if f['size'] > segments_size:
            f['segmentation'] = "yes"
            f['chunk_size'] = segments_size
            request['segments'].append(seg.segmentation(f))
        else:
            f['segmentation'] = "no"
            f['chunk_size'] = f['size']
            request['segments'].append(seg.segmentation(f))
    request['segments'] = sum(request['segments'], [])
    return request

# Guarda el archivo en el sistema de archivos.
def saveFile(file, extension = ".txt"):
    w.saveFile(file, extension)
    return True

def remover(shmName):
	shm = shared_memory.SharedMemory(name = shmName, create = False)
	# resource_tracker.unregister(shm._name, 'shared_memory')
	shm.close()
	shm.unlink()
 
# Todavía no jala
def shareOnMemory(file):
    print("Compartir en memoria")
    return True

#if __name__ == '__main__':
    # Estructura base con la que se trabaja. Toda trabajo entrante
    # debe tener esta misma estructura. 
#   data = {
#        "context": {
#            "type": "local",
            # "path": "/home/julio/objects/one/f.txt"
            #"path": "/home/alejandro/documentos/clase/curso.rar"
#            "path": "/home/alejandro/documentos/clase/ultraman.mkv"
            
            # "path": "/home/julio/objects/TESIS.pdf"
#        }
#    }

    # *************    CARGAR DATOS EN MEMORIA Y RECURPERALOS ********************
    # Esta función obtiene la metadata de los recursos a partir de 
    # una ruta del sistema de archivos y los extrae para ponerlos
    # en una memoria compartida. Con la metadata resultante extrae
    # los archivos y los retorna como bytes. Retorna una arreglo.
    # Los arreglos se componen por un arreglo de dos elementos. El
    # primer elemento son los bytes y el segundo es la metadata del
    # archivo. 
#   response = load_data_and_retrieve(data)
#   print(response[0][1])
    # GUARDAR UN ARCHIVO A PARTIR DE LOS DATOS CARGADOS
    # La función saveFile recibe dos parametros. El primer parametro
    # son los bytes del archivo (obtenidos anteriormente) y el segundo
    # son es la extensión con la que se guardará el archivo.
    #print(response[0][1]["extension"])
#    saveFile(response[0][0], response[0][1]["extension"])


    # *****************     RECUPERAR LOS DATOS A PARTIR DE LA METADATA    ***********
    # 1 Obtener la metadata
    #ld = load_data(data)
    #resources = ld['metadata']['resources']
    #r = retrieveData("psm_aa9fd89d")
    #print(resources)
    #saveFile(r, ".zip")

    # print(response)
    # print("\nRESPONSE: \n", response)
    # for resources in
    # for r in response['metadata']['resources']:
    #     print(r)
    #     if(r['shm']):
    #         saveFile(shm = r['shm'])

    # print(response['metadata']['resources'], "\n")
    # print("\n", json.dumps(response))