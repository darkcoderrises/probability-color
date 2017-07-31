from handlers import ImageHandler
import glob
import sys

if __name__ == "__main__":
    files = glob.glob('./color_lover/*.png')
    size_data = []
    color_data = []

    for i in files:
        sys.stdout.write('%s\r' % i)
        sys.stdout.flush()

        ih = ImageHandler(i)
        ih.set_up()
        ih.find_components()
        data = ih.create_groups()

        size_data.extend(data[0])
        color_data.extend(data[1])

    size_file = open("./result/size_data")
    color_file = open("./result/color_data")

    for i in size_data:
        size_file.write("%s\n" % str(i))

    for i in color_data:
        color_file.write("%s\n" % str(i))
