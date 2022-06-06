from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from ublox_gps import UbloxGps
from datetime import datetime
import json
import time
import serial
import threading
import csv
import json



arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=.1)
port = serial.Serial('/dev/ttyACM0', baudrate=38400, timeout=1)
gps = UbloxGps(port)
# for positioning
csvHeader = ["Time", "Lat", "Long", "Height(in mm)", "Accuracy(in mm)"]
csvData = []
recordingPosition = False




class GetHandler(BaseHTTPRequestHandler):
    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        BaseHTTPRequestHandler.end_headers(self)
        
    def do_GET(self):
        parsed_path = urlparse(self.path); 
        print(parsed_path.query)
        message = responseMessage(parsed_path.query)
        self.send_response(responseCode(parsed_path.query))
        self.end_headers()
        queryProcess(parsed_path.query)

        self.wfile.write(message.encode())
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
                dt = datetime.now()
                pushInData  = [dt, geo.lat, geo.lon, geo.height, geo.hAcc]
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

def responseMessage(queryInput):
    query = queryInput.split("&")
    if('gps=latest' in query):
        return getLatestGPS()
    return ''

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
        exportToCsv()
        return 200
    except (ValueError, IOError) as err:
        return 500

def getLatestGPS(): 
    global csvData
    if(recordingPosition):
        lastPosition = csvData[-1]
        loc = {
            "lat": lastPosition[1],
            "long": lastPosition[2],
            "height": lastPosition[3],
            "accuracy": lastPosition[4]
        }
    else:
        geo = gps.geo_coords(); 
        loc = {
                "lat": geo.lat,
                "long": geo.lon,
                "height": geo.height,
                "accuracy": geo.hAcc
            }
    message = json.dumps(loc)
    return message
         

def exportToCsv():
    global csvData
    global csvHeader
    filename = '/home/admin/Desktop/result/'+str(datetime.now()) + '.csv'
    with open(filename, 'w', encoding='UTF8') as f:
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
    
    
