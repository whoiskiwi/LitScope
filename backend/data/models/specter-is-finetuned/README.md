---
tags:
- sentence-transformers
- sentence-similarity
- feature-extraction
- dense
- generated_from_trainer
- dataset_size:4532
- loss:MultipleNegativesRankingLoss
base_model: sentence-transformers/allenai-specter
widget:
- source_sentence: Group decision support systems cognitive feedback technology acceptance
  sentences:
  - Better Is Better? Signaling Paradoxes in Performance-Based Advertising [SEP] Under
    performance-based advertising, firms pay only for measurable consumer actions,
    such as clicks or sales. However, these actions may result from factors other
    than effective advertising. For example, a high-reputation seller is more likely
    to generate more actions than a low-reputation seller. If such consumer actions
    are counted toward advertising performance, a high-quality firm is penalized
  - 'Cognitive Feedback in GDSS: Improving Control and Convergence [SEP] Cognitive
    feedback in group decision making is information that provides decision makers
    with a better understanding of their own decision processes and that of the other
    group members. It appears to be an effective aid in group decision making. Although
    it has been suggested as a potential feature of group decision support systems
    (GDSS), little research has examined its use and impact. This arti'
  - Why Break the Habit of a Lifetime? Rethinking the Roles of Intention, Habit, and
    Emotion in Continuing Information Technology use1 [SEP] One of the most welcome
    recent developments in Information Systems scholarship has been the growing interest
    in individuals’ continuing use of information technology well after initial adoption,
    known in the literature as IT usage, IT continuance, and post-adoptive IT usage.
    In this essay, we explore the theoretical underpinnings of IS research on continuing
    IT use. Although the IS literature on c
- source_sentence: social feedback effects on consumer self-design technology acceptance
  sentences:
  - 'Turnover of Information Technology Workers: Examining Empirically the Influence
    of Attitudes, Job Characteristics, and External Markets [SEP] (2002). Turnover
    of Information Technology Workers: Examining Empirically the Influence of Attitudes,
    Job Characteristics, and External Markets. Journal of Management Information Systems:
    Vol. 19, No. 3, pp. 231-261.'
  - 'After-Hours Telecommuting and Work-Family Conflict: A Comparative Analysis [SEP]
    After-hours telecommuting (AHT) is a work arrangement where job-relevant work
    is done at home on a computer outside of regular office hours. This study examined
    how after-hours telecommuting affects an individual''s ability to balance work
    and family demands (measured as role overload, spillover of interference from
    work to family and spillover of interference from family to work). It also examined'
  - 'When Social Media Can Be Bad for You: Community Feedback Stifles Consumer Creativity
    and Reduces Satisfaction with Self-Designed Products [SEP] Enabling consumers
    to self-design unique products that match their idiosyncratic preferences is the
    key value driver of modern mass customization systems. These systems are increasingly
    becoming “social,” allowing for consumer-to-consumer interactions such as commenting
    on each other''s self-designed products. The present research examines how receiving
    others'' feedback on initial product configura'
- source_sentence: Signaling theory and risk communication in peer-to-peer funding
  sentences:
  - 'Information Technology Identity: A Key Determinant of IT Feature and Exploratory
    Usage [SEP] Creative information technology usage by employees is the critical
    link between business technology investments and competitive advantage in a digital
    economy. However, to realize anticipated benefits, organizational leaders need
    a richer understanding of what drives individuals’ innovation with incumbent organizational
    technologies. In support of that aim, this study theorized the processes by wh'
  - Risk Disclosure in Crowdfunding [SEP] How should crowdfunding platforms alleviate
    information asymmetry between creators and crowdfunders? In traditional financial
    markets, public companies are required to disclose potential risks to their investors,
    and such risk disclosure requirements are enforced by legal and fiduciary regulations.
    In the crowdfunding context, however, such information asymmetry concerns are
    often addressed by cro
  - Examining the Differential Effectiveness of Fear Appeals in Information Security
    Management Using Two-Stage Meta-Analysis [SEP] Most of the information security
    management research involving fear appeals is guided by either protection motivation
    theory or the extended parallel processing model. Over time, extant research has
    extended these theories, as well as their derivative theories, in a variety of
    ways, leading to several theoretical and empirical inconsistencies. The large
    body of fragmented, and sometimes conflictin
- source_sentence: Reducing information search cost in wellness programs through algorithmic
    personalization
  sentences:
  - When to Broadcast? Inventory Disclosure Policies for Online Sales of Limited Inventory
    [SEP] Online sales of limited inventory such as flash sales and lightning deals
    have become popular among e-commerce retailers including Amazon and eBay. This
    study focuses on the retailer’s best timing of disclosing inventory information
    to maximize the expected sales in a finite horizon. We consider how two prominent
    customer mechanisms, herding effect and scarcity effect, affect the relative performa
  - 'Virtual Team Efficacy Theory: An Integrative Sociotechnical Understanding of
    the Emergence and Ramifications of Collective Efficacy in Virtual Teams [SEP]
    Virtual Team Efficacy Theory Digital technologies facilitate interactions among
    geographically distributed virtual team members. However, some organizations treat
    communication technologies as passive tools rather than active actors influencing
    the relationships between collaborative parties. Researchers have encouraged this
    indifference by applying concepts developed for traditional teams in stud'
  - 'Spoiled for Choice? Personalized Recommendation for Healthcare Decisions: A Multiarmed
    Bandit Approach [SEP] Choice overload is a common problem in many online settings,
    including healthcare. Online healthcare platforms tend to provide a large variety
    of behavior intervention information or programs to help individuals modify their
    lifestyles to improve wellness. However, having too many options can significantly
    increase searching cost, prevent users from discovering the truly relevant interventions,
    an'
- source_sentence: effect of reviewer anonymity versus identity disclosure on sales
    in digital marketplaces
  sentences:
  - The impact of chatbot conversational skill on engagement and perceived humanness
    [SEP] Conversational agents (CAs)—frequently operationalized as chatbots—are computer
    systems that leverage natural language processing to engage in conversations with
    human users. CAs are often operationalized as chatbots which are used for many
    applications including technical support, customer service, and digital personal
    assistants. Despite their widespread use, little research to date has investig
  - 'Examining the Relationship Between Reviews and Sales: The Role of Reviewer Identity
    Disclosure in Electronic Markets [SEP] Consumer-generated product reviews have
    proliferated online, driven by the notion that consumers'' decision to purchase
    or not purchase a product is based on the positive or negative information about
    that product they obtain from fellow consumers. Using research on information
    processing as a foundation, we suggest that in the context of an online community,
    reviewer disclosure of identity-descrip'
  - 'Adoption Patterns and Attitudinal Development in Computer-Supported Meetings:
    An Exploratory Study with SAMM [SEP] :To permit exploration of the development
    of attitudes in a group decision support system environment, eight groups of four
    and five persons each met in a computer-supported conference room over a period
    of two months. Each group addressed two strategic planning tasks, meeting for
    a total of eight two-hour sessions. The computer support provided was Software-Aided
    Meeting Management (SAMM),2 a sys'
pipeline_tag: sentence-similarity
library_name: sentence-transformers
---

# SentenceTransformer based on sentence-transformers/allenai-specter

This is a [sentence-transformers](https://www.SBERT.net) model finetuned from [sentence-transformers/allenai-specter](https://huggingface.co/sentence-transformers/allenai-specter). It maps sentences & paragraphs to a 768-dimensional dense vector space and can be used for semantic textual similarity, semantic search, paraphrase mining, text classification, clustering, and more.

## Model Details

### Model Description
- **Model Type:** Sentence Transformer
- **Base model:** [sentence-transformers/allenai-specter](https://huggingface.co/sentence-transformers/allenai-specter) <!-- at revision 2c68eeca61259b2dd70c3f2628219f925df7031a -->
- **Maximum Sequence Length:** 512 tokens
- **Output Dimensionality:** 768 dimensions
- **Similarity Function:** Cosine Similarity
<!-- - **Training Dataset:** Unknown -->
<!-- - **Language:** Unknown -->
<!-- - **License:** Unknown -->

### Model Sources

- **Documentation:** [Sentence Transformers Documentation](https://sbert.net)
- **Repository:** [Sentence Transformers on GitHub](https://github.com/huggingface/sentence-transformers)
- **Hugging Face:** [Sentence Transformers on Hugging Face](https://huggingface.co/models?library=sentence-transformers)

### Full Model Architecture

```
SentenceTransformer(
  (0): Transformer({'max_seq_length': 512, 'do_lower_case': False, 'architecture': 'BertModel'})
  (1): Pooling({'word_embedding_dimension': 768, 'pooling_mode_cls_token': True, 'pooling_mode_mean_tokens': False, 'pooling_mode_max_tokens': False, 'pooling_mode_mean_sqrt_len_tokens': False, 'pooling_mode_weightedmean_tokens': False, 'pooling_mode_lasttoken': False, 'include_prompt': True})
)
```

## Usage

### Direct Usage (Sentence Transformers)

First install the Sentence Transformers library:

```bash
pip install -U sentence-transformers
```

Then you can load this model and run inference.
```python
from sentence_transformers import SentenceTransformer

# Download from the 🤗 Hub
model = SentenceTransformer("sentence_transformers_model_id")
# Run inference
sentences = [
    'effect of reviewer anonymity versus identity disclosure on sales in digital marketplaces',
    "Examining the Relationship Between Reviews and Sales: The Role of Reviewer Identity Disclosure in Electronic Markets [SEP] Consumer-generated product reviews have proliferated online, driven by the notion that consumers' decision to purchase or not purchase a product is based on the positive or negative information about that product they obtain from fellow consumers. Using research on information processing as a foundation, we suggest that in the context of an online community, reviewer disclosure of identity-descrip",
    'The impact of chatbot conversational skill on engagement and perceived humanness [SEP] Conversational agents (CAs)—frequently operationalized as chatbots—are computer systems that leverage natural language processing to engage in conversations with human users. CAs are often operationalized as chatbots which are used for many applications including technical support, customer service, and digital personal assistants. Despite their widespread use, little research to date has investig',
]
embeddings = model.encode(sentences)
print(embeddings.shape)
# [3, 768]

# Get the similarity scores for the embeddings
similarities = model.similarity(embeddings, embeddings)
print(similarities)
# tensor([[ 1.0000,  0.7766, -0.0767],
#         [ 0.7766,  1.0000,  0.0307],
#         [-0.0767,  0.0307,  1.0000]])
```

<!--
### Direct Usage (Transformers)

<details><summary>Click to see the direct usage in Transformers</summary>

</details>
-->

<!--
### Downstream Usage (Sentence Transformers)

You can finetune this model on your own dataset.

<details><summary>Click to expand</summary>

</details>
-->

<!--
### Out-of-Scope Use

*List how the model may foreseeably be misused and address what users ought not to do with the model.*
-->

<!--
## Bias, Risks and Limitations

*What are the known or foreseeable issues stemming from this model? You could also flag here known failure cases or weaknesses of the model.*
-->

<!--
### Recommendations

*What are recommendations with respect to the foreseeable issues? For example, filtering explicit content.*
-->

## Training Details

### Training Dataset

#### Unnamed Dataset

* Size: 4,532 training samples
* Columns: <code>sentence_0</code> and <code>sentence_1</code>
* Approximate statistics based on the first 1000 samples:
  |         | sentence_0                                                                        | sentence_1                                                                          |
  |:--------|:----------------------------------------------------------------------------------|:------------------------------------------------------------------------------------|
  | type    | string                                                                            | string                                                                              |
  | details | <ul><li>min: 7 tokens</li><li>mean: 11.71 tokens</li><li>max: 19 tokens</li></ul> | <ul><li>min: 41 tokens</li><li>mean: 87.64 tokens</li><li>max: 120 tokens</li></ul> |
* Samples:
  | sentence_0                                                                                          | sentence_1                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
  |:----------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
  | <code>theory of planned behavior workplace software misuse</code>                                   | <code>Software Piracy in the Workplace [SEP] Theft of software and other intellectual property has become one of the most visible problems in computing today. This paper details the development and empirical validation of a model of software ...</code>                                                                                                                                                                                                                             |
  | <code>managing user expectations and perceived performance gaps in IT services</code>               | <code>Zones of tolerance [SEP] The expectation norm of Information Systems SERVQUAL has been challenged on both conceptual and empirical grounds, drawing into question the instrument's practical value. To address the criticism t...</code>                                                                                                                                                                                                                                           |
  | <code>Social Information Processing theory computer-mediated communication group development</code> | <code>Relational Development in Computer-Supported Groups1 [SEP] This study examines how group attitudes and outcomes evolve over time with repeated use of a group support system. Social Information Processing (SIP) theory, which suggests that relational intimacy may take longer to develop in computer-supported groups, was used as the basis for testing a temporally bounded model of group behavior. The basic argument underlying this model is that computer-suppor</code> |
* Loss: [<code>MultipleNegativesRankingLoss</code>](https://sbert.net/docs/package_reference/sentence_transformer/losses.html#multiplenegativesrankingloss) with these parameters:
  ```json
  {
      "scale": 20.0,
      "similarity_fct": "cos_sim",
      "gather_across_devices": false,
      "directions": [
          "query_to_doc"
      ],
      "partition_mode": "joint",
      "hardness_mode": null,
      "hardness_strength": 0.0
  }
  ```

### Training Hyperparameters
#### Non-Default Hyperparameters

- `per_device_train_batch_size`: 16
- `per_device_eval_batch_size`: 16
- `multi_dataset_batch_sampler`: round_robin

#### All Hyperparameters
<details><summary>Click to expand</summary>

- `do_predict`: False
- `eval_strategy`: no
- `prediction_loss_only`: True
- `per_device_train_batch_size`: 16
- `per_device_eval_batch_size`: 16
- `gradient_accumulation_steps`: 1
- `eval_accumulation_steps`: None
- `torch_empty_cache_steps`: None
- `learning_rate`: 5e-05
- `weight_decay`: 0.0
- `adam_beta1`: 0.9
- `adam_beta2`: 0.999
- `adam_epsilon`: 1e-08
- `max_grad_norm`: 1
- `num_train_epochs`: 3
- `max_steps`: -1
- `lr_scheduler_type`: linear
- `lr_scheduler_kwargs`: None
- `warmup_ratio`: None
- `warmup_steps`: 0
- `log_level`: passive
- `log_level_replica`: warning
- `log_on_each_node`: True
- `logging_nan_inf_filter`: True
- `enable_jit_checkpoint`: False
- `save_on_each_node`: False
- `save_only_model`: False
- `restore_callback_states_from_checkpoint`: False
- `use_cpu`: False
- `seed`: 42
- `data_seed`: None
- `bf16`: False
- `fp16`: False
- `bf16_full_eval`: False
- `fp16_full_eval`: False
- `tf32`: None
- `local_rank`: -1
- `ddp_backend`: None
- `debug`: []
- `dataloader_drop_last`: False
- `dataloader_num_workers`: 0
- `dataloader_prefetch_factor`: None
- `disable_tqdm`: False
- `remove_unused_columns`: True
- `label_names`: None
- `load_best_model_at_end`: False
- `ignore_data_skip`: False
- `fsdp`: []
- `fsdp_config`: {'min_num_params': 0, 'xla': False, 'xla_fsdp_v2': False, 'xla_fsdp_grad_ckpt': False}
- `accelerator_config`: {'split_batches': False, 'dispatch_batches': None, 'even_batches': True, 'use_seedable_sampler': True, 'non_blocking': False, 'gradient_accumulation_kwargs': None}
- `parallelism_config`: None
- `deepspeed`: None
- `label_smoothing_factor`: 0.0
- `optim`: adamw_torch_fused
- `optim_args`: None
- `group_by_length`: False
- `length_column_name`: length
- `project`: huggingface
- `trackio_space_id`: trackio
- `ddp_find_unused_parameters`: None
- `ddp_bucket_cap_mb`: None
- `ddp_broadcast_buffers`: False
- `dataloader_pin_memory`: True
- `dataloader_persistent_workers`: False
- `skip_memory_metrics`: True
- `push_to_hub`: False
- `resume_from_checkpoint`: None
- `hub_model_id`: None
- `hub_strategy`: every_save
- `hub_private_repo`: None
- `hub_always_push`: False
- `hub_revision`: None
- `gradient_checkpointing`: False
- `gradient_checkpointing_kwargs`: None
- `include_for_metrics`: []
- `eval_do_concat_batches`: True
- `auto_find_batch_size`: False
- `full_determinism`: False
- `ddp_timeout`: 1800
- `torch_compile`: False
- `torch_compile_backend`: None
- `torch_compile_mode`: None
- `include_num_input_tokens_seen`: no
- `neftune_noise_alpha`: None
- `optim_target_modules`: None
- `batch_eval_metrics`: False
- `eval_on_start`: False
- `use_liger_kernel`: False
- `liger_kernel_config`: None
- `eval_use_gather_object`: False
- `average_tokens_across_devices`: True
- `use_cache`: False
- `prompts`: None
- `batch_sampler`: batch_sampler
- `multi_dataset_batch_sampler`: round_robin
- `router_mapping`: {}
- `learning_rate_mapping`: {}

</details>

### Training Logs
| Epoch  | Step | Training Loss |
|:------:|:----:|:-------------:|
| 1.7606 | 500  | 0.2438        |


### Framework Versions
- Python: 3.12.13
- Sentence Transformers: 5.3.0
- Transformers: 5.0.0
- PyTorch: 2.10.0+cu128
- Accelerate: 1.13.0
- Datasets: 4.0.0
- Tokenizers: 0.22.2

## Citation

### BibTeX

#### Sentence Transformers
```bibtex
@inproceedings{reimers-2019-sentence-bert,
    title = "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks",
    author = "Reimers, Nils and Gurevych, Iryna",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing",
    month = "11",
    year = "2019",
    publisher = "Association for Computational Linguistics",
    url = "https://arxiv.org/abs/1908.10084",
}
```

#### MultipleNegativesRankingLoss
```bibtex
@misc{oord2019representationlearningcontrastivepredictive,
      title={Representation Learning with Contrastive Predictive Coding},
      author={Aaron van den Oord and Yazhe Li and Oriol Vinyals},
      year={2019},
      eprint={1807.03748},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/1807.03748},
}
```

<!--
## Glossary

*Clearly define terms in order to be accessible across audiences.*
-->

<!--
## Model Card Authors

*Lists the people who create the model card, providing recognition and accountability for the detailed work that goes into its construction.*
-->

<!--
## Model Card Contact

*Provides a way for people who have updates to the Model Card, suggestions, or questions, to contact the Model Card authors.*
-->