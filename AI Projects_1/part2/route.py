#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: Durga Sai Sailesh Chodabattula (dchodaba), Manideep Varma Penumatsa (mpenumat), and Lakku Sai Jagan (slakku)
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#


# !/usr/bin/env python3
import sys
import pandas as pd 
import math
import heapq

#reading segments data 
road = pd.read_csv('road-segments.txt', delimiter=' ', header=None, names=["city_1","city_2","length","speed_limit","highway_name"])
road["time"]=road.length/road.speed_limit
road["prob"] = 0

#reading gps data    
gps=pd.read_csv('city-gps.txt',delimiter=' ', header=None, names=["city","latitude","longitude"])
for i in range(0,road.shape[0]):
    if 50 <= int(road['speed_limit'][i]):
       road["prob"].iloc[i] = float(math.tanh(road['length'].iloc[i]/1000)) 
    else:
        road["prob"].iloc[i] = 0

(speed, avg_road_seg)=( road.speed_limit.mean() , road.length.sum()/road.shape[0] )


#generates the successors by comparing the city given with the possible neighbouring cities/route
def successors(start):
    fringe=[]
    for i in range(0,road.shape[0]):
        if road.city_1[i]==start:
            fringe.append([road.city_1[i],road.city_2[i],road.length[i],road.speed_limit[i],road.highway_name[i],road.time[i], road.prob[i]])
        elif road.city_2[i]==start:
            fringe.append([road.city_2[i],road.city_1[i],road.length[i],road.speed_limit[i],road.highway_name[i],road.time[i],road.prob[i]])
    return fringe

# Ref: https://stackoverflow.com/questions/36873187/heuristic-for-an-a-path-finding-gps
#This function calculates the heuristics using haversine formula
def calculate_heuristic(start_lat,start_long,end_lat,end_long):
    R = 3963
    dest_Lat = degrees_to_radians(end_lat-start_lat)
    dest_Lon = degrees_to_radians(end_long-start_long)
    a = math.sin(dest_Lat/2) * math.sin(dest_Lat/2) + math.cos(degrees_to_radians(start_lat)) * math.cos(degrees_to_radians(end_lat)) * math.sin(dest_Lon/2) * math.sin(dest_Lon/2)
    b = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    c = R * b; 
    return c



def degrees_to_radians(deg):
    return deg * (math.pi/180)

# this segment returns the goal with ideal time path                
def calculate_min_heuristic(start,end,cost,end_lat,end_long):
    time=0
    visited_nodes=[]
    fringe = [(0,0,start,[])]
    heapq.heapify(fringe)
    while len(fringe) !=0:
        succ = heapq.heappop(fringe) #popping out the path with the least hueristic value
        if succ[2]==end: return succ[3]# checking the goal state
        visited_nodes.append(succ[2]) #keeping a track of the visited nodes
        for move in successors(succ[2]):
            try:
                lat_c = gps.loc[gps.city==move[1], 'latitude'].iloc[0]  
                long_c = gps.loc[gps.city==move[1], 'longitude'].iloc[0]
                cal_heuristic = calculate_heuristic(lat_c,long_c,end_lat,end_long)  # heuristic is the haversine distance from current state to the goal state 
            except: cal_heuristic=0
                
            if cost == "time":  # cathces the case where a certain destination does not have lat and long
                if move[1] not in visited_nodes:
                    time=0
                    for i in succ[3]: time += i[5]  # caclulating the time travelled from start state to current state
                # cost + heuristic
                    x = time + cal_heuristic/speed
                    heapq.heappush(fringe,(x,move[2],move[1],succ[3]+[move]))
            elif cost == "segments":
                if move[1] not in visited_nodes:
                    cost_segment=len(succ[3])
                    # cost + heuristic
                    x = cost_segment+cal_heuristic/avg_road_seg
                    heapq.heappush(fringe,(x,move[2],move[1],succ[3]+[move]))
            elif cost == "distance":
                if move[1] not in visited_nodes:
                    distance=0
                    for i in succ[3]: distance += i[2] # caclulating the distance travelled from start state to current state
                    # cost + heuristic
                    x = distance + cal_heuristic
                    heapq.heappush(fringe,(x,move[2],move[1],succ[3]+[move]))
            elif cost == "delivery":
                if move[1] not in visited_nodes:
                    deli = 0
                    time_trip=0

                    for i in succ[3]:
                        time_trip += i[5]
                        deli+= i[5] + (2*i[6]*time_trip)
                        #if i[3] >= 50: prob += i[6]  # caclulating the safe probability from start state to current state
                    # cost + heuristic
                    x = deli + cal_heuristic
                    heapq.heappush(fringe,(x,move[2],move[1],succ[3]+[move]))


def get_route(start, end, cost):
    """
    Find shortest driving route between start city and end city
    based on a cost function.

    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-delivery-hours": a float indicating the expected (average) time 
                                   it will take a delivery driver who may need to return to get a new package
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """
    (distance , time , safe, route)=(float(0),float(0),float(0),[])
    end_lat = gps.loc[gps.city==end, 'latitude'].iloc[0] 
    end_long = gps.loc[gps.city==end, 'longitude'].iloc[0]
    heuristic = calculate_min_heuristic(start,end,cost,end_lat,end_long)
    for i in heuristic: #iterating through the popped out goal to get the sum of distance, time and probability of safe path
        distance += i[2]
        time +=  i[5]
        if int(i[3]) >= 50: safe+= (2*i[6]*(time))
        route.append((i[1],str(i[4])+" for "+str(i[2])+" miles"))
    return{"total-segments" : len(heuristic), "total-miles": distance , "total-hours" : time , "total-delivery-hours" : time+safe,  "route-taken" : route}
    
    
'''

    route_taken = [("Martinsville,_Indiana","IN_37 for 19 miles"),
                   ("Jct_I-465_&_IN_37_S,_Indiana","IN_37 for 25 miles"),
                   ("Indianapolis,_Indiana","IN_37 for 7 miles")]
    
    return {"total-segments" : len(route_taken), 
            "total-miles" : 51., 
            "total-hours" : 1.07949, 
            "total-delivery-hours" : 1.1364, 
            "route-taken" : route_taken}
'''


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "safe"):
        raise(Exception("Error: invalid cost function"))
    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])


