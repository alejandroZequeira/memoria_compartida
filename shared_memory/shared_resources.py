from multiprocessing import shared_memory, resource_tracker
import metadata_extractor

def make_shm(size):
    remove_shm_from_resource_tracker()
    shm = shared_memory.SharedMemory(create = True, size = size)
    shm.close()
    # metadata['shm'] = shm.name
    # res = metadata_extractor.get_metadata(path)
    # if res['type'] == 'archivo':
    #     shm = shared_memory.SharedMemory(create = True, size = res['resources'][0]['size'])
    #     shm.close()
    #     res['data'][0]['shm'] = shm.name
    # elif res['type'] == 'directorio':
    #     for file in res['resources']:
    #         shm = shared_memory.SharedMemory(create = True, size = file['size'])
    #         shm.close()
    #         file['shm'] = shm.name
    return shm.name

def remove_shm(shm_name):
	shm = shared_memory.SharedMemory(name = shm_name, create = False)
	# resource_tracker.unregister(shm._name, 'shared_memory')
	shm.close()
	shm.unlink()

def remove_shm_from_resource_tracker():
    """Monkey-patch multiprocessing.resource_tracker so SharedMemory won't be tracked

    More details at: https://bugs.python.org/issue38119
    """

    def fix_register(name, rtype):
        if rtype == "shared_memory":
            return
        return resource_tracker._resource_tracker.register(self, name, rtype)
    resource_tracker.register = fix_register

    def fix_unregister(name, rtype):
        if rtype == "shared_memory":
            return
        return resource_tracker._resource_tracker.unregister(self, name, rtype)
    resource_tracker.unregister = fix_unregister

    if "shared_memory" in resource_tracker._CLEANUP_FUNCS:
        del resource_tracker._CLEANUP_FUNCS["shared_memory"]

# if __name__ == '__main__':
    # response = make_shm("/home/julio/objects/one/f.txt")
    # response = make_shm("/home/julio/objects")
    # print(response)