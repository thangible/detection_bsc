import os
from dataset_maker import create_augmented_images
import albumentations as A

NEWDIR = "../augmented_yolov5_dataset/"
OLDDIR = "../yolov5_dataset"
MASKDIR = '../yolov5_dataset/SegmentationObject'
DATA_INFO = '../yolov5_dataset/manual_annotated_data.csv'

Resize = A.Resize(height = 500, width = 500, interpolation=1, p=1.0)
CenterCrop = A.Compose([A.CenterCrop(height = 200, width = 200, p=1.0),Resize])
CenterCrop_2 = A.Compose([A.CenterCrop(height = 100, width = 100, p=1.0),Resize])
GridDropout = A.GridDropout(ratio = 0.6, random_offset = True, p=1)
CLAHE = A.CLAHE(clip_limit = 4, tile_grid_size=(4, 4), p=1.0)
Sharpen = A.Sharpen(alpha= (0.6,0.8), lightness = (0.6,1.0), p=1.0)
ToGray = A.ToGray(p=1)
ToSepia = A.ToSepia(p=1)
GaussNoise = A.GaussNoise(p =1)

#BATCH2
MotionBlur =  A.MotionBlur(blur_limit =31,  p=1.0)
Normalize = A.Normalize(mean = (0.184, 1.289, 0.661), std = (0.708, 0.338, 0.177), p = 1.0)


aug_dict = {}
aug_dict['MotionBlur'] = MotionBlur
aug_dict['Normalize'] = Normalize


# os.system('python3 train.py --data dataset_baseline.yaml --hyp custom_hyp.yaml --weights yolov5s.pt --cache --epochs 500 --run_name baseline')
for run_name in aug_dict.keys():
    augmentation = aug_dict[run_name]
    create_augmented_images(augmentation = augmentation, olddir = OLDDIR, newdir = NEWDIR, maskdir = MASKDIR, data_info_path = DATA_INFO)
    os.system('python3 train.py --data dataset.yaml --hyp custom_hyp.yaml --weights yolov5s.pt --cache --epochs 500 --run_name {}'.format(run_name))