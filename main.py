
# statement: immediate number should start with 'i', and register should start with 'r'.

def convert_8bit(string):
    string = bin(int(string) + 256)
    return str(string)[3:]


def convert_5bit(string):
    string = bin(int(string) + 32)
    return str(string)[3:]


def check_error(alu_op, seg_type):
    op = ['ADD', 'SUB', 'MUL', 'DIV', 'AND', 'OR', 'NOT', 'RSHIFT', 'LSHIFT', 'MOVE', 'MOVEOUT', 'MOVEIN', 'JUMP',
          'EJUMP', 'NEJUMP', 'MTHAN', 'LRMOVE']
    if alu_op == op[0] or alu_op == op[1] or alu_op == op[4] or alu_op == op[5] or alu_op == op[7] or alu_op == op[8]:
        if seg_type == '855' or seg_type == '555':
            return 0
        else:
            return 1
    elif alu_op == op[2] or alu_op == op[3]:
        if seg_type == '55':
            return 0
        else:
            return 1
    elif alu_op == op[6] or alu_op == op[9]:
        if seg_type == '55' or seg_type == '85':
            return 0
        else:
            return 1
    elif alu_op == op[10] or alu_op == op[15]:
        if seg_type == '555':
            return 0
        else:
            return 1
    elif alu_op == op[12] or alu_op == op[13] or alu_op == op[14]:
        if seg_type == '55':
            return 0
        else:
            return 1
    elif alu_op == op[11]:
        if seg_type == '88':
            return 0
        else:
            return 1
    elif alu_op == op[16]:
        if seg_type == '85':
            return 0
        else:
            return 1


with open('Code.txt', 'r') as file:
    code_file_list = file.readlines()
file.close()

file = open('MachineCode.txt', 'w')

line = 0
error = 0
instruction = 'START Line: '

for line in range(len(code_file_list)):

    if instruction != '':
        file.write(instruction + '\n')
        # file.write('assign w_rom_inst[' + str(line) + "] = 32'b" + instruction + ';\n')
    # print(instruction)

    instruction = ''
    alu = ''
    func = ''
    pc_sign = '10'
    mem_sign = '0'
    imm_sign = '0'
    reg_sign = '11'
    reg = []
    imm = []
    reg_flag = 0
    imm_flag = 0
    code_line_list = ((code_file_list[line]).upper().strip('\n')).split(' ')

    # print(code_line_list)

    if (len(code_line_list) > 4 or len(code_line_list) < 3) and code_line_list[0] != '//' and \
            code_line_list[0] != 'WAIT' and code_line_list[0] != 'C1' and code_line_list[0] != 'S2' and \
            code_line_list[0] != 'C3' and code_line_list[0] != 'S4' and code_line_list[0] != 'C5':
        error += 1
        print('At line ' + str(line + 1) + ': Empty or incomplete statement')
        continue

    if code_line_list[0] == 'ADD':
        alu = '00000001'
    elif code_line_list[0] == 'SUB':
        alu = '00000010'
    elif code_line_list[0] == 'MUL':
        alu = '00000011'
    elif code_line_list[0] == 'DIV':
        alu = '00000100'
    elif code_line_list[0] == 'AND':
        alu = '00000101'
    elif code_line_list[0] == 'OR':
        alu = '00000110'
    elif code_line_list[0] == 'NOT':
        alu = '00000111'
    elif code_line_list[0] == 'RSHIFT':
        alu = '00001000'
    elif code_line_list[0] == 'LSHIFT':
        alu = '00001001'
    elif code_line_list[0] == 'MOVE':
        alu = '00001010'
    elif code_line_list[0] == 'MOVEOUT':
        alu = '00001011'
        reg_sign = '01'
        mem_sign = '1'
    elif code_line_list[0] == 'MOVEIN':
        alu = '00001100'
    elif code_line_list[0] == 'JUMP':
        alu = '00001101'
        pc_sign = '01'
        reg_sign = '01'
    elif code_line_list[0] == 'EJUMP':
        alu = '00001110'
        pc_sign = '01'
        reg_sign = '01'
    elif code_line_list[0] == 'NEJUMP':
        alu = '00001111'
        pc_sign = '01'
        reg_sign = '01'
    elif code_line_list[0] == 'MTHAN':
        alu = '00010000'
    elif code_line_list[0] == 'WAIT':
        alu = '00010001'
        instruction = alu + '100100000000000000000000'
        continue
    elif code_line_list[0] == 'C1':
        alu = '10000000'
        reg_sign = '01'
        instruction = alu + '100100000000000000000000'
        continue
    elif code_line_list[0] == 'S2':
        alu = '10000001'
        reg_sign = '01'
        instruction = alu + '100100000000000000000000'
        continue
    elif code_line_list[0] == 'C3':
        alu = '10000010'
        reg_sign = '01'
        instruction = alu + '100100000000000000000000'
        continue
    elif code_line_list[0] == 'S4':
        alu = '10000011'
        reg_sign = '01'
        instruction = alu + '100100000000000000000000'
        continue
    elif code_line_list[0] == 'C5':
        alu = '10000100'
        reg_sign = '01'
        instruction = alu + '100100000000000000000000'
        continue
    elif code_line_list[0] == 'LRMOVE':
        alu = '10000101'
    elif code_line_list[0] == '//':
        continue
    else:
        error += 1
        print('At line ' + str(line + 1) + ': Unknown operation.')
        continue

    for word in range(1, len(code_line_list)):
        if code_line_list[word][0:1] == 'R':
            if int(code_line_list[word].strip('R')) < 32:
                reg_flag += 1
                reg.append(code_line_list[word].strip('R'))
            else:
                error += 1
                print('At line ' + str(line + 1) + ': Register address out of range.')
                continue
        elif code_line_list[word][0:1] == 'I':
            if int(code_line_list[word].strip('I')) < 256:
                imm_flag += 1
                imm_sign = '1'
                imm.append(code_line_list[word].strip('I'))
            else:
                error += 1
                print('At line ' + str(line + 1) + ': Immediate number too large.')
                continue
        elif code_line_list[word] == 'S_MTHAN':
            reg_flag += 1
            reg.append('31')
        elif code_line_list[word] == 'S_JUMPH':
            reg_flag += 1
            reg.append('30')
        elif code_line_list[word] == 'S_JUMPL':
            reg_flag += 1
            reg.append('29')
        elif code_line_list[word] == 'S_MOVEIN':
            reg_flag += 1
            reg.append('28')
        elif code_line_list[word] == 'S_INTER':
            reg_flag += 1
            reg.append('27')
        elif code_line_list[word] == 'S_CARRY':
            reg_flag += 1
            reg.append('26')
        elif code_line_list[word] == 'S_NEG':
            reg_flag += 1
            reg.append('25')
        elif code_line_list[word] == 'S_MDH':
            reg_flag += 1
            reg.append('24')
        elif code_line_list[word] == 'S_MDL':
            reg_flag += 1
            reg.append('23')
        else:
            error += 1
            print('At line ' + str(line + 1) + ': Error statement, must be a register or immediate number.')
            continue

    if imm_flag == 1 and reg_flag == 2:
        func = convert_8bit(imm[0]) + convert_5bit(reg[0]) + convert_5bit(reg[1])
        seg_flag = '855'
    elif imm_flag == 0 and reg_flag == 2:
        func = convert_5bit(reg[0]) + convert_5bit(reg[1]) + '00000000'
        seg_flag = '55'
    elif imm_flag == 0 and reg_flag == 3:
        func = convert_5bit(reg[0]) + convert_5bit(reg[1]) + convert_5bit(reg[2]) + '000'
        seg_flag = '555'
    elif imm_flag == 2 and reg_flag == 0:
        func = convert_8bit(imm[0]) + convert_8bit(imm[0]) + '00'
        seg_flag = '88'
    elif imm_flag == 1 and reg_flag == 1:
        if alu != '10000101':
            reg_sign = '10'
        func = convert_8bit(imm[0]) + convert_5bit(reg[0]) + '00000'
        seg_flag = '85'
    else:
        error += 1
        print('At line ' + str(line + 1) + ': Error statement, cannot operate with such amount of register or immediate number.')
        continue

    check = check_error(code_line_list[0], seg_flag)
    if check == 1:
        error += 1
        print('At line ' + str(line + 1) + ': This operation is not allowed to operate in this way.')
        continue

    sign = pc_sign + reg_sign + imm_sign + mem_sign
    instruction = alu + sign + func
    # print(alu + ' ' + sign + ' ' + func)

file.write(instruction + '\n')
# file.write('assign w_rom_inst[' + str(line + 1) + "] = 32'b" + instruction + ';\n')
# print(instruction)
if error == 0:
    print('Compile success.')

    # form hex file for sending data to FPGA
    with open('MachineCode.txt', 'r') as file:
        machine_code_file_list = file.readlines()
    file.close()
    file = open('HexMachineCode.txt', 'w')
    for line in range(1, len(machine_code_file_list)):
        for i in range(4):
            msg = hex(int(machine_code_file_list[line][i * 8:i * 8 + 8], 2) + 256)[3:].upper()
            file.write(msg)

else:
    print('There are ' + str(error) + ' errors.')

file.close()
