import sys

in_file = 'AI3M_30 mm Sphere high.gcode'  #file name and/or location
out_file = 'sphere_out.gcode'

x_off = 2  #offset variables
y_off = 2
f_num = 1300

extra_before = "before"
extra_after = "after"

# function to alter the x and y values of the G0/1 line
def alter_line (line, x, y): 
    parts = line.split(' ')  # break the line into managable parts
    if line[0:4] == "G0 X" or line[0:4] == "G1 X":  # is it a line we want to alter?
        x_num = float(parts[1][1:])  # remove the X and parse the number into a float
        y_num = float(parts[2][1:])  # remove the Y and parse the number into a float
        x_num += x  # change the number by the y offset amount
        y_num += y  # change the number by the y offset amount
        if len(parts) > 3:
            e = parts[3]
        else:
            e = '' 
        line = "%s X%3.3f Y%3.3f %s" % (parts[0], x_num, y_num, e)  # re-assemble the line
    elif line[0:4] == "G1 F" or line[0:4] == "G0 F":
        if len(parts) == 3:
            e = parts[2]
            line = "%s F%f %s" % (parts[0], f_num, e)  # re-assemble the line
        elif len(parts) >= 4:
            x_num = float(parts[2][1:])  # remove the X and parse the number into a float
            y_num = float(parts[3][1:])  # remove the Y and parse the number into a float
            x_num += x  # change the number by the y offset amount
            y_num += y  # change the number by the y offset amount
            if len(parts) > 4:
                e = parts[4]
            else:
                e = '' 
            line = "%s F%f X%3.3f Y%3.3f %s" % (parts[0], f_num, x_num, y_num, e)  # re-assemble the line

    return line  


f = open(in_file, 'r+')  #opens file
o = open(out_file, 'w')  # open output file for writing, overwrite if exists

saved = []  # initialize an array, just cuz
edit_block = False   # initialize flag to set if we're inside block to edit
for i in f.readlines():  #saves list to temp_list
    # let's just deal with each line of code and not have to re-iterate and store a bunch of arrays 
    if ';' in i: # looks like we're at a command block
        if ';TYPE:SUPPORT-INTERFACE' in i: # further testing to see if top of block for editing
            edit_block = True
            saved = []  # create empty array to start storing values
        else:
            edit_block = False
            if len(saved) > 0:
                # write the saved array to output with altered values
                o.write(extra_before + "\n")  # liner that goes in front of custom code
                for line in saved:
                    new_line = alter_line(line, x_off, y_off)  # call function to change values
                    o.write(new_line)
                o.write(extra_after + "\n")  # liner that goes after custom code
                saved = []  # reset the array
    if edit_block:  # if we're in an edit block, save the line to the saved array
        saved.append(i)
    o.write(i)
print("Done :)")
f.close()
o.close()
sys.exit() # we're done!

