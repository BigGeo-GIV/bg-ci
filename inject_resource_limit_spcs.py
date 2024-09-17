import sys

file_path = sys.argv[1]

cp_resources = [
    { "size": 'XS','cpu': 1, 'memory': '6Gi' },
    { "size": 'S', 'cpu': 3, 'memory': '13Gi' },
    { "size": 'M', 'cpu': 6, 'memory': '28Gi' },
    { "size": 'L', 'cpu': 28, 'memory': '116Gi' },
    { "size": 'HMS','cpu': 6, 'memory': '58Gi' },
    { "size": 'HMM','cpu': 28, 'memory': '240Gi' },
    { "size": 'HML','cpu': 124, 'memory': '984Gi' },
    { "size": 'GPUS','cpu': 6, 'memory': '27Gi' },
    { "size": 'GPUM','cpu': 44, 'memory': '178Gi' },
    { "size": 'GPUL','cpu': 92, 'memory': '112Gi' }
]

with open(file_path, 'r') as file:
    filedata = file.read()

for cp in cp_resources:
    content = filedata.replace('<resource_place_holder>', 
f'''resources:
        requests:
          cpu: 0.1
          memory: 1Gi
        limits:
          cpu: {cp['cpu']}
          memory: {cp['memory']}''')
    size = cp['size']
    with open(f'biggeo-{size}.yaml', 'w') as file:
        file.write(content)
