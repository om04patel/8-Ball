#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#define PHYLIB_BALL_RADIUS (28.5) //mm
#define PHYLIB_BALL_DIAMETER (2 * PHYLIB_BALL_RADIUS)

#define PHYLIB_HOLE_RADIUS (2 * PHYLIB_BALL_DIAMETER)
#define PHYLIB_TABLE_LENGTH (2700.0) //mm
#define PHYLIB_TABLE_WIDTH (PHYLIB_TABLE_LENGTH / 2.0) //mm

#define PHYLIB_SIM_RATE (0.0001) //s
#define PHYLIB_VEL_EPSILON (0.01) //mm / s

#define PHYLIB_DRAG (150.0) // mm/s^2
#define PHYLIB_MAX_TIME (600) // s
#define PHYLIB_MAX_OBJECTS (26)

typedef enum {             
PHYLIB_STILL_BALL = 0,
PHYLIB_ROLLING_BALL = 1,
PHYLIB_HOLE = 2,                 //Polymorphic Object Types
PHYLIB_HCUSHION = 3,
PHYLIB_VCUSHION = 4,
} phylib_obj;

typedef struct {
double x;
double y;                   //Class representing a vector in 2 dimensions
} phylib_coord;

typedef struct {
    unsigned char number;   //Child Class representing objects in the table - STILL BALL
    phylib_coord pos;
} phylib_still_ball;

typedef struct {
unsigned char number;
phylib_coord pos;
phylib_coord vel;      //Represents Rolling Ball
phylib_coord acc;
} phylib_rolling_ball;

typedef struct {
phylib_coord pos;     //Represents One of the Holes on the table 
} phylib_hole;

typedef struct {
double y;            //Represents a horizontal cushion on the side of the table
} phylib_hcushion;   //Only has a Y-Coordinate - SHORT SIDES OF THE TABLE

typedef struct {
double x;            //Represents a vertical cushion
} phylib_vcushion;     //Only has a X- Coordinate - LONG SIDES OF THE TABLE

typedef union {
phylib_still_ball still_ball;
phylib_rolling_ball rolling_ball;  //C Union that holds all the classes 
phylib_hole hole;                   //Easier Access
phylib_hcushion hcushion;
phylib_vcushion vcushion;
} phylib_untyped; 

typedef struct {
phylib_obj type;
phylib_untyped obj;  //Used to identify the class of the object
} phylib_object;    //type is the enum, obj is the object

typedef struct {
double time;
phylib_object *object[PHYLIB_MAX_OBJECTS]; //The Table itself 
} phylib_table;


phylib_object * phylib_new_still_ball(unsigned char number, phylib_coord *pos );

// 1.) This function allocates memory for a new phylib_object 
// 2.) sets it type to PHYLIB_STILL_BALL 
// 3.) transfer the "number" and "pos" into the structure phylib_object 
// 4.) Return a pointer to the phylib_object -- if malloc fails -> return NULL

phylib_object *phylib_new_rolling_ball( unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc );

// 1.) This function allocates memory for a new phylib_object 
// 2.) sets it type to PHYLIB_ROLLING_BALL 
// 3.) transfer the "number" and "pos" and "vel" and "acc" into the structure phylib_object 
// 4.) Return a pointer to the phylib_object -- if malloc fails -> return NULL

phylib_object * phylib_new_hole( phylib_coord *pos );

// 1.) This function allocates memory for a new phylib_object 
// 2.) sets it type to PHYLIB_NEW_HOLE
// 3.) transfer the "pos" into the structure phylib_object 
// 4.) Return a pointer to the phylib_object -- if malloc fails -> return NULL

phylib_object * phylib_new_hcushion( double y );

// 1.) This function allocates memory for a new phylib_object 
// 2.) sets it type to PHYLIB_HCUSHION ->
// 3.) transfer the "y" into the structure phylib_object 
// 4.) Return a pointer to the phylib_object -- if malloc fails -> return NULL

phylib_object * phylib_new_vcushion( double x );

// 1.) This function allocates memory for a new phylib_object 
// 2.) sets it type to PHYLIB_VCUSHION
// 3.) transfer the "x" into the structure phylib_object 
// 4.) Return a pointer to the phylib_object -- if malloc fails -> return NULL

phylib_table * phylib_new_table(void);

//  1.) Allocate memory for a table structure
//  2.) Return Null if the allocation fails
//  3.) set the member variable "time" to 0.0
//  4.) Assign the array elements to pointers to new objects created by phylib_new_* ->
      //1) a horizontal cushion at y=0.0;
       //2) a horizontal cushion at y=PHYLIB_TABLE_LENGTH;
       //3) a vertical cushion at x=0.0;
      //4) a vertical cushion at x=PHYLIB_TABLE_WIDTH;
       //5) 6 holes: positioned in the four corners where the cushions meet and two more
            //midway between the top holes and bottom holes.
            //The remaining pointers will all be set to NULL

void phylib_copy_object( phylib_object **dest, phylib_object **src );

//Allocate Memory for a phylib_object
//Copy the contents of the object from the location pointed to by src to the newly allocated memory.
//Use memcpy for a one-step operation that works for any type of phylib_object.
//if src points to a location containing a NULL pointer, assign the value of NULL to the location pointed to by dest.
//Save the address of the newly allocated phylib_object at the location pointed to by dest.

phylib_table *phylib_copy_table( phylib_table *table );

void phylib_add_object( phylib_table *table, phylib_object *object );

void phylib_free_table( phylib_table *table );

phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 );

double phylib_length( phylib_coord c );

double phylib_dot_product( phylib_coord a, phylib_coord b );

double phylib_distance( phylib_object *obj1, phylib_object *obj2 );

void phylib_roll(phylib_object *new, phylib_object *old, double time);

unsigned char phylib_stopped(phylib_object *object);

void phylib_bounce (phylib_object **a, phylib_object **b); 

unsigned char phylib_rolling(phylib_table *t);

phylib_table *phylib_segment(phylib_table *table); 

void phylib_free_object(phylib_object *obj); //Helper function

char *phylib_object_string( phylib_object *object );

