import re

with open('average.txt','r') as file:
    file = file.readlines()


time_pattern = re.compile(r'^\d{2}:\d{2}:\d{2}$')
# Test each line against the time pattern

all = []

for line in file:
    if time_pattern.match(line):
        hours, minutes, seconds = list(map(int, line.split(':')))
        hours = hours * 3600
        minutes = minutes * 60
        all.append(hours + minutes + seconds)

print(sum(all) / len(all))