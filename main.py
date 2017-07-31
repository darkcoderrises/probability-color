from handlers import ImageHandler

if __name__ == "__main__":
    ih = ImageHandler('./color_lover/1000169.png')

    ih.set_up()
    ih.find_components()
    ih.create_groups()

