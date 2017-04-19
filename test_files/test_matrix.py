from ledmatrix import LedMatrix

def main():
    led_matrix = LedMatrix()
    led_matrix.change_color(led_matrix.clear_matrix())


if __name__ == "__main__":
    main()
