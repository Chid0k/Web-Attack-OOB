import re
import os 
import json

def parse_log_block(text):
    blocks = {}
    block_id = None
    current_key = None
    buffer = []

    for line in text.splitlines():
        m = re.match(r"--([0-9a-z]+)-([A-Z])--", line)
        if m:
            if current_key and buffer:
                blocks[current_key] = "\n".join(buffer).strip()
                buffer = []
            block_id, key = m.groups()
            if key == "Z":
                break
            current_key = key
        else:
            buffer.append(line)

    if current_key and buffer:
        blocks[current_key] = "\n".join(buffer).strip()

    return {"id": block_id, **blocks}

def parse_block_A(line: str) -> dict:
    regex = re.compile(
        r'^\[(?P<time>[^\]]+)\]\s+'             # Thời gian
        r'(?P<transaction_id>[^\s]+)\s+'        # Transaction ID
        r'(?P<client_ip>\d+\.\d+\.\d+\.\d+)\s+' # Client IP
        r'(?P<client_port>\d+)\s+'              # Client Port
        r'(?P<server_ip>\d+\.\d+\.\d+\.\d+)\s+' # Server IP
        r'(?P<server_port>\d+)$'                # Server Port
    )

    match = regex.match(line.strip())
    if not match:
        return {}

    return {
        "time": match.group("time"),
        "transaction_id": match.group("transaction_id"),
        "client_ip": match.group("client_ip"),
        "client_port": int(match.group("client_port"))
    }

def capture_log(file_path_log, uuid):
    if not os.path.exists(file_path_log):
        return []

    if re.match(r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}', uuid):
        cmd = r"""awk '
/--[0-9a-zA-Z]+-A--/ {{ block=""; flag=1 }}
flag {{ block = block $0 ORS }}
/--[0-9a-zA-Z]+-Z--/ {{
    if (block ~ /{uuid}/) print block
    flag=0
}}' {file_path_log}""".format(uuid=uuid, file_path_log=file_path_log)

        logs = os.popen(cmd).read().strip().split('-Z--\n')
        logs = [parse_log_block(i + '-Z--') for i in logs if i.strip()]
        for i in logs:
            if 'A' in i:
                i.update(parse_block_A(i['A']))
                i.pop('A')
        return logs[::-1]
        
    else:
        return []
