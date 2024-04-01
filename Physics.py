import phylib;
import sqlite3;
import Physics;
################################################################################
#Declare svg constants
HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";
FOOTER = """</svg>\n""";

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER;
HOLE_RADIUS =  phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH;
SIM_RATE = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON;
FRAME_INTERVAL = 0.01;
DRAG = phylib.PHYLIB_DRAG;
MAX_TIME = phylib.PHYLIB_MAX_TIME;
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS;

# add more here

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;

    def svg( self ):
        return """<circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (
            self.obj.still_ball.pos.x,
            self.obj.still_ball.pos.y,
            BALL_RADIUS,
            BALL_COLOURS[self.obj.still_ball.number % len(BALL_COLOURS)]
        )

################################################################################

class RollingBall(phylib.phylib_object):
    """"
    Python RollingBall Class
    """

    def __init__(self, number, pos, vel, acc):

        #this creates a generic phylib object
        phylib.phylib_object.__init__(self,
                                      phylib.PHYLIB_ROLLING_BALL,
                                      number,
                                      pos, vel, acc,
                                      0.0, 0.0);

        # this converts the phylib_object into a RollingBall class
        self.__class__ = RollingBall;

    def svg(self):
        return """<circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (
            self.obj.rolling_ball.pos.x,
            self.obj.rolling_ball.pos.y,
            BALL_RADIUS,
            BALL_COLOURS[self.obj.rolling_ball.number % len(BALL_COLOURS)]
        )


################################################################################

class Hole(phylib.phylib_object):

    def __init__(self, pos):

        #this creates a generic object type
        phylib.phylib_object.__init__(self,
                                    phylib.PHYLIB_HOLE,
                                    0,
                                    pos, None, None,
                                    0.0, 0.0);

        #this converts the phylib object into a Hole class
        self.__class__ = Hole;

    def svg(self):
        return """<circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % (
            self.obj.hole.pos.x,
            self.obj.hole.pos.y,
            HOLE_RADIUS,
        )


################################################################################

class HCushion(phylib.phylib_object):

    def __init__(self, y):

        #this creates a generic object type
        phylib.phylib_object.__init__(self,
                                    phylib.PHYLIB_HCUSHION,
                                    0,
                                    None, None, None,
                                    0.0, y);

        #this converts the phylib object into a HCushion class
        self.__class__ = HCushion;

    def svg(self):
        y_value = -25 if self.obj.hcushion.y == 0 else 2700
        return """<rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (
            y_value
        )


################################################################################

class VCushion(phylib.phylib_object):

    def __init__(self, x):

            #this creates a generic object type
        phylib.phylib_object.__init__(self,
                                    phylib.PHYLIB_VCUSHION,
                                    0,
                                    None, None, None,
                                    x, 0.0);

            #This convers the phylib object into a VCushion class
        self.__class__ = VCushion;

    def svg(self):
        x_value = -25 if self.obj.vcushion.x == 0 else 1350
        return """<rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (
            x_value
        )

################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        self.current = -1
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    # add svg method here
    # Implement the svg method
    def svg(self):
        svg_elements = []

        # Iterate over each object in the table
        for obj in self:
            if obj is not None:
                # Call the svg method of the object and add the result to the list
                svg_elements.append(obj.svg())

        # Concatenate HEADER, the SVG elements, and FOOTER to form the complete SVG
        return HEADER + "\n" + "".join(svg_elements) + FOOTER

    def roll( self , t ):
        new = Table()
        for ball in self:
            if isinstance(ball, RollingBall):
                #created a new ball with the same number as the old ball
                new_ball = RollingBall(ball.obj.rolling_ball.number,
                                        Coordinate(0,0),
                                        Coordinate(0,0),
                                        Coordinate(0,0))
                #compute where it rolls to
                phylib.phylib_roll(new_ball,ball,t)

                #add ball to table
                new += new_ball
            
            if isinstance(ball, StillBall):
                #create a new ball with the same number and pos as the old ball
                new_ball = StillBall(ball.obj.still_ball.number,
                                    Coordinate(ball.obj.still_ball.pos.x,
                                    ball.obj.still_ball.pos.y));
                #add ball to the table
                new += new_ball
        #return table
        return new

    def cueBall(self, table, xvel, yvel):

        """
        Set up the cue ball with the specified initial velocities.

        Parameters:
        - table: The current table state.
        - xvel: Initial velocity in the x-direction.
        - yvel: Initial velocity in the y-direction.

        Returns:
        - The modified cue ball.
        """

        for obj in table:
             # Check if the object is a StillBall or RollingBall and has the number 0 (cue ball)
            if isinstance(obj, (StillBall, RollingBall)) and obj.obj.still_ball.number == 0:

                    # Set the type to RollingBall
                obj.type = phylib.PHYLIB_ROLLING_BALL

                # Extract position coordinates of the rolling ball
                posx = obj.obj.rolling_ball.pos.x
                posy = obj.obj.rolling_ball.pos.y

                # Set the velocities of the rolling ball
                velx = xvel
                vely = yvel               
                                        
                    # Update the velocities of the rolling ball
                obj.obj.rolling_ball.vel.x = velx
                obj.obj.rolling_ball.vel.y = vely

                # Calculate the speed and create a Coordinate for the ball velocity
                ball_vel = Physics.Coordinate(velx,vely)
                speed = phylib.phylib_length(ball_vel)

                # Initialize acceleration components
                accx = 0.0
                accy = 0.0

                # Check if the ball has a non-zero speed to avoid division by zero
                if(speed > VEL_EPSILON):
                    # Calculate drag acceleration components based on velocity
                    accx = -(velx / speed) * DRAG
                    accy = -(vely / speed) * DRAG
                
                # Update the acceleration components of the rolling ball
                obj.obj.rolling_ball.acc.x = accx
                obj.obj.rolling_ball.acc.y = accy

                    # Return the modified cue ball
                return obj
   
class Database():

    def __init__ (self, reset = False):
        #If reset is true, delete the database
        if reset and os.path.exists("phylib.db"):
            os.remove("phylib.db")

        self.createConnection()
        

    def createConnection(self):
          # Call the connect method to establish the database connection
        self.conn = sqlite3.connect("phylib.db")
        # Ensure the database schema is set up
        self.cursor = self.conn.cursor()

    def createDB( self ):
        self.createConnection()
        #Create the tables here
        """Initialize the database and create necessary tables"""
        create_tables =[
            """
        CREATE TABLE IF NOT EXISTS Ball (
            BALLID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            BALLNO INTEGER NOT NULL,
            XPOS FLOAT NOT NULL,
            YPOS FLOAT NOT NULL,
            XVEL FLOAT,
            YVEL FLOAT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS TTable(
            TABLEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            TIME FLOAT NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS BallTable(
            BALLID INTEGER NOT NULL,
            TABLEID INTEGER NOT NULL,
            FOREIGN KEY(BALLID) REFERENCES Ball(BALLID),
            FOREIGN KEY(TABLEID) REFERENCES TTable(TABLEID)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Shot(
            SHOTID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            PLAYERID INTEGER NOT NULL,
            GAMEID INTEGER NOT NULL,
            FOREIGN KEY(PLAYERID) REFERENCES Player(PLAYERID),
            FOREIGN KEY(GAMEID) REFERENCES Game(GAMEID)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS TableShot(
            TABLEID INTEGER NOT NULL,
            SHOTID INTEGER NOT NULL,
            FOREIGN KEY(TABLEID) REFERENCES TTable(TABLEID),
            FOREIGN KEY(SHOTID) REFERENCES Shot(SHOTID)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Game(
            GAMEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            GAMENAME VARCHAR(64) NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Player(
            PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            GAMEID INTEGER NOT NULL,
            PLAYERNAME VARCHAR(64) NOT NULL,
            FOREIGN KEY(GAMEID) REFERENCES Game(GAMEID)
        );
        """
        ]

        for table in create_tables:
            self.cursor.execute(table)
        
        self.close()

    def readTable(self, myTableID):
        # Create database connection
        self.createConnection()

        #Initialize a table object
        table = Table()

        try:
             # Fetch time for the given table ID from the TTable table
            self.cursor.execute("""
                SELECT TIME FROM TTable
                WHERE TABLEID = ?;
            """, (myTableID + 1,))
            result = self.cursor.fetchone()

            # Check if the result is not None, indicating a valid time entry
            if result is not None:
                table.time = result[0]
            else:
                 # Return None if no time entry is found for the given table ID
                return None

            # Fetch ball information for the given table ID from the Ball and BallTable tables
            self.cursor.execute("""
                SELECT Ball.BALLID, Ball.BALLNO, Ball.XPOS, Ball.YPOS, Ball.XVEL, Ball.YVEL
                FROM Ball
                INNER JOIN BallTable ON Ball.BALLID = BallTable.BALLID
                WHERE BallTable.TABLEID = ?;
            """, (myTableID + 1,))
            rows = self.cursor.fetchall()

            # Check if no rows are retrieved, indicating an empty table
            if not rows:
                return None
        
             # Process retrieved ball information
            for row in rows:
                ball_id, ball_number, xpos, ypos, xvel, yvel = row

                pos = Coordinate(xpos, ypos)  # Create a Coordinate object representing the position of the ball
                if xvel is None and yvel is None:  # Check if the ball is not moving (zero velocity)
                    # Create a StillBall object if the ball is not moving
                    ball = StillBall(ball_number, pos)
                else:
                    vel = Coordinate(xvel, yvel)
                    speed = phylib.phylib_length(vel)
                    accx = 0.0
                    accy = 0.0  # Calculate the speed of the ball
                    if speed > VEL_EPSILON: # Calculate drag acceleration if the speed is above a threshold
                        accx = -(vel.x / speed) * DRAG
                        accy = -(vel.y / speed) * DRAG
                    acc = Coordinate(accx, accy)

                    if vel.x == 0.0 and vel.y == 0.0:   
                        # Check if the ball has zero velocity
                        ball = StillBall(ball_number, pos)
                    else:
                         # Create a RollingBall object if the ball has velocity and acceleration
                        ball = RollingBall(ball_number, pos, vel, acc)

                 # Add the ball to the table
                table += ball

            # Commit the changes to the database
            self.conn.commit()

             # Return the populated table
            return table

        except sqlite3.Error as e:
            #return none when error 
            return None


    def writeTable(self, table):
        # Create a database connection
        self.createConnection()
        try:
             # Insert the time information into the TTable table
            self.cursor.execute('''
                INSERT INTO TTable (TIME) VALUES (?);
            ''', (table.time,))

            # Get the last inserted row ID for the TTable table
            table_id = self.cursor.lastrowid - 1

             # Iterate through each object in the table
            for obj in table:
                if isinstance(obj, RollingBall):
                     # Extract information for a RollingBall
                    ball_number = obj.obj.rolling_ball.number
                    x_pos = obj.obj.rolling_ball.pos.x
                    y_pos = obj.obj.rolling_ball.pos.y
                    x_vel = obj.obj.rolling_ball.vel.x
                    y_vel = obj.obj.rolling_ball.vel.y
                elif isinstance(obj, StillBall):
                     # Extract information for a StillBall
                    ball_number = obj.obj.still_ball.number
                    x_pos = obj.obj.still_ball.pos.x
                    y_pos = obj.obj.still_ball.pos.y
                    x_vel = 0
                    y_vel = 0

                else:
                     # Skip
                    continue

                # Insert or ignore ball information into the Ball table
                self.cursor.execute('''
                    INSERT OR IGNORE INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (?, ?, ?, ?, ?);
                ''', (ball_number, x_pos, y_pos, x_vel, y_vel))

                # Get the last inserted row ID for the Ball table
                ball_id = self.cursor.lastrowid


                  # Insert data into the BallTable table linking the ball and the table
                self.cursor.execute('''
                    INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?);
                ''', (ball_id, table_id + 1))

            # Commit the changes to the database
            self.conn.commit()

             # Return the ID of the inserted table
            return table_id

        except sqlite3.Error as e:
            #Handle errors
            return None

    def close(self):
        self.conn.commit()
        self.cursor.close()  #Close the connection and commit the changes
        self.conn.close()

    def getGame(self, gameID):
        # SQL query to retrieve game information and player names
        query = """
            SELECT G.GAMEID, G.GAMENAME, P1.PLAYERNAME, P2.PLAYERNAME
            FROM Game G
            JOIN Player P1 ON G.GAMEID = P1.GAMEID AND P1.PLAYERID = (SELECT MIN(PLAYERID) FROM Player WHERE GAMEID = G.GAMEID)
            JOIN Player P2 ON G.GAMEID = P2.GAMEID AND P2.PLAYERID = (SELECT MAX(PLAYERID) FROM Player WHERE GAMEID = G.GAMEID)
            WHERE G.GAMEID = ?
        """
        # Execute the SQL query with the provided gameID parameter
        self.cursor.execute(query, (gameID,))
        
        # Fetch the first row of the result
        result = self.cursor.fetchone()
        
         #Check if a result is obtained
        if result:
            return result  # Unpack the result tuple and prepend gameID
        else:
            # Return None if no result is found
            return None

    def setGame(self, gameName, player1Name, player2Name):

        try:          
            # Insert gamename and ID into Game Table
            self.cursor.execute('''
                INSERT INTO Game (GAMENAME) VALUES (?)
            ''', ( gameName,))

            # Get the last inserted row ID for the Game Table
            gameID = self.cursor.lastrowid

            # Insert player1Name into the Player Table
            self.cursor.execute('''
                INSERT INTO Player (PLAYERNAME, GAMEID) VALUES (?,?);
            ''', (player1Name,gameID,))

             # Get the last inserted row ID for player1
            player1ID = self.cursor.lastrowid

            # Insert player2Name into the Player Table
            self.cursor.execute('''
                INSERT INTO Player (PLAYERNAME, GAMEID) VALUES (?, ?);
            ''', (player2Name,gameID,))

             # Get the last inserted row ID for player2
            player2ID = self.cursor.lastrowid
            
            # Commit the changes 
            self.conn.commit()

            return gameID

        except sqlite3.Error as e:
            return None

    def updatePlayers(self, newPlayer1Name, newPlayer2Name):
        """
        This method updates the player names in the database.
        """
        try:
            # Update player1Name
            self.cursor.execute('''
                UPDATE Player 
                SET PLAYERNAME = ?
                WHERE PLAYERNAME = ?;
            ''', (newPlayer1Name, 'default_player1_name'))

            # Update player2Name
            self.cursor.execute('''
                UPDATE Player 
                SET PLAYERNAME = ?
                WHERE PLAYERNAME = ?;
            ''', (newPlayer2Name, 'default_player2_name'))

            # Commit the changes
            print("names updated")
            self.conn.commit()

        except sqlite3.Error as e:
            print(f"Error updating player names: {e}")
            raise

    def getLastGameID(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT MAX(GAMEID) FROM Game")
        last_game_id = cursor.fetchone()[0]
        cursor.close()
        self.conn.commit()
        return last_game_id

    def getLastTableID(self):
            cursor = self.conn.cursor()
            cursor.execute("SELECT MAX(TABLEID) FROM TTable")
            last_table_id = cursor.fetchone()[0]
            cursor.close()
            self.conn.commit()
            return last_table_id

    def getTableID(self, table):
            cursor = self.conn.cursor()
            cursor.execute("SELECT ")

    def newShot(self, gameName, playerName):
        # Find the gameID based on gameName
        self.cursor.execute("SELECT GAMEID FROM Game WHERE GAMENAME = ?", (gameName,))
        gameID = self.cursor.fetchone()
        if not gameID:
            raise ValueError(f"Game named {gameName} not found.")
        
        # Find the playerID based on playerName
        self.cursor.execute("SELECT PLAYERID FROM Player WHERE PLAYERNAME = ?", (playerName,))
        playerID = self.cursor.fetchone()
        if not playerID:
            raise ValueError(f"Player named {playerName} not found.")
        
        # Insert a new shot record associated with the gameID and playerID
        self.cursor.execute("INSERT INTO Shot (PLAYERID, GAMEID) VALUES (?, ?)", (playerID[0], gameID[0]))
        shotID = self.cursor.lastrowid
        self.cursor.close()
        self.conn.commit()
        
        return shotID

    def recordTableShotAssociation(self, myTableID, shotID):
        # SQL query to insert the association of a table and a shot into the TableShot table
        query = "INSERT INTO TableShot (TABLEID, SHOTID) VALUES (?, ?)"

        # Execute the SQL query with the provided myTableID and shotID parameters
        self.cursor.execute(query, (myTableID, shotID))

        #Commit the changes
        self.cursor.close()
        self.conn.commit()


class Game():

    def __init__(self, gameID=None, gameName=None, player1Name=None, player2Name=None):
        """
        Initializes a Game object with the given attributes. The gameID, gameName,
        player1Name, and player2Name arguments allow for various ways to instantiate
        a Game object based on the supplied arguments.
        """
        # Create a Database object and initialize the database
        self.db = Database()
        self.db.createDB()
        self.db.createConnection()

      # Scenario 1: Only gameID provided
        if isinstance(gameID, int) and all(param is None for param in [gameName, player1Name, player2Name]):
             # Adjust gameID for SQL indexing
            adjusted_gameID = gameID + 1
            # print(f"Adjusted gameID: {adjusted_gameID}")
            # Get game details from the database using the adjusted gameID
            game_details = self.db.getGame(adjusted_gameID)
            
             # Check if game details are found
             # print(f"Game details: {game_details}")
            if game_details:
                 # Unpack the game details and assign them to instance variables
                self.gameID, self.gameName, self.player1Name, self.player2Name = game_details
            else:
                # Raise a ValueError if no game details are found for the provided gameID
                raise ValueError(f"Game with ID {gameID} not found.")
                
        # Scenario 2: gameID is None, and names are provided
        elif gameID is None and all(isinstance(param, str) for param in [gameName, player1Name, player2Name]):
            # Call setGame method to create a new game in the database and obtain the gameID
            self.gameID = self.db.setGame(gameName, player1Name, player2Name)
            self.gameName = gameName
            self.player1Name = player1Name
            self.player2Name = player2Name
            
        else:
             # Raise a TypeError for invalid arguments during Game instantiation
            raise TypeError("Invalid arguments for Game class instantiation.")   

    def update(self, p1, p2):
        self.db.updatePlayers(p1,p2)

    def shoot(self, gameName, playerName, table, xvel, yvel):

         # Create a new shot in the database and obtain the shotID
        myShotID = self.db.newShot(gameName, playerName)

        # Create a new cue ball with the specified initial velocities
        myCueBall = table.cueBall(table, xvel, yvel)

        # Continue shooting until the table is exhausted
        while table is not None:
            # Record the start time of the current table state
            timeStart = table.time
             
             # Save a copy of the current table state
            myNewTable = table
            
             # Obtain the next segment of the table
            table = table.segment()

            if table is not None: 
                timeEnd = table.time; # Record the end time of the current table state

            # Calculate the elapsed time for the current segment
            elapsed_time = timeEnd - timeStart

            # Calculate the number of framesEF based on the elapsed time and FRAME_INTERVAL
            framesEF = int(elapsed_time / FRAME_INTERVAL)

            # Iterate through framesEF to simulate the movement of the balls
            for frame in range(framesEF):
                 # Calculate the new time for each frame
                timeNew = FRAME_INTERVAL * frame

                 # Create a copy of the table state at the new time
                tableCopy = myNewTable.roll(timeNew)

                 # Update the time of the copied table state
                tableCopy.time = timeNew + timeStart

                 # Write the copied table state to the database and obtain the myTableID
                myTableID = self.db.writeTable(tableCopy)

                 # Create SVG for the table and write it to a file
                 #write_svg(myTableID, tableCopy)

                # Record the association between the table state and the shot in the database
                self.db.recordTableShotAssociation(myTableID, myShotID)

         # Return the shotID of the completed shot
        return myShotID

def write_svg(table_id, table):
    with open("table%4.2f.svg" % table.time, "w") as fp:
        fp.write(table.svg())


