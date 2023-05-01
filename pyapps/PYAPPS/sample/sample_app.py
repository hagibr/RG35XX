from pathlib import Path

cities = ["This is Delhi \n", "This is Paris \n", "This is London \n"]
 
# Writing to file
with open(Path(__file__).parent / "cities.txt", "w") as f:
    # Writing data to a file
    f.write("Hello \n")
    f.writelines(cities)
