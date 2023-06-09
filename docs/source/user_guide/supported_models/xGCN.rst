.. _supported_models-xGCN:

xGCN
=========

Introduction
-----------------

`\[paper\] <https://dl.acm.org/doi/10.1145/3543507.3583340>`_

**Title:** xGCN: An Extreme Graph Convolutional Network for Large-scale Social Link Prediction

**Authors:** Xiran Song, Jianxun Lian, Hong Huang, Zihan Luo, Wei Zhou, Xue Lin, Mingqi Wu, Chaozhuo Li, Xing Xie, Hai Jin

**Abstract:** Graph neural networks (GNNs) have been widely used in various real-world applications, thanks to their flexibility and effectiveness in learning graph-structure data. However, when it comes to large-scale transductive network embedding, which is a practical solution for link predictions, existing GNNs still face some accuracy, efficiency, and scalability issues due to the huge trainable parameters in the embedding table and the paradigm of stacking neighborhood aggregations. In this paper, we propose a novel model xGCN, which encodes graph-structure data in an extreme convolutional manner and has the potential to push the performance of graph embedding-based link predictions to a new record. Instead of assigning each node with a directly learnable embedding vector, xGCN regards node embeddings as static features. It uses a propagation operation to smooth node embeddings and relies on a Refinement neural Network (RefNet) to transform the coarse embeddings derived from the unsupervised propagation into new ones that optimize a training objective. The output of RefNet, which are well refined embeddings, will replace the original node embeddings. This process is repeated
iteratively until the model converges to a satisfying status. We conduct experiments on three social network datasets with link prediction tasks. Results demonstrate that xGCN not only achieves the best accuracy compared with a series of competitive baselines, but also is highly efficient and scalable.

Running with XGCN
----------------------

**Configuration template for xGCN:**

.. code:: yaml

    # config/GCN-config.yaml
    # Dataset/Results root
    data_root: ""
    results_root: ""

    # Trainer configuration
    epochs: 200
    use_validation_for_early_stop: 1
    val_freq: 1
    key_score_metric: r100
    convergence_threshold: 20
    val_method: ""
    val_batch_size: 256
    file_val_set: ""

    # Testing configuration
    test_method: ""
    test_batch_size: 256
    file_test_set: ""

    # DataLoader configuration
    Dataset_type: NodeListDataset
    num_workers: 1
    NodeListDataset_type: LinkDataset
    pos_sampler: ObservedEdges_Sampler
    neg_sampler: RandomNeg_Sampler
    num_neg: 1
    BatchSampleIndicesGenerator_type: SampleIndicesWithReplacement
    train_batch_size: 1024
    str_num_total_samples: num_edges
    epoch_sample_ratio: 0.1

    # Model configuration
    model: xGCN
    seed: 1999

    emb_table_device: "cuda:0"
    forward_device: "cuda:0"
    out_emb_table_device: "cuda:0"

    from_pretrained: 0
    file_pretrained_emb: ""
    freeze_emb: 1
    emb_dim: 64 
    emb_init_std: 1.0

    loss_type: bpr
    L2_reg_weight: 0.0

    dnn_lr: 0.001
    dnn_arch: "[nn.Linear(64, 1024), nn.Tanh(), nn.Linear(1024, 1024), nn.Tanh(), nn.Linear(1024, 64)]"
    use_scale_net: 1
    scale_net_arch: "[nn.Linear(64, 32), nn.Tanh(), nn.Linear(32, 1), nn.Sigmoid()]"

    num_gcn_layers: 1
    stack_layers: 0

    renew_by_loading_best: 1
    K: 10
    T: 3
    tolerance: 3


**Run xGCN from command line:**

.. code:: bash
    
    # script/examples/facebook/run_xGCN.sh
    # set to your own path:
    all_data_root='/home/sxr/code/XGCN_and_data/XGCN_data'
    config_file_root='/home/sxr/code/XGCN_and_data/XGCN_library/config'

    dataset=facebook
    model=xGCN
    seed=0
    device='cuda:0'
    emb_table_device=$device
    forward_device=$device
    out_emb_table_device=$device

    data_root=$all_data_root/dataset/instance_$dataset
    results_root=$all_data_root/model_output/$dataset/$model/[seed$seed]

    # file_pretrained_emb=$all_data_root/model_output/$dataset/Node2vec/[seed$seed]/model/out_emb_table.pt

    python -m XGCN.main.run_model --seed $seed \
        --config_file $config_file_root/$model-config.yaml \
        --data_root $data_root --results_root $results_root \
        --val_method one_pos_k_neg \
        --file_val_set $data_root/val-one_pos_k_neg.pkl \
        --key_score_metric r20 \
        --test_method multi_pos_whole_graph \
        --file_test_set $data_root/test-multi_pos_whole_graph.pkl \
        --emb_table_device $emb_table_device \
        --forward_device $forward_device \
        --out_emb_table_device $out_emb_table_device \
        # --from_pretrained 1 --file_pretrained_emb $file_pretrained_emb \

