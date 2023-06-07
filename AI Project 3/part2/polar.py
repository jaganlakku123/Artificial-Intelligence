#!/usr/local/bin/python3
#
# Authors: [PLEASE PUT YOUR NAMES AND USER IDS HERE]
#
# Ice layer finder
# Based on skeleton code by D. Crandall, November 2021
#

from PIL import Image
from numpy import *
from scipy.ndimage import filters
import sys
import imageio
import numpy as np

# calculate "Edge strength map" of an image                                                                                                                                      
def edge_strength(input_image):
    grayscale = array(input_image.convert('L'))
    filtered_y = zeros(grayscale.shape)
    filters.sobel(grayscale,0,filtered_y)
    return sqrt(filtered_y**2)

# draw a "line" on an image (actually just plot the given y-coordinates
#  for each x-coordinate)
# - image is the image to draw on
# - y_coordinates is a list, containing the y-coordinates and length equal to the x dimension size
#   of the image
# - color is a (red, green, blue) color triple (e.g. (255, 0, 0) would be pure red
# - thickness is thickness of line in pixels
#
def draw_boundary(image, y_coordinates, color, thickness):
    for (x, y) in enumerate(y_coordinates):
        for t in range( int(max(y-int(thickness/2), 0)), int(min(y+int(thickness/2), image.size[1]-1 )) ):
            image.putpixel((x, t), color)
    return image

def draw_asterisk(image, pt, color, thickness):
    for (x, y) in [ (pt[0]+dx, pt[1]+dy) for dx in range(-3, 4) for dy in range(-2, 3) if dx == 0 or dy == 0 or abs(dx) == abs(dy) ]:
        if 0 <= x < image.size[0] and 0 <= y < image.size[1]:
            image.putpixel((x, y), color)
    return image


# Save an image that superimposes three lines (simple, hmm, feedback) in three different colors 
# (yellow, blue, red) to the filename
def write_output_image(filename, image, simple, hmm, feedback, feedback_pt):
    new_image = draw_boundary(image, simple, (255, 255, 0), 2)
    new_image = draw_boundary(new_image, hmm, (0, 0, 255), 2)
    new_image = draw_boundary(new_image, feedback, (255, 0, 0), 2)
    new_image = draw_asterisk(new_image, feedback_pt, (255, 0, 0), 2)
    imageio.imwrite(filename, new_image)

def get_starting_point(emission_probs, init_probs):
    probs = [emission_probs[i][0] * init_probs[i] for i in range(len(emission_probs))] 
    return probs

# Just used to make sure an indexing error does not occur
def check_in_boundary(n, col_length):
    if n > 0 and n < col_length:
        return True
    
# Bayes net. We simply use the normalized edge strength to determine the
# the most probable y value for each column.
def bayes_net(probs):
    path = []
    for prob_col in range(len(probs[0])):
        col = []
        for prob in range(len(probs)):
            col.append(probs[prob][prob_col])
        path.append(col.index(max(col)))
    return path
    
# HMM. To get the optimal y value for each column, we simply multiply
# the previous columns probabilities by the transition probabilities, 
# by the normalized edge strength (emission probabilities)
def get_next_column_probs(curr_col_probs, next_col, emission_probs, transition_probs):
    # stores max prob for each y value
    probs = []
    for prob in range(len(emission_probs)):
        # probabilities for current node/pixel
        # We only calculate the probabilities corresponding to
        # the nearest 13 pixels in the previous column, because 
        # we assume all other transition probabilities are zero.
        curr_probs = []
        if check_in_boundary(prob-6, len(curr_col_probs)):
            curr_probs.append(curr_col_probs[prob-6] * emission_probs[prob][next_col] * transition_probs[0])
        if check_in_boundary(prob-5, len(curr_col_probs)):
            curr_probs.append(curr_col_probs[prob-5] * emission_probs[prob][next_col] * transition_probs[1])
        if check_in_boundary(prob-4, len(curr_col_probs)):
            curr_probs.append(curr_col_probs[prob-4] * emission_probs[prob][next_col] * transition_probs[2])
        if check_in_boundary(prob-3, len(curr_col_probs)):
            curr_probs.append(curr_col_probs[prob-3] * emission_probs[prob][next_col] * transition_probs[3])
        if check_in_boundary(prob-2, len(curr_col_probs)):
            curr_probs.append(curr_col_probs[prob-2] * emission_probs[prob][next_col] * transition_probs[4])
        if check_in_boundary(prob-1, len(curr_col_probs)):
            curr_probs.append(curr_col_probs[prob-1] * emission_probs[prob][next_col] * transition_probs[5])
        curr_probs.append(curr_col_probs[prob] * emission_probs[prob][next_col] * transition_probs[6])
        if check_in_boundary(prob+1, len(curr_col_probs)):
            curr_probs.append(curr_col_probs[prob+1] * emission_probs[prob][next_col] * transition_probs[7])
        if check_in_boundary(prob+2, len(curr_col_probs)):
            curr_probs.append(curr_col_probs[prob+2] * emission_probs[prob][next_col] * transition_probs[8])
        if check_in_boundary(prob+3, len(curr_col_probs)):
            curr_probs.append(curr_col_probs[prob+3] * emission_probs[prob][next_col] * transition_probs[9])
        if check_in_boundary(prob+4, len(curr_col_probs)):
            curr_probs.append(curr_col_probs[prob+4] * emission_probs[prob][next_col] * transition_probs[10])
        if check_in_boundary(prob+5, len(curr_col_probs)):
            curr_probs.append(curr_col_probs[prob+5] * emission_probs[prob][next_col] * transition_probs[11])
        if check_in_boundary(prob+6, len(curr_col_probs)):
            curr_probs.append(curr_col_probs[prob+6] * emission_probs[prob][next_col] * transition_probs[12])
        # find max and append to max probs
        max_prob = max(curr_probs)
        probs.append(max_prob)
    return probs
        
# used for the feedback portion. I decided to run two HMM's and 
# combine the path. They both start at the user's point, so one 
# has to go backwards
def flip_array(array):
    new_array = np.zeros((len(array), len(array[0])))
    for i in range(len(array)):
        nj = 0
        for j in range(len(array[0])-1, -1, -1):
            new_array[i][nj] = array[i][j]
            nj += 1
    return new_array

# I use this for the feedback porion, to split the emission probabilities
# using the user provided x value so that we can run two separate HMM's.
def split_by_col(array, col):
    new_array = np.zeros((len(array), col))
    for i in range(len(array)):
        for j in range(col):
            new_array[i][j] = array[i][j]
    new_array2 = np.zeros((len(array), 225-col))
    for i in range(len(array)):
        for j in range(225-col):
            new_array2[i][j] = array[i][224-j]
    return list(new_array), list(new_array2)
    
# main program
#
if __name__ == "__main__":

    if len(sys.argv) != 6:
        raise Exception("Program needs 5 parameters: input_file airice_row_coord airice_col_coord icerock_row_coord icerock_col_coord")

    input_filename = sys.argv[1]
    gt_airice = [ int(i) for i in sys.argv[2:4] ]
    gt_icerock = [ int(i) for i in sys.argv[4:6] ]
    
    # load in image 
    input_image = Image.open(input_filename).convert('RGB')
    image_array = array(input_image.convert('L'))

    # compute edge strength mask -- in case it's helpful. Feel free to use this.
    edge_strength = edge_strength(input_image)
    imageio.imwrite('edges.png', uint8(255 * edge_strength / (amax(edge_strength))))
    
    ############# AIRICE BASIC PATH ###############
    # normalized edge strengths will be used for emission probabilities
    airice_emission_probs = edge_strength / max(edge_strength.flatten())
    
    airice_simple = bayes_net(airice_emission_probs)
    
    ############## AIRICE HMM PATH ################

    # for transition probs, the closest y positions will have the 
    # greatest probs. I am only going to allow the 13 closest pixels
    # in the next column have a prob greater than 0 to simplify the problem
    
    airice_transition_probs = [.0125, .0125, .025, .05, .125, .2, .2, .2, .125, .05, .025, .0125, .0125]
    
    # It was harder picking the initial probabilities.
    # I decided to give the first 100 pixels to have a 
    # uniform probability of .1, and for the last 75,
    # a probability of 0.
    airice_init_probs = [.01] * 100 + [0] * 75
    
    path = []
    # this part has to be separate from the for loop, because
    # the first calculation is different from the rest, as it includes the
    # initial probabilities, and does not consider init probs or previous probs.
    probs = get_starting_point(airice_emission_probs, airice_init_probs)
    path.append(probs.index(max(probs)))
    for i in range(len(airice_emission_probs[0])-1):
        # each time we get the column probabilities, append the index 
        # of the max value to get the next node in our path. 
        probs = get_next_column_probs(probs, i+1, airice_emission_probs, airice_transition_probs)
        path.append(probs.index(max(probs)))
    
    airice_hmm = path
   
    ############ AIRICE FEEDBACK PATH #############
    # Everything else will stay the same, except for the initial probabilities
    # and the starting point. I will create two paths, one starting from the 
    # user's point going left, and one starting from the same point, going right.
    # I will then combine these paths.
    
    emis_probs_1, emis_probs_2 = split_by_col(airice_emission_probs, gt_airice[1])
    
    # flip array: equivalent to running the HMM backwards.
    emis_probs_2 = flip_array(emis_probs_2)
    
    # We assume that the user provided value is always correct, thus 
    # it has a probability of 1, while the rest of the values have 
    # a probability of 0.
    fb_init_probs = [.0001] * gt_airice[0] + [1] + [.0001] * (174 - gt_airice[0])
    
    path1 = []
    path2 = []
    probs = get_starting_point(emis_probs_2, fb_init_probs)
    path2.append(probs.index(max(probs))) 
    for i in range(len(emis_probs_2[0])-1):
        probs = get_next_column_probs(probs, i+1, emis_probs_2, airice_transition_probs)
        path2.append(probs.index(max(probs)))
        
    probs = get_starting_point(emis_probs_2, fb_init_probs)
    for i in range(len(emis_probs_1[0])):
        probs = get_next_column_probs(probs, i, emis_probs_1, airice_transition_probs)
        path1.append(probs.index(max(probs)))
    
    airice_feedback = path1 + path2
    
    ############## ICEROCK PATH SIMPLE ############### 
   
    # this is really the only difference between airice and icerock. 
    # the emission probs that have a y value below airice path + 10
    # are set to zero, because we assume that the icerock path has to be 
    # at least ten pixels below the airice path.
    
    icerock_emission_probs = []
    for row in range(len(edge_strength)):
        r = []
        for col in range(len(edge_strength[0])):
            if airice_simple[col] + 10 > row:
                r.append(0)
            else:
                r.append(airice_emission_probs[row][col])
        icerock_emission_probs.append(r)

    icerock_simple = bayes_net(icerock_emission_probs)
    ############### ICEROCK PATH HMM ###################
    
    icerock_emission_probs = []
    for row in range(len(edge_strength)):
        r = []
        for col in range(len(edge_strength[0])):
            if airice_hmm[col] + 10 > row:
                r.append(0)
            else:
                r.append(airice_emission_probs[row][col])
        icerock_emission_probs.append(r)
    
    path = []
    probs = get_starting_point(icerock_emission_probs, airice_init_probs)
    path.append(probs.index(max(probs)))
    for i in range(len(icerock_emission_probs[0])-1):
        probs = get_next_column_probs(probs, i+1, icerock_emission_probs, airice_transition_probs)
        path.append(probs.index(max(probs)))
        
    icerock_hmm = path
      
    ########### ICEROCK PATH FEEDBACK #############
    
    icerock_emission_probs = []
    for row in range(len(edge_strength)):
        r = []
        for col in range(len(edge_strength[0])):
            if airice_feedback[col] + 10 > row:
                r.append(0)
            else:
                r.append(airice_emission_probs[row][col])
        icerock_emission_probs.append(r)
    
    emis_probs_1, emis_probs_2 = split_by_col(icerock_emission_probs, gt_icerock[1])
    emis_probs_2 = flip_array(emis_probs_2)
    
    fb_init_probs = [1e-30] * gt_icerock[0] + [1] + [1e-30] * (174 - gt_icerock[0])
    
    path1 = []
    path2 = []
    
    probs = get_starting_point(emis_probs_2, fb_init_probs)
    path2.append(probs.index(max(probs)))
    for i in range(len(emis_probs_2[0])-1):
        probs = get_next_column_probs(probs, i+1, emis_probs_2, airice_transition_probs)
        path2.append(probs.index(max(probs)))
    
    probs = get_starting_point(emis_probs_2, fb_init_probs)
    for i in range(len(emis_probs_1[0])):
        probs = get_next_column_probs(probs, i, emis_probs_1, airice_transition_probs)
        path1.append(probs.index(max(probs)))
        
    icerock_feedback = path1 + path2

    # Now write out the results as images and a text file
    write_output_image("air_ice_output_3.png", input_image, airice_simple, airice_hmm, airice_feedback, gt_airice)
    input_image = Image.open(input_filename).convert('RGB')
    write_output_image("ice_rock_output_3.png", input_image, icerock_simple, icerock_hmm, icerock_feedback, gt_icerock)
    with open("layers_output.txt", "w") as fp:
        for i in (airice_simple, airice_hmm, airice_feedback, icerock_simple, icerock_hmm, icerock_feedback):
            fp.write(str(i) + "\n")
