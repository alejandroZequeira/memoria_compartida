import json
import metadata_extractor as me

def to_segment(data):
    if (data['segmentation'] == "yes"):
        metadata = me.get_metadata(data['path'])
        # print("metadata: ", metadata)
        data['metadata'] = metadata
        if metadata['type'] == "archivo":
            res_positions = positions(metadata['resources'][0]['size'], metadata['resources'][0]['file'], data['segments_size'], "default file")
            data['metadata']['resources'][0]['positions'] = res_positions
        elif metadata['type'] == "directorio":
            for p in range(len(data)):
                res_positions = positions(data['metadata']['resources'][p]['size'], data['metadata']['resources'][p]['file'], data['segments_size'], "default dir")
                data['metadata']['resources'][p]['positions'] = res_positions            
    elif(data['segmentation'] == "no"):
        print("nel")
    return data

def segmentation(metadata):
    # p = positions(metadata['size'], metadata['file'], metadata['chunk_size'], metadata['shm'])
    # # metadata['positions'] = p
    position = 0
    chunk = metadata['chunk_size']
    file_size = metadata['size']
    positions = []
    while position < file_size:
        end_position = position + chunk if ((position + chunk) < file_size) else position + (file_size - position)
        positions.append({
                "file": metadata['path'],  
                "shm": metadata['shm'],
                "chunk_size": metadata['chunk_size'],
                "start_position": position, 
                "end_position": end_position
            })
        position = position + chunk
    return positions

def positions(file_size, path, chunk_size, shm):
	position = 0
	chunk = chunk_size
	positions = []
	while position < file_size:
		end_position = position + chunk if ((position + chunk) < file_size) else position + (file_size - position)
		positions.append({"start_position": position, "end_position": end_position, "shm": shm})
		position = position + chunk
	return positions


if __name__ == '__main__':
    # response = make_shm("/home/julio/objects/one/f.txt")
    # data = {
    #     "segmentation": "no",
    #     "path": "/home/julio/objects/one/f.txt"
    # }
    data = {
        "segmentation": "yes",
        "segments_size": 1048576,
        # "path": "/home/julio/objects"
        "path": "/home/julio/objects/TESIS.pdf"
    }
    response = to_segment(data)
    print(json.dumps(response))