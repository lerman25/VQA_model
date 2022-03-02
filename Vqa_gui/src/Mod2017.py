import pdb

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class Mod2017(nn.Module):

    def __init__(self):
        super(Mod2017, self).__init__()
        """
            vocab_size (int): how many vocabs
            wemb_init (str): path to pretrained wemb weights
            hid_dim (int): for GRU -> 512
            num_classes (int): output classes -> 3129
        """
        # emb_dim = int(wemb_init.split('_')[-1].split('.')[0])
        hid_dim=128
        num_classes=2
        self.hid_dim = hid_dim

        # question encoding
        # self.wembed = nn.Embedding(vocab_size + 1, emb_dim)
        self.gru = nn.GRU(768, hid_dim)

        # image attention
        self.att = nn.Linear(hid_dim, 1)

        # output classifier
        self.clf = nn.Linear(hid_dim, num_classes)
        self.clf_do = nn.Dropout(0.5, inplace=True)

        # initialize word embedding layer weight
        # pretrained_wemb = np.zeros((vocab_size + 1, emb_dim), dtype=np.float32)
        # pretrained_wemb[:vocab_size] = np.load(wemb_init)
        # self.wembed.weight.data.copy_(torch.from_numpy(pretrained_wemb))

        # gated tanh activation
        self.gth_iatt = nn.Linear(2048 + hid_dim, hid_dim)
        self.gthp_iatt = nn.Linear(2048 + hid_dim, hid_dim)
        self.gth_q = nn.Linear(hid_dim, hid_dim)
        self.gthp_q = nn.Linear(hid_dim, hid_dim)
        self.gth_i = nn.Linear(2048, hid_dim)
        self.gthp_i = nn.Linear(2048, hid_dim)
        self.gth_clf = nn.Linear(hid_dim, hid_dim)
        self.gthp_clf = nn.Linear(hid_dim, hid_dim)


    def forward(self, question, image):
        """
        question -> shape (batch, 14)
        image -> shape (batch, 36, 2048)
        """
        # question encoding
        # emb = self.wembed(question)                 # (batch, seqlen, emb_dim)
        # enc, hid = self.gru(emb.permute(1, 0, 2))   # (seqlen, batch, hid_dim)
        # question=question.reshape(question.size(0),14,300)
        batch_size = question.size(0)
        qenc,hid = self.gru(question.permute(1, 0, 2))  
        qenc = qenc[-1]
        # print(qenc.size())                         # (batch, hid_dim)
        # print(question.size(0)*question.size(1)*question.size(2))
        # image attention
        qenc_reshape = qenc.repeat(1, 49).view(-1, 49, self.hid_dim) 
        # print(image.shape,qenc_reshape.shape)       # (batch, 36, hid_dim)
        # image = image.view(image.size(0),image.size(1),image.size(2)*image.size(3))
        # image = image.permute(0,2,1)
        image = F.normalize(image, -1) 
        # print(image.shape,qenc_reshape.shape)       # (batch, 36, hid_dim)                                 # (batch, 36, 2048)
        concated = torch.cat((image, qenc_reshape), -1)                 # (batch, 36, 2048 + hid_dim)
        concated = torch.mul(torch.tanh(self.gth_iatt(concated)), torch.sigmoid(self.gthp_iatt(concated)))
        a = self.att(concated)                              # (batch, 36, 1)
        a = F.softmax(a.squeeze(), dim=0)      
        print(a.unsqueeze(0).shape,image.shape)             # (batch, 36)
        v_head = torch.bmm(a.unsqueeze(0).unsqueeze(0), image).squeeze() # (batch, 2048)

        # element-wise (question + image) multiplication
        q = torch.mul(torch.tanh(self.gth_q(qenc)), torch.sigmoid(self.gthp_q(qenc)))
        v = torch.mul(torch.tanh(self.gth_i(v_head)), torch.sigmoid(self.gthp_i(v_head)))
        h = torch.mul(q, v) # (batch, hid_dim)

        # output classifier
        s_head = self.clf(torch.mul(torch.tanh(self.gth_clf(h)), torch.sigmoid(self.gthp_clf(h))))
        s_head = self.clf_do(s_head)
        return s_head
    @staticmethod
    def get_model_instance():
        return Mod2017(128,2)
