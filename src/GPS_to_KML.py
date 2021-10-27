from math import sqrt

class Point:
    def __init__(self, latitude, longitude, speed, angle, color):
        self.latitude = latitude
        self.longitude = longitude
        self.speed = speed
        self.angle = angle
        self.color = color

    def change_color(self, color):
        self.color = color

DEFAULT_COLOR = "BLACK"


def emit_header(fp_out):
    """
    Writes out the header of the KML file
    :param fp_out: file to write to
    :return: None
    """
    fp_out.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    fp_out.write("<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n")
    fp_out.write("  <Document>\n")
    fp_out.write("    <name>Paths</name>\n")
    fp_out.write("    <description>Examples of paths. Note that the tessellate tag is by default\n")
    fp_out.write("      set to 0. If you want to create tessellated lines, they must be authored\n")
    fp_out.write("      (or edited) directly in KML.</description>\n")


def emit_style(fp_out, hex):
    fp_out.write("    <Style id=\"greenLineGreenPoly\">\n")
    fp_out.write("      <LineStyle>\n")
    fp_out.write("        <color>" + str(hex) + "</color>\n")
    fp_out.write("        <width>2</width>\n")
    fp_out.write("      </LineStyle>\n")
    fp_out.write("      <PolyStyle>\n")
    fp_out.write("        <color>" + str(hex) + "</color>\n")
    fp_out.write("      </PolyStyle>\n")
    fp_out.write("    </Style>\n")


def emit_coordinates(fp_out, lines):
    for item in lines:
        fp_out.write(str(item.latitude) + "," + str(item.longitude) + "," + str(item.speed) + "\n")


def emit_close_placemark(fp_out):
    fp_out.write("        </coordinates>\n")
    fp_out.write("      </LineString>\n")
    fp_out.write("    </Placemark>\n")

def emit_open_placemark(fp_out, hex):
    fp_out.write("    <Placemark>\n")
    fp_out.write("      <name>Absolute Extruded</name>\n")
    fp_out.write("      <description>Transparent green wall with yellow outlines</description>\n")
    fp_out.write("      <styleUrl>#greenLineGreenPoly</styleUrl>\n")
    fp_out.write("      <LineString>\n")
    fp_out.write("        <extrude>1</extrude>\n")
    fp_out.write("        <tessellate>1</tessellate>\n")
    fp_out.write("        <altitudeMode>absolute</altitudeMode>\n")
    fp_out.write("        <coordinates>  ")

def emit_coordinates(fp_out, lines):
    """
    Writes out coordinates based on the given .txt information
    :param fp_out: file to write to
    :param lines: lines of data containing coordinates
    :return: None
    """
    for item in lines:
        fp_out.write(str(item[0]) + "," + str(item[1]) + "," + str(item[2]) + "\n")


def emit_trailer(fp_out):
    """
    Writes out the trailer of the KML file
    :param fp_out: file to write to
    :return: None
    """
    fp_out.write("        </coordinates>\n")
    fp_out.write("      </LineString>\n")
    fp_out.write("    </Placemark>\n")
    fp_out.write("  </Document>\n")
    fp_out.write("</kml>\n")


def read_and_parse(filename):
    """
    Parses lines of the given .txt file
    :param filename: name of the file to parse
    :return: array of strings from the lines of the given file
    """
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
    """
    Takes lines of GPS data and extracts the information pertinent to writing a KML file
    :param lines: lines of GPS data
    :return: array of GPS data to be written to the KML file
    """
    clean = []
    for value in lines:
        temp = value.split(",")
        RMC = value.count("GPRMC")
        GGA = value.count("GPGGA")
        if RMC == 1 and GGA == 0:
            clean.append((temp[3], temp[4], temp[5], temp[6], temp[7], temp[8]))
    del lines
    return clean


def calculate_lat_long(clean):
    """
    Calculates the latitude and longitude for each line of GPS data
    :param clean: cleaned lines of GPS data
    :return: array of tuples containing coordinates and speeds
    """
    final = []
    for value in clean:
        hold_num = float(value[0]) // 100
        degrees = float(value[0]) % 100
        degrees = degrees / 60

        if(value[1] == "N"):
            long = str(hold_num + degrees)
        else:
            long = "-" + str(hold_num + degrees)

        hold_num = float(value[2]) // 100
        degrees = float(value[2]) % 100
        degrees = degrees / 60

        if(value[3] == "E"):
            lat = str(hold_num + degrees)
        else:
            lat = "-" + str(hold_num + degrees)

        final.append(Point(lat, long, value[4], value[5], DEFAULT_COLOR))

    del clean
    return final


def get_distance(pos_1, pos_2):
    lat_diff = abs(float(pos_1[0]) - float(pos_2[0])) * 364000
    long_diff = abs(float(pos_1[1]) - float(pos_2[1])) * 288200
    return sqrt((lat_diff * lat_diff) + (long_diff + long_diff))


def get_degrees(pos_1, pos_2):
    return abs((float(pos_1[3]) - float(pos_2[3]) + 180 + 360) % 360 - 180)


def main():
    """
    Reads the given file of GPS data and created a KML file readable by Google Earth
    :return:
    """
    raw_lines = read_and_parse("2021_09_08__181321_gps_JERAMIAS_and_BACK.txt")
    clean = clean_lines(raw_lines)
    final = calculate_lat_long(clean)

    new_final = []
    new_final_2 = []

    temp = 0
    while temp < len(final) / 2:
        new_final.append(final[temp])
        temp += 1
    while temp < len(final):
        new_final_2.append(final[temp])
        temp += 1

    fp_out = open("Test_Output.kml", "w")

    emit_header(fp_out)


    emit_open_placemark(fp_out, "ffff00ff")
    emit_coordinates(fp_out, new_final)
    emit_close_placemark(fp_out)

    emit_open_placemark(fp_out, "ffff0000")
    emit_coordinates(fp_out, new_final_2)
    emit_close_placemark(fp_out)
    emit_trailer(fp_out)



















"""

    new_final = []
    non_turn = []
    idx = 0
    while idx < len(final):
        idx2 = idx
        possible_turn = []
        while idx2 < len(final):
            pos_1 = final[idx]
            pos_2 = final[idx2]
            if get_distance(pos_1, pos_2) > 50:
                if get_degrees(pos_1, pos_2) > 70:
                    for i in range (idx, idx2):
                        possible_turn.append(final[idx])
                    new_final.append((non_turn, False))
                    new_final.append((possible_turn, True))
                    non_turn = []
                    possible_turn = []
                    idx = idx2 + 1
                    idx2 = idx
                else:
                    non_turn.append(final[idx])
                    idx += 1
            else:
                non_turn.append((final[idx]))
            idx2+=1
        idx+=1
    new_final.append((non_turn, False))
"""


if __name__ == "__main__" :
    main()
