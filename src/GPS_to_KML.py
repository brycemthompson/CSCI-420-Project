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
    two_points = [stripped_list[0], stripped_list[1]]
    return two_points


def main():
    FILENAME = "2021_09_AA__GPS_CHECK.txt"
    two_points = read_and_parse(FILENAME)
    print(two_points)
    return None


if __name__ == "__main__":
    main()