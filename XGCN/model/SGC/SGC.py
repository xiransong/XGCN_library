from XGCN.model.base import BaseEmbeddingModel
from XGCN.model.module import init_emb_table, dot_product, bpr_loss
from XGCN.data import io, csr

import numpy as np
import torch
import torch.nn.functional as F
import dgl
import os.path as osp
from tqdm import tqdm


class SGC(BaseEmbeddingModel):
    
    def __init__(self, config):
        super().__init__(config)
        self.device = self.config['device']

        assert self.config['from_pretrained'] and self.config['freeze_emb']
        self.emb_table = init_emb_table(config, self.info['num_nodes'])
        self.out_emb_table = torch.empty(self.emb_table.weight.shape, dtype=torch.float32)
        
        data_root = self.config['data_root']
        print("# load graph")
        if 'indptr' in self.data:
            indptr = self.data['indptr']
            indices = self.data['indices']
        else:
            data_root = config['data_root']
            indptr = io.load_pickle(osp.join(data_root, 'indptr.pkl'))
            indices = io.load_pickle(osp.join(data_root, 'indices.pkl'))
            self.data['indptr'] = indptr
            self.data['indices'] = indices
        indptr, indices = csr.get_undirected(indptr, indices)
        E_src = csr.get_src_indices(indptr)
        E_dst = indices
        
        print("# calc edge_weights")
        all_degrees = indptr[1:] - indptr[:-1]
        d_src = all_degrees[E_src]
        d_dst = all_degrees[E_dst]
        
        edge_weights = np.sqrt((1 / (d_src * d_dst)))
        del all_degrees, d_src, d_dst
        
        g = dgl.graph((E_src, E_dst)).to(self.device)
        g.edata['ew'] = torch.FloatTensor(edge_weights).to(self.device)
        g.ndata['X_0'] = self.emb_table.weight
        
        transform = dgl.SIGNDiffusion(
            k=self.config['num_gcn_layers'],
            in_feat_name='X_0',
            out_feat_name='X',
            eweight_name='ew'
        )
        g = transform(g)
        self.emb_table = g.ndata['X_' + str(self.config['num_gcn_layers'])]
        
        emb_dim = self.emb_table.shape[-1]
        self.mlp = torch.nn.Linear(emb_dim, emb_dim).to(self.device)
        
        self.optimizers = {}
        self.optimizers['gnn-Adam'] = torch.optim.Adam(
            [{'params': self.mlp.parameters(), 'lr': self.config['dnn_lr']}]
        )
    
    def get_output_emb(self, nids):
        return self.mlp(self.emb_table[nids])
        
    def forward_and_backward(self, batch_data):
        ((src, pos, neg), ) = batch_data
        
        src_emb = self.get_output_emb(src)
        pos_emb = self.get_output_emb(pos)
        neg_emb = self.get_output_emb(neg)
        
        pos_score = dot_product(src_emb, pos_emb)
        neg_score = dot_product(src_emb, neg_emb)
        
        loss_fn_type = self.config['loss_fn']
        if loss_fn_type == 'bpr':
            loss = bpr_loss(pos_score, neg_score)
        elif loss_fn_type == 'bce':
            pos_loss = F.binary_cross_entropy_with_logits(
                pos_score, 
                torch.ones(pos_score.shape).to(self.device),
            ).mean()
            neg_loss = F.binary_cross_entropy_with_logits(
                neg_score, 
                torch.zeros(neg_score.shape).to(self.device),
            ).mean()
            
            loss = pos_loss + neg_loss
        else:
            assert 0
        
        rw = self.config['L2_reg_weight']
        if rw > 0:
            L2_reg_loss = 1/2 * (1 / len(src)) * (
                (src_emb**2).sum() + (pos_emb**2).sum() + (neg_emb**2).sum()
            )
            loss += rw * L2_reg_loss
        
        self._backward(loss)
        
        return loss.item()
    
    def on_epoch_begin(self):
        self.mlp.train()
    
    @torch.no_grad()
    def infer_out_emb_table(self):
        self.mlp.eval()
        dl = torch.utils.data.DataLoader(dataset=torch.arange(self.info['num_nodes']), 
                                         batch_size=8192)
        for nids in tqdm(dl, desc="infer all output embs"):
            self.out_emb_table[nids] = self.get_output_emb(nids).cpu()
        
        if self.graph_type == 'user-item':
            self.target_emb_table = self.out_emb_table[self.info['num_users'] : ]
        else:
            self.target_emb_table = self.out_emb_table
    
    def save(self, root=None):
        if root is None:
            root = self.model_root
        self._save_optimizers(root)
        self._save_out_emb_table(root)
        torch.save(self.mlp.state_dict(), osp.join(root, 'mlp-state_dict.pt'))
    
    def load(self, root=None):
        if root is None:
            root = self.model_root
        self._load_optimizers(root)
        self._load_out_emb_table(root)
        self.mlp.load_state_dict(
            torch.load(osp.join(root, 'mlp-state_dict.pt'))
        )
