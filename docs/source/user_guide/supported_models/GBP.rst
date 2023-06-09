.. _supported_models-GBP:

GBP
========

Introduction
-----------------

`\[paper\] <https://arxiv.org/abs/2010.15421>`_

**Title:** Scalable Graph Neural Networks via Bidirectional Propagation

**Authors:** Ming Chen, Zhewei Wei, Bolin Ding, Yaliang Li, Ye Yuan, Xiaoyong Du, Ji-Rong Wen

**Abstract:** Graph Neural Networks (GNN) is an emerging field for learning on non-Euclidean data. Recently, there has been increased interest in designing GNN that scales to large graphs. Most existing methods use "graph sampling" or "layer-wise sampling" techniques to reduce training time. However, these methods still suffer from degrading performance and scalability problems when applying to graphs with billions of edges. This paper presents GBP, a scalable GNN that utilizes a localized bidirectional propagation process from both the feature vectors and the training/testing nodes. Theoretical analysis shows that GBP is the first method that achieves sub-linear time complexity for both the precomputation and the training phases. An extensive empirical study demonstrates that GBP achieves state-of-the-art performance with significantly less training/testing time. Most notably, GBP can deliver superior performance on a graph with over 60 million nodes and 1.8 billion edges in less than half an hour on a single machine. The codes of GBP can be found at https://github.com/chennnM/GBP .

Running with XGCN
----------------------

**Configuration template for GBP:**

.. code:: yaml
    
    # config/GBP-config.yaml
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
    train_batch_size: 2048
    str_num_total_samples: num_edges
    epoch_sample_ratio: 0.1

    # Model configuration
    model: GBP
    seed: 1999
    device: 'cuda:0'

    from_pretrained: 1
    file_pretrained_emb: ''
    freeze_emb: 1

    alpha: 0.1
    walk_length: 6
    rmax_ratio: 0.01
    dnn_arch: "[nn.Linear(64, 1024), nn.Tanh(), nn.Linear(1024, 64)]"
    dnn_lr: 0.001
    L2_reg_weight: 0.0

    loss_fn: bpr


**Run GBP from command line:**

Note that pretrained embeddings are needed, to run the script below, please run Node2vec first. 

.. code:: bash

    # script/examples/facebook/run_GBP.sh
    all_data_root='/home/sxr/code/XGCN_and_data/XGCN_data'
    config_file_root='/home/sxr/code/XGCN_and_data/XGCN_library/config'

    dataset=facebook
    model=GBP
    seed=0
    device='cuda:1'

    data_root=$all_data_root/dataset/instance_$dataset
    results_root=$all_data_root/model_output/$dataset/$model/[seed$seed]

    # pretrained embeddings are needed
    file_pretrained_emb=$all_data_root/model_output/$dataset/Node2vec/[seed$seed]/model/out_emb_table.pt

    python -m XGCN.main.run_model --seed $seed \
        --config_file $config_file_root/$model-config.yaml \
        --data_root $data_root --results_root $results_root \
        --val_method one_pos_k_neg \
        --file_val_set $data_root/val-one_pos_k_neg.pkl \
        --key_score_metric r20 \
        --test_method multi_pos_whole_graph \
        --file_test_set $data_root/test-multi_pos_whole_graph.pkl \
        --file_pretrained_emb $file_pretrained_emb \
        --device $device \
