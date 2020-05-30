apple = 0
bread = 1
chocolate = 100

while(chocolate > apple+bread):
  dimsum = bread * bread
  apple = apple + dimsum
  bread = bread + 1
  print("apple: {}, bread: {}, dimsum: {}, chocolate: {}".format(apple, bread, dimsum, chocolate))

if (apple > 100):
  print("apple: ", apple)
else:
  print("bread: ", bread)

