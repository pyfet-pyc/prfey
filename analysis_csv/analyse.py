import sys, os, csv

try:
    folder = sys.argv[1]
except:
    print("Usage:\npython analyse.py py3.8")
    exit()

if not folder.endswith('/'):
    folder += '/'
if not os.path.exists(folder):
    print("Invlid directory")
    exit()
files = next(os.walk(folder), (None, None, []))[2]

# print(files)

try:
    core_functions = [folder+x for x in files if "Error_functions" in x][0]
    other_functions = [folder+x for x in files if "Error_functions" not in x]
except:
    print("Not core directory for functions found")
    exit()

# Create dictionary of core functions
with open(core_functions) as csvfile:
    spamreader = csv.reader(csvfile)
    all_functions = [list(filter(None, x)) for x in spamreader][1:]
    # print(all_functions[:5])
    all_functions_dict = {x[0]: x[2:]  for x in all_functions}

for exp in other_functions:
    with open(exp) as csvfile:
        spamreader = csv.reader(csvfile)
        all_functions = [list(filter(None, x)) for x in spamreader][1:]
        for sub_exp in all_functions:
            id = sub_exp[0]
            status = sub_exp[1]
            failing_funcs = sub_exp[3:]
            if status == 'Pass':
                all_functions_dict[id] = []
                continue
            if status == 'Fail' and failing_funcs[0] == '#VALUE!':
                continue
            all_functions_dict[id] = [x for x in all_functions_dict[id] if x in failing_funcs]

f = open('log{}.txt'.format(folder[:-1]),'w')
for x in all_functions_dict:
    print('{} {}'.format(x, len(all_functions_dict[x])),file=f)

f = open('log_full{}.txt'.format(folder[:-1]),'w')
for x in all_functions_dict:
    print('{} {}'.format(x, all_functions_dict[x]),file=f)
