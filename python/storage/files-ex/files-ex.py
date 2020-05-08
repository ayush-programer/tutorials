# Python3 File Examples

try:
    with open("crew.txt") as crew_file:
        crew = crew_file.read()

except FileNotFoundError:
    print("Oh no! File crew.txt not found!")

else:
    print("Crew members are:")

    for crew_member in crew.split():
        print("\t* " + crew_member)
# Crew members are:
#	* Picard
#	* Riker
#	* Data
#	* Geordi
#	* Worf
#	* Wesley
#	* Beverly
#	* Deanna

# Note: The 'with' keyword is similar
# to try/catch; it will also close the
# file/stream automatically when done

print("We will repeat crew members:")

try:
    with open("crew.txt") as crew_file:
        for crew_member in crew_file:
            # rstrip() to remove \n at line end
            print("\t* " + crew_member.rstrip())

except FileNotFoundError:
    print("We could not repeat crew members")
# Crew members are:
#	* Picard
#	* Riker
#	* Data
#	* Geordi
#	* Worf
#	* Wesley
#	* Beverly
#	* Deanna

try:
    with open("crew.txt") as crew_file:
        crew = crew_file.readlines()

except FileNotFoundError:
    print("Oh no, could not find crew.txt!")

else:
    for crew_number in range(0, len(crew)):
        crew[crew_number] = crew[crew_number].rstrip()

    print("Once more:")
    print(crew)

finally:
    print("File either opened or failed.")
# Once more:
# ['Picard', 'Riker', 'Data', 'Geordi', 'Worf', 'Wesley', 'Beverly', 'Deanna']
# File either opened or failed.

# Note: Block under 'finally' will run after try
# finishes whether there was an exception or not

with open("werc.txt", "w") as werc_file:
    for crew_member in crew:
        werc_file.write("".join(reversed(crew_member)).title() + "\n")

with open("werc.txt", "a") as werc_file:
    werc_file.write("Q\n")

try:
    print("Alternate universe crew:")
    with open("werc.txt") as werc_file:
        for werc in werc_file.readlines():
            print("\t- " + werc.rstrip())

except FileNotFoundError:
    pass    # do nothing
# Alternate universe crew:
#       - Dracip
#       - Rekir
#       - Atad
#       - Idroeg
#       - Frow
#       - Yelsew
#       - Ylreveb
#       - Annaed
#       - Q
