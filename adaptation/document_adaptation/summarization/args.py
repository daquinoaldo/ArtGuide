_args = {
    "accum_count": 1,
    "alpha": 0.9, 
    "batch_size": 3000, 
    "beam_size": 3, 
    "beta1": 0.9, 
    "beta2": 0.999, 
    "block_trigram": True, 
    "dec_dropout": 0.2, 
    "dec_ff_size": 2048, 
    "dec_heads": 8, 
    "dec_hidden_size": 768, 
    "dec_layers": 6, 
    "enc_dropout": 0.2, 
    "enc_ff_size": 512, 
    "enc_hidden_size": 512, 
    "enc_layers": 6, 
    "encoder": 'bert', 
    "ext_dropout": 0.2, 
    "ext_ff_size": 2048, 
    "ext_heads": 8, 
    "ext_hidden_size": 768, 
    "ext_layers": 2, 
    "finetune_bert": True, 
    "generator_shard_size": 32, 
    "gpu_ranks": '0', 
    "label_smoothing": 0.1, 
    "large": False, 
    "load_from_extractive": '', 
    "log_file": './val_abs_bert_cnndm', 
    "lr": 1, 
    "lr_bert": 0.002, 
    "lr_dec": 0.002, 
    "max_grad_norm": 0,
    "max_pos": 512, 
    "max_tgt_len": 0, # usato per estrarre il target - non serve 
    "min_length": 20, # calcolato in automatico - non serve
    "max_length": 300, # 500
    "mode": 'test', 
    "model_path": './document_adaptation/summarization/models/', 
    "optim": 'adam', 
    "param_init": 0, 
    "param_init_glorot": True, 
    "recall_eval": False, 
    "report_every": 1, 
    "report_rouge": False, 
    "result_path": './abs_bert_cnndm', 
    "save_checkpoint_steps": 5, 
    "seed": 666, 
    "sep_optim": False, 
    "share_emb": False, 
    "task": 'abs', 
    "temp_dir": './document_adaption/summarization/temp', 
    "test_all": False, 
    "test_batch_size": 500, 
    "test_from": './document_adaption/summarization/checkpoint/model_step_148000.pt', 
    "checkpoint_ext": './bertext_cnndm_transformer.pt',
    "checkpoint_abs": './model_step_148000.pt',
    "test_start_from": -1, 
    "train_from": '', 
    "train_steps": 1000, 
    "use_bert_emb": False, 
    "use_interval": True, 
    "visible_gpus": '-1', 
    "warmup_steps": 8000, 
    "warmup_steps_bert": 8000, 
    "warmup_steps_dec": 8000,
    # Tokenizer,
    "min_src_nsents":1,
    "max_src_nsents":100,
    "min_src_ntokens_per_sent":5,
    "max_src_ntokens_per_sent":300,
    "min_tgt_ntokens":0, # non serve ma utilizzato
    "max_tgt_ntokens":0, # non serve ma utilizzato
    "lower":True,
    "use_bert_basic_tokenizer":False,

}

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

args = Struct(**_args)