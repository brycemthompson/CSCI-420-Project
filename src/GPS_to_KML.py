import sys


# Point class
# Description: Helper class describing teh various parts of a 'Point', including the latitude, longitude, speed, angle,
# color, and time instance of the point
class Point:
    def __init__(self, latitude, longitude, speed, angle, time):
        self.latitude = latitude
        self.longitude = longitude
        self.speed = speed
        self.angle = angle
        self.time = time


# calculate_lat_long function
# Description: Helper function that takes in the clean data and converts it into our Point data type,
# while also converting the given data into real 'latitude' and 'longitude' values
def calculate_lat_long(clean):
    final = []

    # Loop through the clean values
    for value in clean:
        hold_num = float(value[0]) // 100
        degrees = float(value[0]) % 100
        degrees = degrees / 60

        # Grab the longitude
        if value[1] == "N":
            long = str(hold_num + degrees)
        else:
            long = "-" + str(hold_num + degrees)

        hold_num = float(value[2]) // 100
        degrees = float(value[2]) % 100
        degrees = degrees / 60

        # Grab the latitude
        if value[3] == "E":
            lat = str(hold_num + degrees)
        else:
            lat = "-" + str(hold_num + degrees)

        # Create a new point with the values and append to the final list.
        final.append(Point(lat, long, value[4], value[5], value[6]))

    del clean
    return final


# clean_lines function
# Description: Helper function that takes in the raw data from the gps files and cleans it by
# removing lines that don't make sense and values that we don't need
def clean_lines(lines):
    # Initialize values
    clean = []
    ignoreValue = False
    last_lat = 0
    last_long = 0
    curr_lat = 0
    curr_long = 0

    # Loop through the provided lines and separate by comma
    for value in lines:
        temp = value.split(",")
        # If we have a GPRMC, then we use elements 3 and 5
        if temp[0] == "$GPRMC":
            if len(temp) > 5:  # Ensure the values exist
                curr_lat = float(temp[3])
                curr_long = float(temp[5])
            else:
                curr_lat = last_lat
                curr_long = last_long
        # If we have a GPGGA, then we use elements 2 and
        elif temp[0] == "$GPGGA":
            if len(temp) > 4:  # Ensure the values exist
                curr_lat = float(temp[2])
                curr_long = float(temp[4])
            else:
                curr_lat = last_lat
                curr_long = last_long

        # Calculate the difference between the last coordinates
        lat_diff = abs(curr_lat - last_lat)
        long_diff = abs(curr_long - last_long)

        # If there is a latitude or longitude outlier, ignore it
        if lat_diff < 7800 or long_diff < 7800:
            RMC = value.count("GPRMC")
            GGA = value.count("GPGGA")
            if RMC == 1 and GGA == 0:
                # Loop through the elements of temp (the parsed lined)
                for idx in range(0, len(temp)):
                    # If a value is missing, ignore the value
                    if temp[idx] is None:
                        ignoreValue = True
                # If we don't have any missing values, add the line to the cleaned list.
                if not ignoreValue:
                    clean.append((temp[3], temp[4], temp[5], temp[6], temp[7], temp[8], temp[1]))
                ignoreValue = False
    del lines
    return clean


# emit_common_sign function
# Description: Helper function that takes in a point and outputs a place mark into the KML file
# that represents a 'Blue Common Location'
def emit_common_sign(fp_out, item):
    fp_out.write("    <Placemark>\n")
    fp_out.write("        <description>Blue PIN for A Common Location</description>\n")
    fp_out.write("        <Style id=\"normalCommon\">\n")
    fp_out.write("            <IconStyle>\n")
    fp_out.write("                <color>ffff0000</color>\n")
    fp_out.write("                    <Icon>\n")
    fp_out.write("                        <href>http://maps.google.com/mapfiles/kml/paddle/blu-blank.png</href>\n")
    fp_out.write("                    </Icon>\n")
    fp_out.write("            </IconStyle>\n")
    fp_out.write("        </Style>\n")
    fp_out.write("        <Point>\n")
    fp_out.write("            <coordinates>" + str(item.latitude) + "," + str(item.longitude) + "," + str(item.speed) + "</coordinates>\n")
    fp_out.write("        </Point>\n")
    fp_out.write("    </Placemark>\n")


# emit_coordinates function
# Description: Helper function that adds each point in the line to the KML file
def emit_coordinates(fp_out, lines):
    for item in lines:
        fp_out.write(str(item.latitude) + "," + str(item.longitude) + "," + str(item.speed) + "\n")


# emit_header function
# Description: Helper function called first for every run that outputs the start of a KML
def emit_header(fp_out):
    fp_out.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    fp_out.write("<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n")
    fp_out.write("  <Document>\n")
    fp_out.write("    <name>Paths</name>\n")
    fp_out.write("    <description>Examples of paths. Note that the tessellate tag is by default\n")
    fp_out.write("      set to 0. If you want to create tessellated lines, they must be authored\n")
    fp_out.write("      (or edited) directly in KML.</description>\n")


# emit_placemarker_end function
# Description: Helper function that ends the place marker, so that a new place marker (for a new line) can be created
def emit_placemarker_end(fp_out):
    fp_out.write("        </coordinates>\n")
    fp_out.write("      </LineString>\n")
    fp_out.write("    </Placemark>\n")


# emit_placemarker_start function
# Description: Helper function that emits the start of a place marker, used specifically for the 'path'
# that the GPS is tracking. It takes in a specific style to make the line, blue, green, or yellow.
def emit_placemarker_start(fp_out, style):
    fp_out.write("    <Placemark>\n")
    fp_out.write("      <name>Absolute Extruded</name>\n")
    fp_out.write("      <description>Transparent green wall with yellow outlines</description>\n")
    fp_out.write("      <styleUrl>#" + style + "</styleUrl>\n")
    fp_out.write("      <LineString>\n")
    fp_out.write("        <extrude>1</extrude>\n")
    fp_out.write("        <tessellate>1</tessellate>\n")
    fp_out.write("        <altitudeMode>absolute</altitudeMode>\n")
    fp_out.write("        <coordinates>  ")


# emit_stop_sign function
# Description: Helper function that takes in a point and outputs a place mark into the KML file
# that represents a 'Red Stop'
def emit_stop_sign(fp_out, item):
    fp_out.write("    <Placemark>\n")
    fp_out.write("        <description>Red PIN for A Stop</description>\n")
    fp_out.write("        <Style id=\"normalPlacemark\">\n")
    fp_out.write("            <IconStyle>\n")
    fp_out.write("                <color>ff0000ff</color>\n")
    fp_out.write("                    <Icon>\n")
    fp_out.write("                        <href>http://maps.google.com/mapfiles/kml/paddle/1.png</href>\n")
    fp_out.write("                    </Icon>\n")
    fp_out.write("            </IconStyle>\n")
    fp_out.write("        </Style>\n")
    fp_out.write("        <Point>\n")
    fp_out.write("            <coordinates>" + str(item.latitude) + "," + str(item.longitude) + "," + str(item.speed) + "</coordinates>\n")
    fp_out.write("        </Point>\n")
    fp_out.write("    </Placemark>\n")


# emit_styles function
# Description: Following the header, we have various 'styles' that get used throughout the KML file which are emitted
# to be used later
def emit_styles(fp_out):
    fp_out.write("    <Style id=\"yellowLineGreenPoly\">\n")
    fp_out.write("      <LineStyle>\n")
    fp_out.write("        <color>5014F0E6</color>\n")
    fp_out.write("        <width>4</width>\n")
    fp_out.write("      </LineStyle>\n")
    fp_out.write("      <PolyStyle>\n")
    fp_out.write("        <color>5014F0E6</color>\n")
    fp_out.write("      </PolyStyle>\n")
    fp_out.write("    </Style>\n")


# emit_trailer function
# Description: Helper function that emits the end of the KML file
def emit_trailer(fp_out):
    fp_out.write("  </Document>\n")
    fp_out.write("</kml>\n")


# read_and_parse function
# Description: Helper function takes in a single file and parses all the GPS data in that one file, and returns the data
def read_and_parse(filename):
    file = open(filename, "r")

    # Remove the initial 5 lines
    for line_idx in range(0, 5):
        file.readline()

    # Split and strip the values
    contents = file.read()
    contents_list = contents.split("\n")
    stripped_list = []

    # Loop through and append the stripped values
    for value in contents_list:
        stripped_list.append(value.strip())
    return stripped_list


# main function
# Description: Main function that handles the running parameters and calls to the helper functions
def main(argv):
    # Collect the argCount for argument checking
    argCount = len(argv)
    argIdx = 0
    arguments = []

    # Check for AT LEAST one text file
    if len(argv) < 3:
        print("You must enter at least one text file and one kml file output name to run this program.")
        exit(0)
    if argv[1][argv[1].index("."):] != ".txt":
        print("You must enter at least one text file to run this program.")
        exit(0)

    # Given we have a single text file, check the rest of the arguments.
    for arg in argv:
        extension = arg[arg.index("."):]
        # If we are on index 0, the value is the python file. Skip it.
        if argIdx > 0:
            if argIdx == argCount - 1:
                # Check that this argument is the KML file
                if extension.lower() != ".kml":
                    print("The last argument must be a KML file!")
                    exit(0)
            elif argIdx < argCount:
                # Check that these arguments are text files
                if extension.lower() != ".txt":
                    print("You must only enter text files prior to the single KML file!")
                    exit(0)
                argIdx += 1
            arguments.append(arg)
        else:
            argIdx += 1

    # Read in, clean, and calculate the latitudes and longitudes from the text files.
    list_of_lat_longs = []
    argIdx = 0
    for arg in arguments:
        if argIdx != len(arguments) - 1:
            raw_lines = read_and_parse(arg)
            clean = clean_lines(raw_lines)
            list_of_lat_longs.append(calculate_lat_long(clean))
            argIdx += 1

    nf = []
    # for each file of gps data
    for final in list_of_lat_longs:
        not_turn = []
        idx = 0
        # go through each point. Attempt to locate turns
        while idx < len(final):
            not_turn.append(final[idx])
            idx += 1

        nf.append((not_turn, "not"))

    fp_out = open(arguments[-1], "w")

    # output some KML headers and styles
    emit_header(fp_out)
    emit_styles(fp_out)

    # for each gps file
    for item in nf:
        # print all the non-turns to kml file
        if item[1] == "not":
            emit_placemarker_start(fp_out, "yellowLineGreenPoly")
            emit_coordinates(fp_out, item[0])
            emit_placemarker_end(fp_out)

    # print the trailer to kml file
    emit_trailer(fp_out)


if __name__ == "__main__":
    main(sys.argv)
