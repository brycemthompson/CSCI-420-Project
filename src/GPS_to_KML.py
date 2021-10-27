from math import sqrt

# Constants
COLOR_RED = "ff0000"
COLOR_MAGENTA = "ff00ff"


class Point:
    def __init__(self, latitude, longitude, speed, angle, color):
        self.latitude = latitude
        self.longitude = longitude
        self.speed = speed
        self.angle = angle
        self.color = color

    def change_color(self, color):
        self.color = color


def emit_header(fp_out):
    fp_out.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    fp_out.write("<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n")
    fp_out.write("  <Document>\n")
    fp_out.write("    <name>Paths</name>\n")
    fp_out.write("    <description>Examples of paths. Note that the tessellate tag is by default\n")
    fp_out.write("      set to 0. If you want to create tessellated lines, they must be authored\n")
    fp_out.write("      (or edited) directly in KML.</description>\n")\

def emit_styles(fp_out):
    fp_out.write("    <Style id=\"yellowLineGreenPoly\">\n")
    fp_out.write("      <LineStyle>\n")
    fp_out.write("        <color>7f00ffff</color>\n")
    fp_out.write("        <width>4</width>\n")
    fp_out.write("      </LineStyle>\n")
    fp_out.write("      <PolyStyle>\n")
    fp_out.write("        <color>7f00ff00</color>\n")
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
            clean.append((temp[3], temp[4], temp[5], temp[6], temp[7]))
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

        final.append(Point(lat, long, value[4], value[5], COLOR_MAGENTA))

    del clean
    return final

def get_distance(pos_1, pos_2):
    lat_diff = abs(float(pos_1[0]) - float(pos_2[0])) * 364000
    long_diff = abs(float(pos_1[1]) - float(pos_2[1])) * 288200
    return sqrt((lat_diff * lat_diff) + (long_diff + long_diff))


def get_degrees(pos_1, pos_2):
    return abs((float(pos_1[3]) - float(pos_2[3]) + 180 + 360) % 360 - 180)


def main():
    raw_lines = read_and_parse("2021_09_08__181321_gps_JERAMIAS_and_BACK.txt")
    clean = clean_lines(raw_lines)
    final = calculate_lat_long(clean)

    nf = []
    nf2 = []
    temp = 0
    while temp < len(final) /2:
        nf.append(final[temp])
        temp+=1
    while temp < len(final):
        nf2.append(final[temp])
        temp+=1

    fp_out = open("Test_Output.kml", "w")

    emit_header(fp_out)
    emit_styles(fp_out)

    emit_placemarker_start(fp_out, "yellowLineGreenPoly")
    emit_coordinates(fp_out, nf)
    emit_placemarker_end(fp_out)

    emit_placemarker_start(fp_out, "blueLineGreenPoly")
    emit_coordinates(fp_out, nf2)
    emit_placemarker_end(fp_out)

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
