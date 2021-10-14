"""
Authors: David Malik, Bryce Thompson, Atlee Hasson
Project - IoT Using GPS, Data Visualization, and Anomaly Detection
Checkpoint 01
"""


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
    fp_out.write("    <Style id=\"yellowLineGreenPoly\">\n")
    fp_out.write("      <LineStyle>\n")
    fp_out.write("        <color>7f00ffff</color>\n")
    fp_out.write("        <width>4</width>\n")
    fp_out.write("      </LineStyle>\n")
    fp_out.write("      <PolyStyle>\n")
    fp_out.write("        <color>7f00ff00</color>\n")
    fp_out.write("      </PolyStyle>\n")
    fp_out.write("    </Style>\n")
    fp_out.write("    <Placemark>\n")
    fp_out.write("      <name>Absolute Extruded</name>\n")
    fp_out.write("      <description>Transparent green wall with yellow outlines</description>\n")
    fp_out.write("      <styleUrl>#yellowLineGreenPoly</styleUrl>\n")
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
            clean.append((temp[3], temp[4], temp[5], temp[6], temp[7]))
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

        final.append((lat, long, value[4]))

    del clean
    return final

def main():
    """
    Reads the given file of GPS data and created a KML file readable by Google Earth
    :return:
    """
    raw_lines = read_and_parse("2021_09_08__181321_gps_JERAMIAS_and_BACK.txt")
    clean = clean_lines(raw_lines)
    final = calculate_lat_long(clean)

    fp_out = open("Test_Output.kml", "w")

    emit_header(fp_out)
    emit_coordinates(fp_out, final)
    emit_trailer(fp_out)

if __name__ == "__main__" :
    main()
