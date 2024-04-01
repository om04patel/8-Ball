#include "phylib.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

phylib_object *phylib_new_still_ball(unsigned char number, phylib_coord *pos) {
    // Allocate memory for a new phylib_object
    phylib_object *newObject = (phylib_object *)malloc(sizeof(phylib_object));

    // Check if malloc was successful
    if (newObject == NULL) {
        return NULL; // Return NULL if memory allocation fails
    }

    // Set the type of the new object to PHYLIB_STILL_BALL
    newObject->type = PHYLIB_STILL_BALL;

    // Set the values of the still_ball structure within the union
    newObject->obj.still_ball.number = number;
    newObject->obj.still_ball.pos = *pos; // Dereference pos to get the phylib_coord values

    // Return a pointer to the newly created phylib_object
    return newObject;
}

phylib_object *phylib_new_rolling_ball(unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc) {
    // Allocate memory for a new phylib_object
    phylib_object *newObject = (phylib_object *)malloc(sizeof(phylib_object));

    // Check if malloc was successful
    if (newObject == NULL) {
        return NULL; // Return NULL if memory allocation fails
    }

    // Set the type of the new object to PHYLIB_ROLLING_BALL
    newObject->type = PHYLIB_ROLLING_BALL;

    // Set the values of the rolling_ball structure within the union
    newObject->obj.rolling_ball.number = number;
    newObject->obj.rolling_ball.pos = *pos; // Dereference pos to get the phylib_coord values
    newObject->obj.rolling_ball.vel = *vel; // Dereference vel to get the phylib_coord values
    newObject->obj.rolling_ball.acc = *acc; // Dereference acc to get the phylib_coord values

    // Return a pointer to the newly created phylib_object
    return newObject;
}

phylib_object *phylib_new_hole(phylib_coord *pos) {
    // Allocate memory for a new phylib_object
    phylib_object *newObject = (phylib_object *)malloc(sizeof(phylib_object));

    // Check if malloc was successful
    if (newObject == NULL) {
        return NULL; // Return NULL if memory allocation fails
    }

    // Set the type of the new object to PHYLIB_HOLE
    newObject->type = PHYLIB_HOLE;

    // Set the values of the hole structure within the union
    newObject->obj.hole.pos = *pos; // Dereference pos to get the phylib_coord values

    // Return a pointer to the newly created phylib_object
    return newObject;
}

phylib_object *phylib_new_hcushion(double y) {
    // Allocate memory for a new phylib_object
    phylib_object *newObject = (phylib_object *)malloc(sizeof(phylib_object));

    // Check if malloc was successful
    if (newObject == NULL) {
        return NULL; // Return NULL if memory allocation fails
    }

    // Set the type of the new object to PHYLIB_HCUSHION
    newObject->type = PHYLIB_HCUSHION;

    // Set the value of the hcushion structure within the union
    newObject->obj.hcushion.y = y;

    // Return a pointer to the newly created phylib_object
    return newObject;
}

phylib_object *phylib_new_vcushion(double x) {
    // Allocate memory for a new phylib_object
    phylib_object *newObject = (phylib_object *)malloc(sizeof(phylib_object));

    // Check if malloc was successful
    if (newObject == NULL) {
        return NULL; // Return NULL if memory allocation fails
    }

    // Set the type of the new object to PHYLIB_VCUSHION
    newObject->type = PHYLIB_VCUSHION;

    // Set the value of the vcushion structure within the union
    newObject->obj.vcushion.x = x;

    // Return a pointer to the newly created phylib_object
    return newObject;
}

phylib_table *phylib_new_table(void) {
    // Allocate memory for a new phylib_table
    phylib_table *newTable = (phylib_table *)malloc(sizeof(phylib_table));

    // Check if malloc was successful
    if (newTable == NULL) {
        return NULL; // Return NULL if memory allocation fails
    }

    // Set the member variable "time" to 0.0
    newTable->time = 0.0;

    // Assign the array elements to pointers to new objects created by phylib_new_*

    // 1) a horizontal cushion at y=0.0
    newTable->object[0] = phylib_new_hcushion(0.0);

    // 2) a horizontal cushion at y=PHYLIB_TABLE_LENGTH
    newTable->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);

    // 3) a vertical cushion at x=0.0
    newTable->object[2] = phylib_new_vcushion(0.0);

    // 4) a vertical cushion at x=PHYLIB_TABLE_WIDTH
    newTable->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);

    // 5) 6 holes: positioned in the four corners where the cushions meet and two more
    // midway between the top holes and bottom holes.
    newTable->object[4] = phylib_new_hole(&(phylib_coord){0.0, 0.0});
    newTable->object[5] = phylib_new_hole(&(phylib_coord){0.0, PHYLIB_TABLE_WIDTH});
    newTable->object[6] = phylib_new_hole(&(phylib_coord){0.0, PHYLIB_TABLE_LENGTH});
    newTable->object[7] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, 0.0});
    newTable->object[8] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_WIDTH});
    newTable->object[9] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH});

    // The remaining pointers will all be set to NULL
    for (int i = 10; i < PHYLIB_MAX_OBJECTS; ++i) {
        newTable->object[i] = NULL;
    }

    // Return a pointer to the newly created phylib_table
    return newTable;
}

void phylib_copy_object( phylib_object **dest, phylib_object **src ){

    if(*src == NULL){
        *dest = NULL;  //if the src is null then we pass the NULL pointer to destination
    } else {
        //Allocate memory for the new Object
        *dest= (phylib_object *)malloc(sizeof(phylib_object));

        if(*dest == NULL){
            // Handle memory allocation failure
            fprintf(stderr, "Memory allocation failed in phylib_copy_object\n");
            exit(EXIT_FAILURE);
        }

        memcpy(*dest,*src,sizeof(phylib_object)); // Use memcpy to copy the contents of the object from src to newObject
    }    
}

phylib_table *phylib_copy_table(phylib_table *table) {
    // Allocate memory for a new phylib_table
    phylib_table *newTable = (phylib_table *)malloc(sizeof(phylib_table));
    
    // Check if malloc was successful
    if (newTable == NULL) {
        return NULL; // Return NULL if allocation fails
    }

    memcpy(newTable,table,sizeof(phylib_table));

    // Copy the contents from the original table to the new memory location
    

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if (table->object[i] != NULL) {
         // Copy the contents of the object using phylib_copy_object
            phylib_copy_object(&(newTable->object[i]), &(table->object[i]));
        } else {
            // If the original object is NULL, set the corresponding object in newTable to NULL
            newTable->object[i] = NULL;
        }
    }

    return newTable; // Return the address of the newly allocated phylib_table
}

void phylib_add_object(phylib_table *table, phylib_object *object) {
    // Iterate over the object array in the table
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; ++i) {
        // Check if the current object pointer is NULL
        if (table->object[i] == NULL) {
            // Assign the address of the object to the NULL pointer
            table->object[i] = object;
            return;  // Object added, exit the function
        }
    }
    // If there are no NULL pointers in the array, the function should do nothing
}

void phylib_free_table(phylib_table *table) {
    // Free every non-NULL pointer in the object array
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; ++i) {
        if (table->object[i] != NULL) {
            free(table->object[i]);
            table->object[i] = NULL;  // Set the pointer to NULL after freeing
        }
    }
    // Free the table itself
    free(table);
}

phylib_coord phylib_sub(phylib_coord c1, phylib_coord c2) {
    phylib_coord result;  //use result variable for coordinates
    result.x = c1.x - c2.x;  //calculate the x value
    result.y = c1.y - c2.y;  //calculate the y value
    return result;
}

double phylib_length(phylib_coord c) {
    // Calculate the length using the Pythagorean theorem
    double length_squared = ((c.x * c.x) + (c.y * c.y));
    
    // Return the square root of the length squared
    double length = 0.0;
    if (length_squared > 0.0) {
        // Avoid taking the square root if length_squared is zero
        length = sqrt(length_squared);
    }
    return length;
}

double phylib_dot_product(phylib_coord a, phylib_coord b) {
    // Compute the dot product of two vectors
    double dotProduct = ((a.x * b.x) + (a.y * b.y));
    
    return dotProduct;
}

double phylib_distance(phylib_object *obj1, phylib_object *obj2) {
    // Check if obj1 is a PHYLIB_ROLLING_BALL
    if (obj1->type != PHYLIB_ROLLING_BALL) {
        return -1.0; // Return -1.0 if obj1 is not a PHYLIB_ROLLING_BALL
    }

    // Calculate the distance based on the type of obj2
    switch (obj2->type) {
        case PHYLIB_ROLLING_BALL: {
        double distance = phylib_length(phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.rolling_ball.pos))
                              - PHYLIB_BALL_DIAMETER;
                return distance;
                                }
        case PHYLIB_STILL_BALL: {
            // Compute the distance between the centres of the two balls and subtract two radii
            double distance = phylib_length(phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.still_ball.pos))
                              - PHYLIB_BALL_DIAMETER;
            return distance;
        }
        case PHYLIB_HOLE: {
            // Compute the distance between the centre of the ball and the hole and subtract the HOLE_RADIUS
            double distance = phylib_length(phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.hole.pos))
                              - PHYLIB_HOLE_RADIUS;
            return distance;
        }
        case PHYLIB_HCUSHION: {
            // Compute the distance between the centre of the ball and the cushion and subtract the BALL_RADIUS
            double distance = fabs(obj1->obj.rolling_ball.pos.y - obj2->obj.hcushion.y) - PHYLIB_BALL_RADIUS;
            return distance;
        }
        case PHYLIB_VCUSHION: {
            // Compute the distance between the centre of the ball and the cushion and subtract the BALL_RADIUS
            double distance = fabs(obj1->obj.rolling_ball.pos.x - obj2->obj.vcushion.x) - PHYLIB_BALL_RADIUS;
            return distance;
        }
        default:
            return -1.0;
            break; // Return -1.0 if obj2 isn't any valid type
    }
}

void phylib_roll(phylib_object *new, phylib_object *old, double time) {
    // Check if new and old are PHYLIB_ROLLING_BALLs
    if (new->type != PHYLIB_ROLLING_BALL || old->type != PHYLIB_ROLLING_BALL) {
        // If not, do nothing
        return;
    }

    // Calculate the updated position using the physics formula
    new->obj.rolling_ball.pos.x = old->obj.rolling_ball.pos.x +
                                  old->obj.rolling_ball.vel.x * time +
                                  0.5 * old->obj.rolling_ball.acc.x * time * time;

    new->obj.rolling_ball.pos.y = old->obj.rolling_ball.pos.y +
                                  old->obj.rolling_ball.vel.y * time +
                                  0.5 * old->obj.rolling_ball.acc.y * time * time;

    // Calculate the updated velocity using the physics formula
    new->obj.rolling_ball.vel.x = old->obj.rolling_ball.vel.x +
                                  old->obj.rolling_ball.acc.x * time;

    new->obj.rolling_ball.vel.y = old->obj.rolling_ball.vel.y +
                                  old->obj.rolling_ball.acc.y * time;

    // Check if either velocity changes sign and update accordingly
    if ((old->obj.rolling_ball.vel.x * new->obj.rolling_ball.vel.x) < 0.0) {
        new->obj.rolling_ball.vel.x = 0.0;
        new->obj.rolling_ball.acc.x = 0.0;
    }

    if ((old->obj.rolling_ball.vel.y * new->obj.rolling_ball.vel.y) < 0.0) {
        new->obj.rolling_ball.vel.y = 0.0;
        new->obj.rolling_ball.acc.y = 0.0;
    }
}

unsigned char phylib_stopped(phylib_object *object) {
    // Check if the object is a ROLLING_BALL
    if (object->type != PHYLIB_ROLLING_BALL) {
        // If not, return 0
        return 0;
    }

    // Calculate the speed (length of velocity vector)
    double speed = phylib_length(object->obj.rolling_ball.vel);

    // Check if the speed is less than PHYLIB_VEL_EPSILON
    if (speed < PHYLIB_VEL_EPSILON) {
        // Convert the ROLLING_BALL to STILL_BALL
        object->type = PHYLIB_STILL_BALL;

        // Transfer information from rolling ball to still ball
        object->obj.still_ball.number = object->obj.rolling_ball.number;
        object->obj.still_ball.pos = object->obj.rolling_ball.pos;

        return 1; // Return 1 indicating conversion
    }
    return 0; // Return 0 if no conversion
}

void phylib_bounce(phylib_object **a, phylib_object **b) {
    
    if((*a)->type != PHYLIB_ROLLING_BALL){
        return;
    }

    switch ((*b)->type) {
        case PHYLIB_HCUSHION:
            // Reverse y velocity and y acceleration of a
            (*a)->obj.rolling_ball.vel.y = -((*a)->obj.rolling_ball.vel.y);
            (*a)->obj.rolling_ball.acc.y = -((*a)->obj.rolling_ball.acc.y);
            break;

        case PHYLIB_VCUSHION:
            // Reverse x velocity and x acceleration of a
            (*a)->obj.rolling_ball.vel.x = -((*a)->obj.rolling_ball.vel.x);
            (*a)->obj.rolling_ball.acc.x = -((*a)->obj.rolling_ball.acc.x);
            break;

        case PHYLIB_HOLE:
            // Free memory of a and set it to NULL
            phylib_free_object(*a);
            *a = NULL;
            break;

        case PHYLIB_STILL_BALL:
            // "Upgrade" the STILL_BALL to a ROLLING BALL
            (*b)->type = PHYLIB_ROLLING_BALL;
            (*b)->obj.rolling_ball.pos = ((*b)->obj.still_ball.pos);
            (*b)->obj.rolling_ball.vel.x = 0.0;
            (*b)->obj.rolling_ball.vel.y = 0.0;
            (*b)->obj.rolling_ball.acc.x = 0.0;
            (*b)->obj.rolling_ball.acc.y = 0.0;


            // Proceed directly to the ROLLING_BALL case
            // No break statement here to continue execution

        case PHYLIB_ROLLING_BALL: {
            // Compute the position of a with respect to b
            phylib_coord r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);

            // Compute the relative velocity of a with respect to b
            phylib_coord v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);

            // Compute the length of r_ab
            double length_r_ab = phylib_length(r_ab);

            // Check if length_r_ab is not zero to avoid division by zero
            if (length_r_ab > 0.0) {
                // Compute the normal vector, n
                phylib_coord n = { r_ab.x / length_r_ab, r_ab.y / length_r_ab };

                // Calculate the ratio of the relative velocity, v_rel, in the direction of ball a
                double v_rel_n = phylib_dot_product(v_rel, n);

                // Update the velocities of a and b based on the collision
                (*a)->obj.rolling_ball.vel.x -= v_rel_n * n.x;
                (*a)->obj.rolling_ball.vel.y -= v_rel_n * n.y;

                (*b)->obj.rolling_ball.vel.x += v_rel_n * n.x;
                (*b)->obj.rolling_ball.vel.y += v_rel_n * n.y;

                // Compute the speeds of a and b
                double speed_a = phylib_length((*a)->obj.rolling_ball.vel);
                double speed_b = phylib_length((*b)->obj.rolling_ball.vel);

                // Check if the speed is greater than PHYLIB_VEL_EPSILON for a
                if (speed_a > PHYLIB_VEL_EPSILON) {
                    // Set the acceleration of a
                    (*a)->obj.rolling_ball.acc.x = -(((*a)->obj.rolling_ball.vel.x) / speed_a) * PHYLIB_DRAG;
                    (*a)->obj.rolling_ball.acc.y = -(((*a)->obj.rolling_ball.vel.y) / speed_a) * PHYLIB_DRAG;
                }
                if (speed_b > PHYLIB_VEL_EPSILON){
                    (*b)->obj.rolling_ball.acc.x = -(((*b)->obj.rolling_ball.vel.x) / speed_b) * PHYLIB_DRAG;
                    (*b)->obj.rolling_ball.acc.y = -(((*b)->obj.rolling_ball.vel.y) / speed_b) * PHYLIB_DRAG;
                }
            }
            break;
        }
    }
}

unsigned char phylib_rolling(phylib_table *t) {
    unsigned char rollingCount = 0; // Initialize count of rolling balls to zero

    // Iterate over the objects in the table
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; ++i) {
        // Check if the object is not NULL and of type PHYLIB_ROLLING_BALL
        if (t->object[i] != NULL && t->object[i]->type == PHYLIB_ROLLING_BALL) {
            rollingCount++; // Increment count for each rolling ball found
        }
    }
    return rollingCount; // Return the total number of rolling balls
}  

phylib_table *phylib_segment(phylib_table *table) {

    // Check if there are any ROLLING_BALLs on the table
    if (phylib_rolling(table) == 0) {
        // No ROLLING_BALLs, return NULL
        return NULL;
    }
    // Create a copy of the table to be modified
    phylib_table *segmentTable = phylib_copy_table(table);

    double segmentTime = PHYLIB_SIM_RATE;

    while(segmentTime <= PHYLIB_MAX_TIME){ // Loop over time

        for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
            if(segmentTable->object[i] != NULL && segmentTable->object[i]->type == PHYLIB_ROLLING_BALL){ //check for rolling ball)
            phylib_roll(segmentTable->object[i],table->object[i],segmentTime); //apply roll   
            }
        }

        for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
            for(int j = 0; j < PHYLIB_MAX_OBJECTS; j++){
                    if(i != j && segmentTable->object[i] != NULL && segmentTable->object[i]->type == PHYLIB_ROLLING_BALL && segmentTable->object[j] != NULL){
                        double dist = phylib_distance(segmentTable->object[i],segmentTable->object[j]); 
                        if(dist < 0.0){
                            phylib_bounce(&(segmentTable->object[i]),&(segmentTable->object[j])); //check for collisions
                            segmentTable->time += segmentTime;
                            return segmentTable;
                        }
                    }
                }
                if(segmentTable->object[i] != NULL && segmentTable->object[i]->type == PHYLIB_ROLLING_BALL && phylib_stopped(segmentTable->object[i])){ //Rolling ball has stopped
                    segmentTable->time += segmentTime;
                    return segmentTable;
                }
            }
        segmentTime += PHYLIB_SIM_RATE;                             //update time
        }  
        segmentTable->time += segmentTime;   //update time  
        return segmentTable;
    }
   
void phylib_free_object(phylib_object *obj) { //Helper Function
        if (obj == NULL) {
            return;  // Do nothing if the object is already NULL
        }
        // Free the generic memory for the object
        free(obj);
    }

char *phylib_object_string( phylib_object *object )
{
static char string[80];
if (object==NULL)
{
snprintf( string, 80, "NULL;" );
return string;
}
switch (object->type)
{
case PHYLIB_STILL_BALL:
snprintf( string, 80,
"STILL_BALL (%d,%6.1lf,%6.1lf)",
object->obj.still_ball.number,
object->obj.still_ball.pos.x,
object->obj.still_ball.pos.y );
break;
case PHYLIB_ROLLING_BALL:
snprintf( string, 80,
"ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
object->obj.rolling_ball.number,
object->obj.rolling_ball.pos.x,
object->obj.rolling_ball.pos.y,
object->obj.rolling_ball.vel.x,
object->obj.rolling_ball.vel.y,
object->obj.rolling_ball.acc.x,
object->obj.rolling_ball.acc.y );
break;
case PHYLIB_HOLE:
snprintf( string, 80,
"HOLE (%6.1lf,%6.1lf)",
object->obj.hole.pos.x,
object->obj.hole.pos.y );
break;
case PHYLIB_HCUSHION:    
snprintf( string, 80,
"HCUSHION (%6.1lf)",
object->obj.hcushion.y );
break;
case PHYLIB_VCUSHION:
snprintf( string, 80,
"VCUSHION (%6.1lf)",
object->obj.vcushion.x );
break;
}
return string;
}
