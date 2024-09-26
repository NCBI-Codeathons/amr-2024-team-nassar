"""
generate includes all the functions needed for generating training datasets from LLMs
@author: Maaly Nassar
@email:maaly13@yahoo.com
"""

import os
#os.environ["TOKENIZERS_PARALLELISM"] = 'true' # need to be set for transformers tokenizers https://github.com/huggingface/transformers/issues/5486
import sys
import sys
import stat
import re
import json
import time
# import torch
import pathlib
from pathlib import Path
import numpy as np
import pandas as pd
import transformers
from transformers import pipeline, AutoTokenizer, AutoModel, BitsAndBytesConfig, AutoModelForCausalLM

from datasets import Dataset
import torch
from argparse import ArgumentParser
parser = ArgumentParser()


### ADDING ARGUMENTS ###
########################

parser.add_argument('--input','--input',required=True, help='input file path')
parser.add_argument('--prompt','--prompt',required=True, help='prompt json file path')
parser.add_argument('--model','--model',required=True, help='llm name')
parser.add_argument('--output','--output',required=True, help='output file path')
parser.add_argument('--mconfig','--mconfig',required=True, help='quantize,flashattn,bfloat16,float16,auto')
parser.add_argument('--hf_token','--hf_token',required=True, help='huggingface token')
args = parser.parse_args()


os.environ['HF_TOKEN'] = args.hf_token
hf_token = os.getenv('HF_TOKEN')

model_name = args.model
if model_name in ['google/gemma-2-9b']: os.environ['CUDA_LAUNCH_BLOCKING'] = '1' 

mconfig = args.mconfig

### DOWNLOAD INPUT DATAFRAME ###
################################

df = pd.read_csv(Path(args.input))
print(df)

### DOWNLOAD PROMPT FILE ###
############################

with open(Path(args.prompt)) as json_file: prompt = json.load(json_file)
task = prompt['task']
examples = prompt['examples']

### LOAD LLM ###
################
### https://huggingface.co/docs/transformers/en/quantization/bitsandbytes ###
# quantization_config = BitsAndBytesConfig(llm_int8_enable_fp32_cpu_offload=True)
# quantization_config = BitsAndBytesConfig(load_in_8bit=True)
# quantization_config = BitsAndBytesConfig(load_in_4bit=True) # works with large models but slow 
quantization_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.bfloat16) # works and faster
# quantization_config = BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type="nf4") # qlora better for training not inference

mconfigs = {
    'quantize':{"torch_dtype": torch.float16, "quantization_config": quantization_config,"low_cpu_mem_usage": True}, # llama 70b on g5.12xl
    'flashattn':{"torch_dtype": torch.float16, "attn_implementation":"flash_attention_2"}, # flashattn unsupported in p3 ec2
    'bfloat16':{"torch_dtype": torch.bfloat16,"low_cpu_mem_usage": True}, # bfloat16 unsupported in p3 ec2
    'float16':{"torch_dtype": torch.float16,"low_cpu_mem_usage": True},
    'auto':{"torch_dtype": "auto","low_cpu_mem_usage": True}, # qwen model
}

pipeline = transformers.pipeline(
    "text-generation",
    model=model_name,
    model_kwargs=mconfigs[mconfig],
    #device="cuda",
    trust_remote_code=True,
    device_map="auto"
)

### GENERATE OUTPUT ###
#######################

gdf = {'id':[],'input':[],'task':[],'output':[]}
output_file = args.output

start_time = time.time()
#checks = [n for n in range(0,len(df),10)]

for r,row in df.iterrows():
    message = "Instructions: "+task+" Text: "+row['text']
    messages = [*examples,*[{"role":"user","content":message}]]
    prompt = pipeline.tokenizer.apply_chat_template(messages,tokenize=False,add_generation_prompt=True)
    terminators = [pipeline.tokenizer.eos_token_id,pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")]
    outputs = pipeline(prompt,max_new_tokens=4000,eos_token_id=terminators,do_sample=True,temperature=0.2,top_p=0.95,top_k=50)
    output = outputs[0]["generated_text"][len(prompt):]
    gdf['task'].append(task)
    gdf['input'].append(row['text'])
    gdf['output'].append(output)
    gdf['id'].append(row['id'])
    print(output)
    #if r in checks: pd.DataFrame(gdf).to_csv(output_file ,index=False,encoding='utf-8')
    pd.DataFrame(gdf).to_csv(output_file ,index=False,encoding='utf-8') 
    
elapsed_time = time.time() - start_time
