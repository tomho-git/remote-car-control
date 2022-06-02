from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from ublox_gps import UbloxGps
import json
import time
import serial
import threading
import csv


arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=.1)
port = serial.Serial('/dev/ttyACM0', baudrate=38400, timeout=1)
gps = UbloxGps(port)
# for positioning
csvHeader = ["Lat", "Long", "Height(in mm)", "Accuracy(in mm)"]
csvData = []
recordingPosition = False




class GetHandler(BaseHTTPRequestHandler):
    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        BaseHTTPRequestHandler.end_headers(self)
        
    def do_GET(self):
        parsed_path = urlparse(self.path); 
        print(parsed_path.query)
        # message = '\n'.join([
        #     'CLIENT VALUES:',
        #     'client_address=%s (%s)' % (self.client_address,
        #         self.address_string()),
        #     'command=%s' % self.command,
        #     'path=%s' % self.path,
        #     'real path=%s' % parsed_path.path,
        #     'query=%s' % parsed_path.query,
        #     'request_version=%s' % self.request_version,
        #     '',
        #     'SERVER VALUES:',
        #     'server_version=%s' % self.server_version,
        #     'sys_version=%s' % self.sys_version,
        #     'protocol_version=%s' % self.protocol_version,
        #     '',
        #     ])
        self.send_response(responseCode(parsed_path.query))
        self.end_headers()
        queryProcess(parsed_path.query)


        # self.wfile.write(message)
        return

    def do_POST(self):
        content_len = int(self.headers.getheader('content-length'))
        post_body = self.rfile.read(content_len)
        self.send_response(200)
        self.end_headers()

        data = json.loads(post_body)

        self.wfile.write(data['foo'])
        return

def write_read_arduino(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data

def queryProcess(queryInput):
    if(queryInput == ""):
        return
    else:
        query = queryInput.split("&")
        if("car=forward" in query):
            write_read_arduino("W")
        elif("car=backward" in query):
            write_read_arduino("S")
        elif("car=anticlockwise" in query):
            write_read_arduino("Q")
        elif("car=clockwise" in query):
            write_read_arduino("E")
        elif("car=stop" in query):
            write_read_arduino("X")
        return

def gpsRecordingSubProgram():
    global csvData
    global recordingPosition
    while True:
        if(recordingPosition):
            try:
                geo = gps.geo_coords()
                pushInData  = [geo.lat, geo.lon, geo.height, geo.hAcc]
                csvData.append(pushInData)
                print(csvData)
            except (ValueError, IOError) as err:
                        print(err)
        else:
            time.sleep(0.5)

def responseCode(queryInput):
    query = queryInput.split("&")
    if("gps=start" in query):
        return startGps()
    elif("gps=end" in query):
        return endGps()
    return 200


def startGps(): 
    try:
        global csvData
        global recordingPosition
        csvData = []
        recordingPosition = True
        return 200
    except (ValueError, IOError) as err:
        return 500
    
    

def endGps():
    try:
        global recordingPosition
        recordingPosition = False
        exportCsv()
        return 200
    except (ValueError, IOError) as err:
        return 500

def exportCsv():
    global csvData
    global csvHeader
    with open('result.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(csvHeader)
        writer.writerows(csvData)


if __name__ == '__main__':
    server = HTTPServer(('192.168.4.1', 8080), GetHandler)
    print ('Starting server at http://192.168.4.1:8080')
    p1 = threading.Thread(target = gpsRecordingSubProgram)
    p1.start()
    p2 = threading.Thread(target = server.serve_forever)
    p2.start()
    
    
