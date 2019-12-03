# https://adventofcode.com/2019/day/3


def check_intersec(line, point1, point2):
   for i in range(len(line)-1):
      if point1[0] == point2[0] and line[i][1] == line[i+1][1]:
         if min(point1[1], point2[1]) < line[i][1] and max(point1[1], point2[1]) > line[i][1] and min(line[i][0], line[i+1][0]) < point1[0] and max(line[i][0], line[i+1][0]) > point1[0]:
            #print(f"intersec [{point1}, {point2}] with [{line[i]}, {line[i+1]}] at ({point1[0]}, {line[i][1]})")
            return abs(point1[0]) + abs(line[i][1])
      elif point1[1] == point2[1] and line[i][0] == line[i+1][0]:
         if min(point1[0], point2[0]) < line[i][0] and max(point1[0], point2[0]) > line[i][0] and min(line[i][1], line[i+1][1]) < point1[1] and max(line[i][1], line[i+1][1]) > point1[1]:
            #print(f"intersec [{point1}, {point2}] with [{line[i]}, {line[i+1]}] at ({point1[1]}, {line[i][0]})")
            return abs(point1[1]) + abs(line[i][0])
        
   return -1


def puzzle1(input_f):
   line1 = [(0,0)]
   count = 0
   min_dist = 0
   for instruction in input_f.readline().split(","):
      direction = instruction[0]
      if direction == "U":
         line1.append((line1[count][0],line1[count][1]+int(instruction[1:])))
      if direction == "D":
         line1.append((line1[count][0],line1[count][1]-int(instruction[1:])))
      if direction == "L":
         line1.append((line1[count][0]-int(instruction[1:]),line1[count][1]))
      if direction == "R":
         line1.append((line1[count][0]+int(instruction[1:]),line1[count][1]))
      count += 1
   prev_point = (0,0)
   for instruction in input_f.readline().split(","):
      direction = instruction[0]
      curr_point = (0,0)
      if direction == "U":
         curr_point = (prev_point[0], prev_point[1]+int(instruction[1:]))
      if direction == "D":
         curr_point = (prev_point[0], prev_point[1]-int(instruction[1:]))
      if direction == "L":
         curr_point = (prev_point[0]-int(instruction[1:]), prev_point[1])
      if direction == "R":
         curr_point = (prev_point[0]+int(instruction[1:]), prev_point[1])
      
      # check intersection
      dist = check_intersec(line1, prev_point, curr_point)
      if dist != -1:
         if min_dist == 0:
            min_dist = dist
         else:
            min_dist = min(min_dist, dist)
      prev_point = curr_point[:]
   return min_dist


if __name__ == "__main__":
   with open("res/day3.txt") as input_f:
      print(puzzle1(input_f))