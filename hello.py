from urllib.parse import parse_qs

def app(environ, start_response):
    if environ['QUERY_STRING']:
        qs = parse_qs(environ['QUERY_STRING'])
        print('qs =', qs)
        data = b''
        for var in qs:
            for i in qs[var]:
                data += (str(var) + '=' + str(i) + '\n').encode('utf-8')
    headers = [('Content-Type', 'text/plain'), ('Content-Length', str(len(data)))]
    start_response('200 OK', headers)
    print('data to return:', data)
    return iter([data])

