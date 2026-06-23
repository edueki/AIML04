# Dictionary
# Unordered
# Mutable

user1_data = {"first_name":"pr","last_name":"reddy", "mobile":"999999", "email":"pr@gmail.com", "number": 5}
user2_data = {"last_name":"reddy", "mobile":"999999", "email":"pr@gmail.com", "number": 5, "first_name":"pr"}

# Control loops
# for

# for i in user1_data.values():
#     print (f"{i}")

user_data = ["pr","reddy", "999999", "pr@gmail.com", "12345", "Feb 2nd 2000", 5, True]

print (__name__)
for i in user_data:
    print ("Inside for loop")
    print(i)
    print ("loop completed! start next iteration")


# print (user1_data.items())
# if user1_data == user2_data:
#     print("user1_data and user2_data are equal")
# else:
#     print("user1_data and user2_data are not equal")





# set data collection
# Immutable Data Type
# unordered
# user1_data = {"pr","reddy", "999999", "pr@gmail.com", "12345", "Feb 2nd 2000", 5, 5, 5}
#
# user2_data = {"pr","reddy", "pr@gmail.com", "12345", "Feb 2nd 2000", 5, "999999"}
#
# if user1_data == user2_data:
#     print ("Both users profile is matching!")
# else:
#     print ("Both users profile is not matching!")


# Tuple data collection
# Ordered Data Type
# Immutable Data Type
# user1_data = ("pr","reddy", "999999", "pr@gmail.com", "Feb 2nd 2000", 5, 5, 5, "12345")
# user2_data = ("pr","reddy", "999999", "pr@gmail.com", "12345", "Feb 2nd 2000", 5, 5, 5)
#
# if user1_data == user2_data:
#     print ("Both users profile is matching!")
# else:
#     print ("Both users profile is not matching!")

# var1, var3 =  5, 10
#
# var2 = ( 10, 12 )
#
# print (var1)
# print (var2)





# # registration app
#
# # Data Layer
# # user_data = ["pr","reddy", "999999", "pr@gmail.com", "12345", "Feb 2nd 2000", 5, True]
#
# # print (type(user_data))
# # Data processing
# # # print (type(user_data[-5]))
# # user_data[-5] = user_data[-5].upper()
# # print (user_data)
# user_data = ["pr","reddy", "999999", ["pr@gmail.com", "reddy@gmail.com"], "12345", "Feb 2nd 2000", "5"]
# print ( len(user_data) )
#
# user_data[3].insert(0, "new@gmail.com")
#
# print (user_data)
#
# ####
# # name = "PR Reddy"
# # print ( name.split("e") )
#
#
# # Business Logic Layer
