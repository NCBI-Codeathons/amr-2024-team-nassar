# GraphRAG with Result and Discussion Section of Literatures

```bash
cd literature_analysis/graphrag_result_and_discussion
python -m graphrag.index --init --root . # if not initialized
python -m graphrag.prompt_tune --root . --config ./settings.yaml --domain "self-resistance genes" --limit 10 --language English --max-tokens 2048 --chunk-size 256 --min-examples-required 3 --no-entity-types --output ./auto_tuning
python -m graphrag.index --root .
```