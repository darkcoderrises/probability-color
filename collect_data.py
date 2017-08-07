from handlers import ImageHandler
import glob
import sys

if __name__ == "__main__":
    files = glob.glob('./color_lover/*.png')
    size_file = open("./result/size_data")
    color_file = open("./result/color_data")


    for index, i in enumerate(files):
        sys.stdout.write('%d: %s\r' % index, i)
        sys.stdout.flush()

        ih = ImageHandler(i)
        ih.set_up()
        ih.find_components()
        data = ih.create_groups()

        for i in data[0]:
            size_file.write("%s\n" % str(i))

        for i in data[1]:
            color_file.write("%s\n" % str(i))

