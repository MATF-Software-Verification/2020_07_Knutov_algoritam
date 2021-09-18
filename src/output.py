# -BEGIN BLOCK id: 1 type: ordinary
t=f=1
# -END BLOCK id: 1
# -BEGIN BLOCK id: 2 type: for
for i in range(10):
# -END BLOCK id: 2
# -BEGIN BLOCK id: 3 type: ordinary
    t = 10
    f += t
# -END BLOCK id: 3
# -BEGIN BLOCK id: 4 type: ordinary
print(f)
# -END BLOCK id: 4
