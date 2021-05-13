# -BEGIN BLOCK id: 1 type: ordinary
a = 10
b = 12
c = 0
g = 0
h = 0
f = 0
# -END BLOCK id: 1
# -BEGIN BLOCK id: 2 type: if then
if a > b:
# -END BLOCK id: 2
# -BEGIN BLOCK id: 3 type: ordinary
    h = 12
    g = 11
# -END BLOCK id: 3
# -BEGIN BLOCK id: 4 type: else
else:
# -END BLOCK id: 4
# -BEGIN BLOCK id: 5 type: ordinary
    c = 20
    f = 12
# -END BLOCK id: 5
# -BEGIN BLOCK id: 6 type: if then
if g > 10:
# -END BLOCK id: 6
# -BEGIN BLOCK id: 7 type: ordinary
    g = 100
# -END BLOCK id: 7
# -BEGIN BLOCK id: 8 type: for
for i in range(10):
# -END BLOCK id: 8
# -BEGIN BLOCK id: 9 type: ordinary
    t = 10
    f += t
# -END BLOCK id: 9
# -BEGIN BLOCK id: 10 type: ordinary
a = 10
b = 12
# -END BLOCK id: 10
# -BEGIN BLOCK id: 11 type: if then
if a == 10:
# -END BLOCK id: 11
# -BEGIN BLOCK id: 12 type: ordinary
    b = 1
# -END BLOCK id: 12
# -BEGIN BLOCK id: 13 type: elif
elif a < 10:
# -END BLOCK id: 13
# -BEGIN BLOCK id: 14 type: ordinary
    b = 2
# -END BLOCK id: 14
# -BEGIN BLOCK id: 15 type: elif
elif a > 10:
# -END BLOCK id: 15
# -BEGIN BLOCK id: 16 type: ordinary
    b = 3
# -END BLOCK id: 16
# -BEGIN BLOCK id: 17 type: ordinary
print(c)
c = 13
# -END BLOCK id: 17
