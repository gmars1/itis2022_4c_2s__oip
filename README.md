# itis2022_4c_2s__oip

> Газизов Марсель, 11-202

---

## before all

```bash
pip install -r requirements.txt
```

## task1

```bash
python -m task1.target_list_generator
```
> заполнить `task1/target_list.txt`


```bash
python -m task1.crawler
```
> скачать страницы в `task1/crawled/`, заполнить `task1/index.txt`

## task2 

```bash
python -m task2.setup
```
> загрузить необходимые библиотеки


```bash
python -m task2.main
```
> заполнить `task2/lemmas.txt`, `task2/tokens.txt`
>
> заполнить `task2/tokens/`, `task2/lemmas/` для каждого файла
> 
> требуется:
> - `task1/crawled/`

## task3 

```bash
python -m task3.invert_index_creator
```
> заполнить `task3/invert_index.txt`, `task3/lemmas_invert_index.txt`, 
> 
> требуется:
> - `task2/tokens.txt`
> - `task2/lemmas.txt`
> - `task1/crawled/`

```bash
python -m task3.search
```
> cli для поиска


## task4

```bash
python -m task4.main
```
> заполнить `task4/tfidf_lemmas/`, `task4/tfidf_tokens`
> 
> требуется:
> - `/task2/tokens.txt` 
> - `task2/lemmas.txt` 
> - `task3/invert_index.txt`
