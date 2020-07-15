
            # wait for new laser data
            new_laser_data_flag = False 
            while not new_laser_data_flag:pass
            last_laser_data = laser_data

            #   do for all particles
            for index , particle in enumerate(particles):

                #   calculate the start and the end of sensor line (the lenth is 0.4)
                #   [start_point , end_point]
                sensor_line = [ [particle[0],particle[1]] , \
                    [ 0.4*math.cos(particle[2]*math.pi/180)+particle[0] , \
                        0.4*math.sin(particle[2]*math.pi/180)+particle[1] ] ]

                #   distance of particle to all walls that faces it
                particle_distance_to_walls = [] 
                #   the  intersection point to all those walls
                intersection_points = []

                for line in all_map_lines:

                    #   calculate the intersection point 
                    intersection_point = map.intersection(line[0],line[1] , sensor_line[0],sensor_line[1])

                    #   check for the existance of intersection point 
                    if intersection_point :
                        #   calculate the distance of intersection point and particle position
                        particle_distance_to_walls.append( \
                            math.sqrt( (particle[0]-intersection_point[0])**2 + (particle[1]-intersection_point[1])**2 ))
                        #   save the intersection point position
                        intersection_points.append(intersection_point)

                #   find the minimum distance and its index in the list
                particles_distance , intersection_index = min( (i , j) for \
                    (i , j) in enumerate(particle_distance_to_walls))

                #   TODO: nastaran plot this . this line is the particle sensor line
                #   particle sensor line [ start_point , end_point ]
                particle_sensor_line = [ [ particle[0] , particle[1] ] , intersection_points[intersection_index] ]

                #   sensor model is a normal distribution [mean,var]
                #   mean is the distance that particles read 
                #   var is 0.000097
                weights[index] += stats.norm(particles_distance, 0.000097).pdf(last_laser_data)

            #   normalize the weights
            weights /= np.sum(weights)
