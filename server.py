import sys; # used to get argv
import cgi; # used to parse Mutlipart FormData          # this should be replace with multipart in the future
import os;
import glob;
import Physics;
import math;
import random;
import json

# web server parts
from http.server import HTTPServer, BaseHTTPRequestHandler;

# used to parse the URL and extract form data for GET requests
from urllib.parse import urlparse, parse_qsl;


# handler for our web-server - handles both GET and POST requests
class MyHandler( BaseHTTPRequestHandler ):

    def do_GET(self):
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path );

        # check if the web-pages matches the list
        if parsed.path in [ '/index.html' ]:

            # retreive the HTML file
            fp = open( '.'+self.path );
            content = fp.read();

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            # send it to the broswer
            self.wfile.write( bytes( content, "utf-8" ) );
            fp.close();

        elif parsed.path.endswith('.svg') and parsed.path.startswith('/table-'):
            # Dynamically handle SVG files without hardcoding the file name
            try:
                with open('.' + parsed.path, 'rb') as fp:  # Open the file in binary mode
                    content = fp.read()
                self.send_response(200)
                self.send_header("Content-type", "image/svg+xml")  # Set the correct content type for SVG files
                self.send_header("Content-length", len(content))
                self.end_headers()
                self.wfile.write(content)

            except IOError:
                # File not found, return 404
                self.send_response(404)
                self.end_headers()
                self.wfile.write(bytes("404: File not found %s" % parsed.path, "utf-8"))

        # check if the web-pages matches the list
        else:
            # generate 404 for GET requests that aren't the 2 files above
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );

    def do_POST(self):

        p1 = "default_player1_name"  # Default player names
        p2 = "default_player2_name"
        table = createNewTable()
        game = Physics.Game(gameName="Game 01", player1Name=p1, player2Name=p2) 
        db = Physics.Database()

        if self.path == "/handle_names":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            # Extract player names if available
            p1 = data.get('player1')
            p2 = data.get('player2')

            # Update player names of the existing game object
            if p1 is not None and p2 is not None:
                print("Player 1:", p1)
                print("Player 2:", p2)

                game.update(p1,p2)

                # Send success response for receiving player names
                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(bytes("Received player names successfully!", "utf-8"))

        elif self.path == "/handle_mouse_position":

            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            vx = data.get('vx')
            vy = data.get('vy')

            if vx is not None and vy is not None:
                print("vx:", vx)
                print("vy:", vy)

                tableID = db.getLastTableID() or 0

                game.shoot("Game 01", p1, table, vx, vy)

                svgs = []
                table = db.readTable(tableID)

                while table is not None:
                    svgdata = table.svg()
                    svgs.append(svgdata)     
                    tableID += 1
                    table = db.readTable(tableID)

                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                response_json = json.dumps(svgs)
                self.wfile.write(response_json.encode('utf-8'))

        else:
            print("Invalid path:", self.path)
            self.send_response(400)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes("Invalid path: " + self.path, "utf-8"))

def nudge():
    return random.uniform( -1.5, 1.5 );

def createNewTable():
    table = Physics.Table()

    # Define the positions of the balls from the SVG
    ball_positions = [
        (675, 2025),  # Cue ball
        (675, 675),   # Apex ball
        (615, 630),   # Second row
        (735, 630),
        (555, 585),   # Third row
        (675, 585),
        (795, 585),
        (495, 540),   # Fourth row
        (615, 540),
        (735, 540),
        (855, 540)
        # Add more rows as needed
    ]

    for ball_id, (x, y) in enumerate(ball_positions, start=0):
        pos = Physics.Coordinate(x, y)
        sb = Physics.StillBall(ball_id, pos)
        table += sb

    return table


def createNewTableAndSave():
    # Generate the table
    table = createNewTable()


if __name__ == "__main__":
    createNewTableAndSave()
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler );
    print( "Server listing in port:  ", int(sys.argv[1]) );
    httpd.serve_forever();