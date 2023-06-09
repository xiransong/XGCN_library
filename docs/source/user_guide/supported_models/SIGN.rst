.. _supported_models-SIGN:

SIGN
========

-----------------
Introduction
-----------------

`\[paper\] <https://arxiv.org/abs/2004.11198>`_

**Title:** SIGN: Scalable Inception Graph Neural Networks

**Authors:** Fabrizio Frasca, Emanuele Rossi, Davide Eynard, Ben Chamberlain, Michael Bronstein, Federico Monti

**Abstract:** Graph representation learning has recently been applied to a broad spectrum of problems ranging from computer graphics and chemistry to high energy physics and social media. The popularity of graph neural networks has sparked interest, both in academia and in industry, in developing methods that scale to very large graphs such as Facebook or Twitter social networks. In most of these approaches, the computational cost is alleviated by a sampling strategy retaining a subset of node neighbors or subgraphs at training time. In this paper we propose a new, efficient and scalable graph deep learning architecture which sidesteps the need for graph sampling by using graph convolutional filters of different size that are amenable to efficient precomputation, allowing extremely fast training and inference. Our architecture allows using different local graph operators (e.g. motif-induced adjacency matrices or Personalized Page Rank diffusion matrix) to best suit the task at hand. We conduct extensive experimental evaluation on various open benchmarks and show that our approach is competitive with other state-of-the-art architectures, while requiring a fraction of the training and inference time. Moreover, we obtain state-of-the-art results on ogbn-papers100M, the largest public graph dataset, with over 110 million nodes and 1.5 billion edges.

----------------------
Running with XGCN
----------------------

XGCN implements two version of SIGN: (1) ``SIGN``: freeze node embeddings (such as embeddings pretrained by node2vec) as fixed features;
(2) ``SIGN_learnable_emb``: has learnable node embeddings. 

SIGN
-----------------

**Configuration template for SIGN:**

.. code:: yaml

    # config/SIGN-config.yaml
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
    model: SIGN
    seed: 1999
    device: 'cuda:0'

    from_pretrained: 1
    file_pretrained_emb: ''
    freeze_emb: 1

    L2_reg_weight: 0.0
    dnn_lr: 0.001

    num_gcn_layers: 2
    num_dnn_layers: 2

    loss_fn: bpr


**Run SIGN from command line:**

Note that pretrained embeddings are needed, to run the script below, please run Node2vec first. 

.. code:: bash

    # script/examples/facebook/run_SIGN.sh
    # set to your own path:
    all_data_root='/home/sxr/code/XGCN_and_data/XGCN_data'
    config_file_root='/home/sxr/code/XGCN_and_data/XGCN_library/config'

    dataset=facebook
    model=SIGN
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



SIGN_learnable_emb
-----------------------

**Configuration template for SIGN_learnable_emb:**

.. code:: yaml

    # config/SIGN_learnable_emb-config.yaml
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
    Dataset_type: BlockDataset
    num_workers: 0
    num_gcn_layers: 2
    train_num_layer_sample: "[10, 10]"
    NodeListDataset_type: LinkDataset
    pos_sampler: ObservedEdges_Sampler
    neg_sampler: RandomNeg_Sampler
    num_neg: 1
    BatchSampleIndicesGenerator_type: SampleIndicesWithReplacement
    train_batch_size: 2048
    str_num_total_samples: num_edges
    epoch_sample_ratio: 0.1

    # Model configuration
    model: SIGN_learnable_emb
    seed: 1999

    graph_device: "cuda:0"
    emb_table_device: "cuda:0"
    gnn_device: "cuda:0"
    out_emb_table_device: "cuda:0"

    forward_mode: sample

    emb_dim: 64
    emb_lr: 0.005
    gnn_lr: 0.001
    emb_init_std: 0.1
    use_sparse: 0
    freeze_emb: 0
    from_pretrained: 0
    file_pretrained_emb: ''

    num_dnn_layers: 2

    L2_reg_weight: 0.0
    loss_type: bpr


**Run SIGN_learnable_emb from command line:**

.. code:: bash

    # script/examples/facebook/run_SIGN_learnable_emb.sh
    # set to your own path:
    all_data_root='/home/sxr/code/XGCN_and_data/XGCN_data'
    config_file_root='/home/sxr/code/XGCN_and_data/XGCN_library/config'

    dataset=facebook
    model=SIGN_learnable_emb
    seed=0
    device="cuda:1"
    graph_device=$device
    emb_table_device=$device
    gnn_device=$device
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
        --graph_device $graph_device --emb_table_device $emb_table_device \
        --gnn_device $gnn_device --out_emb_table_device $out_emb_table_device \
        # --from_pretrained 1 --file_pretrained_emb $file_pretrained_emb \
