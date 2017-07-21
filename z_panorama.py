import trimesh	# mesh_plane  
import shapely
import numpy as np
import sys

Z_RES = 180
C_RES = 360
POLY_TOLERANCE = 1e-2

angs = np.linspace(0,2*np.pi,C_RES)  # angles in radians
X_DIRS = np.cos(angs)
Y_DIRS = np.sin(angs)

# def get_trunc_str(f):
# 	n = 10
# 	s = '{0:.18f}'.format(f)
# 	i, p, d = s.partition('.')
# 	return '.'.join([i, (d+'0'*n)[:n]])

def mod_dist(p1,p2):
	return abs(p1[0] - p2[0]) + abs(p1[1]-p2[1])

def create_pan(fname):	
	mesh = trimesh.load_mesh(fname)
	maxes = np.amax(np.array(mesh.vertices),axis=0)
	mins = np.amin(np.array(mesh.vertices),axis=0)

	center = (maxes + mins)/2
	ranges = maxes - mins

	radius = max(ranges)/np.sqrt(2)
	circ_pts = np.transpose(radius * np.concatenate(([X_DIRS],[Y_DIRS])))

	heights = np.linspace(mins[2],maxes[2],Z_RES)

	for h in range(Z_RES):		

		# print('\n\n\n\n\n\n\n')
		# print(h)
		# print('\n\n\n\n\n\n\n')

		plane_normal = (0,0,1)
		plane_origin = (0,0,heights[h])

		cut_slice = trimesh.intersections.mesh_plane(mesh,plane_normal,plane_origin)
		cut_slice = np.array(cut_slice)
		cut_slice = np.round(cut_slice,decimals = 6)
		
		
		connected_pts = {}

		for l_seg in cut_slice:
			p0 = (l_seg[0][0],l_seg[0][1])
			p1 = (l_seg[1][0],l_seg[1][1])	

			# keep the next line - useful for plotting the slice in Octave when things are hard to understand
			# print(str(l_seg[0][0]) + ',' + str(l_seg[0][1]) + ';' +str(l_seg[1][0]) + ',' + str(l_seg[1][1]) + ';')
			
			# key0 = get_trunc_str(p0[0])+get_trunc_str(p0[1])
			# key1 = get_trunc_str(p1[0])+get_trunc_str(p1[1])

			key0 = p0
			key1 = p1

			if connected_pts.has_key(key0):
				connected_pts[key0].append((p0,p1))
			else:
				connected_pts[key0] = [(p0,p1)]

			if connected_pts.has_key(key1):
				connected_pts[key1].append((p0,p1))
			else:
				connected_pts[key1] = [(p0,p1)]

		open_loops = []
		ordered_polys = []
		
		while len(connected_pts)>0:
			init_pt = connected_pts.iterkeys().next()

			# print('About to enter loop ')
			# for key,value in connected_pts.iteritems():
			# 	print(str(key) + ' ==> \n' + str(value))
			# print('Init :' + str(init_pt))

			poly = []
			poly.append(init_pt)
			curr_pair = connected_pts[init_pt][0]

			connected_pts[init_pt].remove(curr_pair)
			if len(connected_pts[init_pt]) == 0:
				del connected_pts[init_pt]

			if curr_pair[0] == init_pt:
				curr_pt = curr_pair[1]
			else:
				curr_pt = curr_pair[0]			

			while True:
				poly.append(curr_pt)

				# print('\n\n\n\n')
				# print(poly)

				if connected_pts.has_key(curr_pt):
					connected_pts[curr_pt].remove(curr_pair)
					if len(connected_pts[curr_pt]) == 0:
						del connected_pts[curr_pt]
						if curr_pt != init_pt:
							open_loops.append(poly)
							break

				if curr_pt == init_pt:
					# ordered_polys.append(poly)
					ordered_polys.append(shapely.geometry.Polygon(poly))
					break

				curr_pair = connected_pts[curr_pt][0]

				connected_pts[curr_pt].remove(curr_pair)
				if len(connected_pts[curr_pt]) == 0:
					del connected_pts[curr_pt]

				if curr_pair[0] == curr_pt:
					curr_pt = curr_pair[1]
				else:
					curr_pt = curr_pair[0]
								
				# if curr_pt == init_pt:
				# 	poly.append(init_pt)	# closing the loop
				# 	print(len(poly))
				# 	ordered_polys.append(poly)
				# 	break

		for c in range(C_RES):
				intersections = []
				radial_lseg = shapely.geometry.LineString([(center[0],center[1]),tuple(circ_pts[c])])
				for sh_poly in ordered_polys:
					print(sh_poly)
					print(radial_lseg)
					intersections.extend(list(sh_poly.exterior.intersection(radial_lseg).coords))

		# for op in ordered_polys:
		# 	for pt in op:
		# 		print(str(pt[0]) + ',' + str(pt[1]) + ';')
		# 	raw_input('That is on ordered poly in ' + str(heights[h]))
		# for ol in open_loops:
		# 	for pt in op:
		# 		print(str(pt[0]) + ',' + str(pt[1]) + ';')
		# 	raw_input('That is on open loop in ' + str(heights[h]))
		
		# temp_poly = open_loops[0]
		# open_loops.remove(temp_poly)

		# while len(open_loops) > 0:			
		# 	min_dist_start = [min(POLY_TOLERANCE,mod_dist(temp_poly[0]),temp_poly[len(temp_poly)-1]),-1,True]
		# 	min_dist_end = [min(POLY_TOLERANCE,mod_dist(temp_poly[0]),temp_poly[len(temp_poly)-1]),-1,True]

		# 	for count in range(len(open_loops)):
		# 		start_start = mod_dist(temp_poly[0],open_loops[count][0])
		# 		if start_start< min_dist_start[0]:
		# 			min_dist = [start_start,count,True]

		# 		start_end = mod_dist(temp_poly[0],open_loops[count][len(open_loops[count]) - 1])
		# 		if start_end < min_dist_start[0]:
		# 			min_dist = [start_end,count,False]

		# 		end_start = mod_dist(temp_poly[len(temp_poly)-1],open_loops[count][0])
		# 		if end_start < min_dist_end[0]:
		# 			min_dist = [end_start,count,True]

		# 		end_end = mod_dist(temp_poly[len(temp_poly)-1],open_loops[count][len(open_loops[count]) - 1])
		# 		if end_end < min_dist_end[0]:
		# 			min_dist = [end_end,count,False]

		# 	if min_dist[1] != -1:
		# 		if min_dist[2] == False:
		# 			temp_poly.reverse()
		# 		if min_dist[3] == False:
		# 			open_loops[min_dist[1]].reverse()
		# 		temp_poly.extend(open_loops[min_dist[1]])
		# 		open_loops.remove(open_loops[min_dist[1]])
		# 		# loop must keep running, as the end points of temp_poly have changed

		# 	else:
		# 		if mod_dist(temp_poly[0]),temp_poly[len(temp_poly)-1] < POLY_TOLERANCE:




	print(fname)



if len(sys.argv)>1:
	create_pan(sys.argv[1])
	exit()

flist_mn10test = [line.rstrip('\n') for line in open('test10.txt')]
for model in flist_mn10test:
	create_pan(model)








		# single_lines = []
		# del_keys = []

		# all_lists_pairs = True
		# for key,value in connected_pts.iteritems():
		# 	if len(value) == 1:

		# 		if value[0][0] == key:
		# 			other_pt = value[0][1]
		# 		else:
		# 			other_pt = value[0][0]

		# 		print("huiasfhauisdhf\n\n")
		# 		print(connected_pts[other_pt])

		# 		if len(connected_pts[other_pt]) > 2:
		# 			connected_pts[other_pt].remove(value)
		# 			del_keys.append(key)

		# 		else:
		# 			single_lines.extend(value)
		# 			all_lists_pairs = False	

		# for key in del_keys:
		# 	del connected_pts[key]
				
		# if all_lists_pairs == False:
		# 	print('Error: not all lists are of size > 2 at height ' + str(heights[h]))
		# 	print(single_lines)
		# 	raw_input("Continue?")
		# 	# for key,value in connected_pts.iteritems():
		# 	# 	print(value)
		
		# print('\n\n\n\n\n\n')



