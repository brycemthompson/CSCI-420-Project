import sys
from math import sqrt

# Constants
COLOR_RED = "ff0000"
COLOR_MAGENTA = "ff00ff"


class Point:
    def __init__(self, latitude, longitude, speed, angle, color, time):
        self.latitude = latitude
        self.longitude = longitude
        self.speed = speed
        self.angle = angle
        self.color = color
        self.time = time

    def change_color(self, color):
        self.color = color


def emit_header(fp_out):
    fp_out.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    fp_out.write("<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n")
    fp_out.write("  <Document>\n")
    fp_out.write("    <name>Paths</name>\n")
    fp_out.write("    <description>Examples of paths. Note that the tessellate tag is by default\n")
    fp_out.write("      set to 0. If you want to create tessellated lines, they must be authored\n")
    fp_out.write("      (or edited) directly in KML.</description>\n")


def emit_styles(fp_out):
    fp_out.write("    <Style id=\"greenLineGreenPoly\">\n")
    fp_out.write("      <LineStyle>\n")
    fp_out.write("        <color>5014F032</color>\n")
    fp_out.write("        <width>4</width>\n")
    fp_out.write("      </LineStyle>\n")
    fp_out.write("      <PolyStyle>\n")
    fp_out.write("        <color>5014F032</color>\n")
    fp_out.write("      </PolyStyle>\n")
    fp_out.write("    </Style>\n")
    fp_out.write("    <Style id=\"blueLineGreenPoly\">\n")
    fp_out.write("      <LineStyle>\n")
    fp_out.write("        <color>ffff0000</color>\n")
    fp_out.write("        <width>4</width>\n")
    fp_out.write("      </LineStyle>\n")
    fp_out.write("      <PolyStyle>\n")
    fp_out.write("        <color>ffff0000</color>\n")
    fp_out.write("      </PolyStyle>\n")
    fp_out.write("    </Style>\n")
    fp_out.write("    <Style id=\"yellowLineGreenPoly\">\n")
    fp_out.write("      <LineStyle>\n")
    fp_out.write("        <color>5014F0E6</color>\n")
    fp_out.write("        <width>4</width>\n")
    fp_out.write("      </LineStyle>\n")
    fp_out.write("      <PolyStyle>\n")
    fp_out.write("        <color>5014F0E6</color>\n")
    fp_out.write("      </PolyStyle>\n")
    fp_out.write("    </Style>\n")


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


def emit_coordinates(fp_out, lines):
    for item in lines:
        fp_out.write(str(item.latitude) + "," + str(item.longitude) + "," + str(item.speed) + "\n")


def emit_placemarker_end(fp_out):
    fp_out.write("        </coordinates>\n")
    fp_out.write("      </LineString>\n")
    fp_out.write("    </Placemark>\n")


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


def emit_common_sign(fp_out, item):
    fp_out.write("    <Placemark>\n")
    fp_out.write("        <description>Red PIN for A Stop</description>\n")
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

def emit_trailer(fp_out):
    fp_out.write("  </Document>\n")
    fp_out.write("</kml>\n")


def read_and_parse(filename):
    file = open(filename, "r")

    # Remove the initial 5 lines
    for line_idx in range(0, 5):
        file.readline()

    # Split and strip the values
    contents = file.read()
    contents_list = contents.split("\n")
    stripped_list = []
    for value in contents_list:
        stripped_list.append(value.strip())
    return stripped_list


def clean_lines(lines):
    clean = []
    for value in lines:
        temp = value.split(",")
        RMC = value.count("GPRMC")
        GGA = value.count("GPGGA")
        if RMC == 1 and GGA == 0:
            clean.append((temp[3], temp[4], temp[5], temp[6], temp[7], temp[8], temp[1]))
    del lines
    return clean


def calculate_lat_long(clean):
    final = []
    for value in clean:
        hold_num = float(value[0]) // 100
        degrees = float(value[0]) % 100
        degrees = degrees / 60

        if value[1] == "N":
            long = str(hold_num + degrees)
        else:
            long = "-" + str(hold_num + degrees)

        hold_num = float(value[2]) // 100
        degrees = float(value[2]) % 100
        degrees = degrees / 60

        if value[3] == "E":
            lat = str(hold_num + degrees)
        else:
            lat = "-" + str(hold_num + degrees)

        final.append(Point(lat, long, value[4], value[5], COLOR_MAGENTA, value[6]))

    del clean
    return final


def get_distance(pos_1, pos_2):
    lat_diff = abs(float(pos_1.latitude) - float(pos_2.latitude)) * 364000
    long_diff = abs(float(pos_1.longitude) - float(pos_2.longitude)) * 288200
    return long_diff + lat_diff


def get_degrees(pos_1, pos_2, pos_3):
    temp = (float(pos_1.angle) - float(pos_2.angle) + 180 + 360) % 360 - 180
    if float(pos_1.angle) < float(pos_3.angle) < float(pos_2.angle):
        return temp, "right"
    elif float(pos_2.angle) < float(pos_3.angle) < float(pos_1.angle):
        return temp, "left"
    elif float(pos_3.angle) > float(pos_1.angle) > float(pos_2.angle) or float(pos_1.angle) > float(pos_2.angle) > float(pos_3.angle):
        return temp, "right"
    elif float(pos_2.angle) > float(pos_1.angle) > float(pos_3.angle) or float(pos_3.angle) > float(pos_2.angle) > float(pos_1.angle):
        return temp, "left"
    else:
        return temp, "left"


def get_time_diff(prev_point, second_point):
    return abs(float(second_point.time) - float(prev_point.time))


def try_to_append(stops, second_point):
    temp = (True, None)
    for point in stops:
        dist = get_distance(point, second_point)
        if dist < 1000:
            temp = (False, point)
            break
    if temp[0]:
        stops.append(second_point)
    return temp


def is_stop_in_common_locs(stop, common_locs):
    temp = (True, None)
    for point in common_locs:
        dist = get_distance(point, stop)
        if dist < 1000:
            temp = (False, point)
            break
    return temp


def merge_stops(stops):
    new_stops = []
    common_locs = []
    for item in stops:
        for stop in item:
            bool_1, point = is_stop_in_common_locs(stop, common_locs)
            if bool_1:
                bool_2, point = try_to_append(new_stops, stop)
                if not bool_2:
                    new_stops.remove(point)
                    common_locs.append(point)
    return new_stops, common_locs

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
    stops = []
    for final in list_of_lat_longs:
        temp_stops = []
        not_turn = []
        idx = 0
        while idx < len(final):
            idx2 = idx + 1
            while idx2 < len(final):
                pos1 = final[idx]
                pos2 = final[idx2]
                pos3 = final[int(idx/2)]
                if get_distance(pos1, pos2) > 200:
                    result = get_degrees(pos1, pos2, pos3)
                    if abs(result[0]) > 65 and ((abs(float(pos1.latitude) - float(pos2.latitude)) * 364000) > 50 and (abs(float(pos1.longitude) - float(pos2.longitude)) * 288200 > 50)):
                        temp_array = final[idx-1:idx2+1]
                        nf.append((not_turn, "not"))
                        nf.append((temp_array, result[1]))
                        not_turn = []
                        idx = idx2
                        idx2 = idx - 1
                    else:
                        not_turn.append(final[idx])
                        idx += 1
                idx2 += 1

            if idx2 >= len(final):
                idx = idx2
            idx += 1
        if not_turn:
            nf.append((not_turn, "not"))

        idx = 0
        prev_point = final[0]
        second_point = final[0]
        while idx < len(final):
            current_point = final[idx]
            if current_point.latitude == prev_point.latitude and current_point.longitude == prev_point.longitude:
                second_point = current_point
            else:
                # check time between second point and prev point
                time_diff = get_time_diff(prev_point, second_point)
                if time_diff >= 2:
                    try_to_append(temp_stops, second_point)
                prev_point = current_point
                second_point = current_point
            idx += 1
        stops.append(temp_stops)

    fp_out = open(arguments[-1], "w")

    emit_header(fp_out)
    emit_styles(fp_out)

    for item in nf:
        if item[1] == "not":
            emit_placemarker_start(fp_out, "blueLineGreenPoly")
            emit_coordinates(fp_out, item[0])
            emit_placemarker_end(fp_out)
        elif item[1] == "right":
            emit_placemarker_start(fp_out, "yellowLineGreenPoly")
            emit_coordinates(fp_out, item[0])
            emit_placemarker_end(fp_out)
        elif item[1] == "left":
            emit_placemarker_start(fp_out, "greenLineGreenPoly")
            emit_coordinates(fp_out, item[0])
            emit_placemarker_end(fp_out)

    (stops, common_loc) = merge_stops(stops)
    for item in stops:
        emit_stop_sign(fp_out, item)
    for item in common_loc:
        emit_common_sign(fp_out, item)

    emit_trailer(fp_out)

if __name__ == "__main__":
    main(sys.argv)
