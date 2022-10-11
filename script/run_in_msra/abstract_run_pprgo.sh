source /opt/conda/bin/activate
conda env create --file=env/requirements.xgcn.yaml
conda activate xgcn 

PROJECT_ROOT='xGCN'
ALL_DATA_ROOT='/home/jialia/ds/social_and_user_item'

DEVICE='cuda'

########################################
DATASET=$1
seed=$2
use_ssnet=$3

bash xGCN/script/run_in_msra/run_pprgo.sh $PROJECT_ROOT $ALL_DATA_ROOT $DEVICE $DATASET $seed $use_ssnet
# xGCN/script/run_in_msra/