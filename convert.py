import os
import glob
from tqdm import tqdm

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    
    return (x, y, w, h)
    
labels = "full_dataset/label" # label 폴더(json)
outpath = "txt"
json_backup ="json_backup"

if not os.path.isdir(outpath): os.makedirs(outpath, exist_ok=True)
if not os.path.isdir(json_backup): os.makedirs(json_backup, exist_ok=True)

""" Get input json file list """
# 둘중 하나 선택
# [1]
# json_name_list = []
# for file in os.listdir(labels):
#     if file.endswith(".json"):
#         json_name_list.append(file)

# [2]
json_name_list = glob.glob(os.path.join(labels, "*.json"))

# 클래스 입력 -> labelme에서 입력한 (숫자, 클래스명)이랑 같아야 함
class_name = {"green_3": 0,
              "orange_3" : 1,
              "red_3" : 2,
              "all_green_4" : 3,
              "straight_green_4" : 4,
              "left_green_4" : 5,
              "orange_4" : 6,
              "red_4" : 7,
              "delivery_a1" : 8,
              "delivery_a2" : 9,
              "delivery_a3" : 10,
              "delivery_b1" : 11,
              "delivery_b2" : 12,
              "delivery_b3": 13}

temp = 0 
total = 0
count = 0
isLabeled = False
now_json = ""
w, h = 640, 480 # 이미지 사이즈 -> 조절 (로지텍 웹캠 기준)

""" Process """
for json_name in tqdm(json_name_list):
    txt_name = json_name.rstrip(".json") + ".txt"
    """ Open input text files """
    txt_path = os.path.join(labels, json_name)
    # print("Input:" + txt_path)
    txt_file = open(txt_path, "r")
    
    """ Open output text files """
    txt_outpath = os.path.join(outpath, txt_name)
    # print("Output:" + txt_outpath)
    txt_outfile = open(txt_outpath, "a")

    """ Convert the data to YOLO format """ 
    lines = txt_file.readlines()   #for ubuntu, use "\r\n" instead of "\n"

    count = 0     
    total += 1
    
    for idx, line in enumerate(lines):
        if "lineColor" in line:
            break # skip reading after find lineColor
        if "label" not in line:
            pass
            
        if ("label" in line) and lines[idx - 1] == "    {\n":
            x1 = float(lines[idx + 3].lstrip().strip('\n').strip(',')) # float(lines[idx+3].rstrip(','))
            y1 = float(lines[idx + 4].lstrip())  # float(lines[idx+4])
            x2 = float(lines[idx + 7].lstrip().strip('\n').strip(','))
            y2 = float(lines[idx + 8].lstrip())  # float(lines[idx+8])
            cls = line.split('"')[3]
            
            if cls not in class_name.keys():
                print("Unvalid label name : {} ({})".format(cls, json_name))
                continue
            
            cls = str(class_name[cls])
            
            xmin = min(x1,x2)
            xmax = max(x1,x2)
            ymin = min(y1,y2)
            ymax = max(y1,y2)
            
            if count == 0:
                temp += 1
            
            count += 1
            
            w = 640
            h = 480

            b = (xmin, xmax, ymin, ymax)
            bb = convert((w,h), b)
            txt_outfile.write(cls + " " + " ".join([str(a) for a in bb]) + '\n')
    
print("Total : {} / {}".format(temp, total))