# Python3 Number Examples

print(3 + 2)
# 5

print(3 - 2)
# 1

print(3 * 2)
# 6

print(3 / 2)
# 1.5

# Note: In Python2, result would be 1;
# To accomplish same behavior in Python2,
# use e.g. 3.0 / 2

print(3 // 2)
# 1

print(3 ** 2)
# 9

print(3 % 2)
# 1

print("Meaning of life: " + str(42))
# Meaning of life: 42

if int("42") == 42:
    print("There is meaning!")
# There is meaning!

print(bin(43))
# 0b101011

print(bin(43)[2:])
# 101011

print(bin(43)[2:].zfill(8))
# 00101011

print(int('FF', 16))
# 255

print(hex(255))
# 0xff

print(int('377', 8))
# 255

print(oct(255))
# 0o377

# sum(iterable, start_value)
print(sum([3, 4], 10))
# 17
