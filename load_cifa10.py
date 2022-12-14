from typing import List

import numpy as np
import torch
from torchvision import transforms,datasets
from torch.utils.data import DataLoader
import argparse
import cv2
import os
from torch.utils.data import TensorDataset
import re



#1.加载cifar10数据集，返回的是train_loader,test_loader
def get_loader(args):
    train_set = []
    train_label: List[int] = []
    test_set = []
    train_dataset = []
    test_label = []
    test_dataset = []
    test_acc = []
    history = []
    #设置数据加载时的变换形式，包括撞转成tensor,裁剪，归一化
    # transform_train=transforms.Compose([
    #     transforms.RandomResizedCrop((args.img_size,args.img_size),scale=(0.05,1.0)),
    #     transforms.ToTensor(),
    #     transforms.Normalize((0.301), (0.3201))
    # ])
    # transform_test = transforms.Compose([
    #     transforms.Resize((args.img_size, args.img_size)),
    #     transforms.ToTensor(),
    #     transforms.Normalize((0.301), (0.3201))
    # ])
    Pipline = transforms.Compose(
        [

            transforms.ToTensor(),  # 将图片转化为tensor

            transforms.Normalize((0.301), (0.3201))  # 降低模型复杂度，官网提供的数据
        ]
    )  # 对图像作相应处理
    for filename in os.listdir('D:\\jupyter\\transformer_pytorch_inCV\\training'):
        imgPath = 'D:\\jupyter\\transformer_pytorch_inCV\\training'
        img = cv2.imread(imgPath + '\\' + filename, 0)  # 循环读取该目录下的所有图片
        train_label.append(int(re.findall(r"\d+", filename)[0]))  # 将图片名的第一个数字作为该图片的类
        train_set.append(Pipline(img).numpy().tolist())  # 对图片作pipline操作后转化为数组
    train_dataset = TensorDataset(torch.tensor(train_set), torch.tensor(train_label))  # 对两个列表进行压缩后作为训练集
    for filename in os.listdir('D:\\jupyter\\transformer_pytorch_inCV\\testing'):
        imgPath = 'D:\\jupyter\\transformer_pytorch_inCV\\testing'
        img = cv2.imread(imgPath + '\\' + filename, 0)
        test_label.append(int(re.findall(r"\d+", filename)[0]))
        test_set.append(Pipline(img).numpy().tolist())
    test_dataset = TensorDataset(torch.tensor(test_set), torch.tensor(test_label))  # 对两个列表进行压缩后作为测试集
    # #默认使用cifar10数据集
    # if args.dataset=="cifar10":
    #     trainset=datasets.CIFAR10(root=r'../data',train=True,download=False,transform=transform_train)
    #     testset=datasets.CIFAR10(root=r'../data',train=False,download=False,transform=transform_train)
    # else:
    #     trainset = datasets.CIFAR100(root='./data', train=True, download=True, transform=transform_train)
    #     testset = datasets.CIFAR100(root='./data', train=False, download=True, transform=transform_train)
    #
    #
    # print("train number:",len(trainset))
    # print("test number:",len(testset))

    train_loader=DataLoader(train_dataset,batch_size=args.train_batch_size,shuffle=True)
    test_loader=DataLoader(test_dataset,batch_size=args.eval_batch_size,shuffle=False)
    print("train_loader:",len(train_loader))
    print("test_loader:",len(test_loader))

    return train_loader,test_loader


#定义一个实例配置文件
# parser = argparse.ArgumentParser()
# # parser.add_argument("--dataset", choices=["cifar10", "cifar100"], default="cifar10")
# parser.add_argument("--img_size", type=int, default=224,)
# parser.add_argument("--train_batch-size", default=20, type=int,)
# parser.add_argument("--eval_batch-size", default=20, type=int,)
#
# args = parser.parse_args()
# get_loader(args)