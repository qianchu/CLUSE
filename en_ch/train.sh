if [ ! -d $1 ]; then
	  mkdir $1
fi

TF_CFLAGS=( $(python -c 'import tensorflow as tf; print(" ".join(tf.sysconfig.get_compile_flags()))') )
TF_LFLAGS=( $(python -c 'import tensorflow as tf; print(" ".join(tf.sysconfig.get_link_flags()))') )
g++ -std=c++11 -shared word2vec_ops.cc word2vec_kernels.cc -o word2vec_ops.so -fPIC ${TF_CFLAGS[@]} ${TF_LFLAGS[@]} -O2
python2.7 main.py --dataset_dir ../data/en_ch/ --log_path $1.txt --save_dir $1/ --major_weight $2 --reg_weight $3
