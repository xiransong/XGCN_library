source /opt/conda/bin/activate
conda env create --file=env/requirements.xgcn.yaml
conda activate xgcn 

PROJECT_ROOT='xGCN'
ALL_DATA_ROOT='/home/jialia/ds/social_and_user_item'

# PROJECT_ROOT='/media/xreco/jianxun/xGCN'
# ALL_DATA_ROOT='/media/xreco/DEV/xiran/data/social_and_user_item'

DEVICE='cuda'

########################################
DATASET=$1
seed=$2

num_gcn_layers=$3
num_layer_sample=$4

bash $PROJECT_ROOT/script/run_in_msra/run_sgc_learnable_emb.sh $PROJECT_ROOT $ALL_DATA_ROOT $DEVICE $DATASET $seed \
    $num_gcn_layers $num_layer_sample
