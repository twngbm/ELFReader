import turtle
import reader
total_size = len(reader.filecontent)
turtle.colormode(255)
s_wide = 1600
lm = -s_wide/2
rm = s_wide/2
h = 50
per = total_size/s_wide

section_dict = {}
# section_dict=[offset/per:[name,start_offset/per-rm,end_pos/per-rm,color]]
section_dict["File Header"] = ["File Header", 0x0 /
                               per-rm, (0x0/per+reader.e_ehsize/per)-rm, (0, 0, 0)]
base = reader.e_phoff
x = 30
color_d = int(200/reader.e_phnum)
for ph in reader.pandas_phdata:
    color = (x, x, 235)
    section_dict[base] = [ph[1], base/per-rm,
                          (base/per+reader.e_phentsize/per)-rm, color]
    base += reader.e_phentsize
    x += color_d
base = reader.e_shoff

x = 30
color_d = int(200/reader.e_shnum)
y = 255-int(reader.e_shnum)*2
curf_dict = {}
for sh in reader.shdata:

    section_dict[base] = [sh[1], base/per-rm,
                          (base/per+reader.e_shentsize/per)-rm, (y, x, x)]
    curf_dict[hex(sh[1])] = [(sh[0]/per+reader.e_shentsize/(2*per))-rm, (sh[4]/per +
                                                                         sh[5]/(2*per))-rm, (sh[0]/per+reader.e_shentsize/(2*per))-(sh[4]/per+sh[5]/(2*per)),(y, x, x)]
    base += reader.e_shentsize
    y += 1
    x += color_d
x = 30
color_d = int(200/reader.e_shnum)
y = int(130/reader.e_shnum)
z = 100

for sh in reader.shdata:
    section_dict[sh[4]] = [sh[1], sh[4]/per-rm,
                           (sh[4]/per+sh[5]/per)-rm, (255, z, x)]
    z += y
    x += color_d

print(section_dict)
print(curf_dict)

turtle.speed("fastest")
turtle.penup()
turtle.setpos(lm, h)
turtle.pd()
turtle.setpos(rm, h)
turtle.setpos(rm, -h)
turtle.setpos(lm, -h)
turtle.setpos(lm, h)
turtle.penup()
turtle.home()


x = 255
for key in section_dict:
    turtle.pu()
    turtle.fillcolor(section_dict[key][3])
    turtle.begin_fill()
    turtle.setpos(section_dict[key][1], h)
    turtle.pd()
    turtle.setpos(section_dict[key][1], -h)
    turtle.setpos(section_dict[key][2], -h)
    turtle.setpos(section_dict[key][2], h)
    turtle.setpos(section_dict[key][1], h)
    turtle.end_fill()
    turtle.pu()
turtle.fillcolor((0, 0, 0))

flip = 1
for key in curf_dict:
    turtle.pu()
    turtle.pencolor(curf_dict[key][3])
    turtle.setpos(curf_dict[key][0], -h*flip)
    turtle.seth(180+60*flip)
    radius = curf_dict[key][2]/2
    n_radius=radius/0.866
    turtle.pd()
    turtle.circle(-n_radius*flip, 120)
    turtle.pu()
    flip *= -1
turtle.done()

