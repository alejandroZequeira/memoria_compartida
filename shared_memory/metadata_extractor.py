import os
import json

def get_metadata(res):
    type = None
    data = []
    if (os.path.isdir(res)):
        data = dirs(res)
        type = "directorio"
    elif (os.path.isfile(res)):
        data.append(files(res))
        type = "archivo"
    else:
        print("Entrada inválida")
    return { "type": type, "resources": data}

def files(res):
    return {'path': res, 'size': os.path.getsize(res), 'extension': os.path.splitext(res)[1] }

def dirs(res):
    list_metadata = []
    for element in os.listdir(res):
        if os.path.isdir(res + '/' + element):
            list_metadata = list_metadata + dirs(res + '/' + element)
        elif os.path.isfile(res + '/' + element):
            list_metadata.append(files(f"{res}/{element}"))
    return list_metadata



if __name__ == '__main__':
    response = get_metadata("/home/julio/objects")
    # response = metadata_extractor("/home/julio/objects/one/f.txt")
    # response = dirs("/home/julio/objects")
    # print()
    print(json.dumps(response))