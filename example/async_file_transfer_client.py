import asyncio
import aiofiles
import traceback
import sys

HOST = 'localhost'
PORT = 9999

#   ===================================================================


async def client(filename, loop)->bool:
    data_transferred = 0
    data = None

    try:
        reader, writer = await asyncio.open_connection(HOST, PORT, loop=loop)
        filename = filename.encode()
        writer.write(filename)
        data = await reader.read(1024)

    except asyncio.CancelledError:
        print(getTracebackStr())
        return False

    if not data:
        print(getTracebackStr())
        return False

    try:
        async with aiofiles.open(filename, mode='wb') as f:
            while data:
                f.write(data)
                data_transferred += len(data)
                data = await reader.read(1024)
    except Exception as e:
        print(getTracebackStr())
        return False

    print('파일[%s] 전송종료. 전송량 [%d]' % (filename, data_transferred))
    return True

#   ===================================================================


def run_client():
    print("다운로드 받은 파일이름을 입력하세요:", end="")
    filename = input()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client(filename, loop))
    loop.run_forever()

def getTracebackStr():
    xrange = range
    lines = traceback.format_exc().strip().split('\n')
    rl = [lines[-1]]
    lines = lines[1:-1]
    lines.reverse()
    for i in xrange(0,len(lines),2):
        rl.append('^\t%s at %s' % (lines[i].strip(),lines[i+1].strip()))
    return '\n'.join(rl)



run_client()