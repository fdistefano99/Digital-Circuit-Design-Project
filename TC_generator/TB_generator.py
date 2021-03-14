from math import floor, log2
from random import randint

def solve_case(case):
    image = case[2:]
    min_pixel_value, max_pixel_value = min(image), max(image)
    delta_value = max_pixel_value - min_pixel_value
    shift_level = 8 - floor(log2(delta_value + 1))

    def equalize(pixel):
        temp_pixel = (pixel - min_pixel_value) << shift_level
        return min(255, temp_pixel)

    return [equalize(x) for x in image]

def generate_case(cols, rows):
    if test_type=="RANDOM":
        return [cols, rows] + [randint(0, 256) for _ in range(rows * cols)]
    elif test_type=="ALL0":
        return [cols, rows] + [0 for _ in range(rows * cols)]
    elif test_type=="ALL255":
        return [cols, rows] + [255 for _ in range(rows * cols)]
    elif test_type=="MANUAL":
        return [cols, rows] + [int(input("Inserire il " + str(i) + "° pixel dell'immagine: ")) for i in range(rows * cols)]

def generate_ram(cols, rows):
    case = generate_case(cols, rows)
    return case + solve_case(case)

cols=int(input("Inserire il numero di colonne(compreso tra 1 e 128) dell'immagine: "))
rows=int(input("Inserire il numero di righe(compreso tra 1 e 128) dell'immagine: "))
test_type=str(input("Inserire la tipologia di test('RANDOM', 'ALL0', 'ALL255' o 'MANUAL') da generare: "))

ram=generate_ram(cols, rows)

model_part1=open("TB_model_part1.vhd", "r")
model_part2=open("TB_model_part2.vhd", "r")
model_part3=open("TB_model_part3.vhd", "r")
TB=open("TB_" + str(cols) + "x" + str(rows) + "_" + test_type + ".vhd", "w")
TB.writelines(model_part1.readlines())
for i in range(cols * rows + 2):
    TB.write(str(i) +  " => std_logic_vector(to_unsigned(  " + str(ram[i]) + "  , 8)),\n\t\t\t\t\t\t ")
TB.write("others => (others =>'0'));\n")
TB.writelines(model_part2.readlines())
for i in range(cols * rows + 2, cols * rows * 2 + 2):
    TB.write("assert RAM(" + str(i) + ") = std_logic_vector(to_unsigned( " + str(ram[i]) + " , 8)) report \"TEST FALLITO (WORKING ZONE). Expected  " + str(ram[i]) + "  found \" & integer'image(to_integer(unsigned(RAM("+ str(i) +"))))  severity failure;\n\t")
TB.writelines(model_part3.readlines())
TB.close()
model_part1.close()
model_part2.close()
model_part3.close()
input("Testbench generato.")







