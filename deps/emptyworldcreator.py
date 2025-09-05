import pyperclip
x=int(input("Enter the X value "))
y=int(input("Enter the y value "))
world=""
for i in range(y):
    world=world+"0"
    for j in range(x-1):
        world=world+" 0"
    world=world+"\n"

print(world)
pyperclip.copy(world)