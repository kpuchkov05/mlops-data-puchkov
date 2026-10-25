# Отчёт по практической работе № 3

## Окружение

| Компонент | Версия |
|---|---:|
| Python | 3.12.15 |
| DVC | 3.66.1 |
| ClearML | 2.1.4 |
| scikit-learn | 1.8.0 |
| pandas | 3.0.1 |

Git-репозиторий: <https://github.com/kpuchkov05/mlops-data-puchkov>

## DVC

### Версии и история Git

| Состояние данных | Git commit | Git tag | SHA-256 `data.dvc` |
|---|---|---|---|
| Базовый Iris | `432b68de32e50ddac5eafeee28dd8adfe2f4fe18` | `data-v1` | `af9a6b92231af3d30166d4ec05038ab3fdebc3f28a1de1bea4cea5449e7fde76` |
| Iris и Wine | `b934ed8213d142a6a3228631708443e10e7ca8a2` | — | `c42cbceead4c55e97976c576e2bc8dd9ab7037d776a1eff253e8ecde3170ff24` |
| Iris с вычисляемыми признаками | `12e88145a96d4b032fc212b24581a9c65417d641` | — | `e6ba0d79a80bff8042f21fd623be1788c9babbd1a70a0fcc9293dbf4be1212c9` |
| Объединённая версия | `330ca928582b6e2a68e69362e2b6494fe2fb5bb8` | — | `b63003486e5847feba08f387096e7a53191e49eae92790a231dc6c99bbce7692` |
| Объединённая версия в `main` | `746b5cf074a56ae60155f91f0bea302c4df1b1b8` | — | `b63003486e5847feba08f387096e7a53191e49eae92790a231dc6c99bbce7692` |

Коммит настройки remote: `c13d240`. Ветки `feature/wine` и
`feature/iris-features` сохранены в истории. Merge driver DVC объединил
`data.dvc` без конфликтных маркеров, после чего `dvc checkout` восстановил
объединённый workspace.

### DVC remote

Remote `local-storage` — отдельная локальная директория вне Git-репозитория:

```text
/Users/kirillpuckov/Documents/Codex/2026-10-25/gb/work/mlops-data-puchkov-dvc-remote
```

В remote отправлены объекты всех версий. После базового `dvc push` локальные
`.dvc/cache` и `data` были удалены. Команда `dvc pull` заново восстановила
базовый Iris с тем же SHA-256, поэтому версия не зависела от старого cache.

### Итоговые CSV

| Файл | SHA-256 | Форма | Столбцы |
|---|---|---:|---|
| `data/iris.csv` | `3e1ba63f55da2aabc432d00b1670140f5162bf9ef34b837598ec2fc176c9ff26` | 150 × 7 | исходные 4 признака, `target`, `sepal_area`, `petal_area` |
| `data/wine.csv` | `38860ba04ace4d402242340bcf40be4bd6f4ebde9144a3dc89dc12c20f7f8e60` | 178 × 14 | 13 исходных признаков и `target` |

Базовый `iris.csv` имел SHA-256
`6d700503c9c2e2c71d187b889a87af8a8d3a6dd5bae1266d46f4ee4db5a6349f`.
В ветке `feature/wine` этот хэш не изменился.

### Чистое восстановление

Репозиторий клонирован в новую пустую директорию без переноса workspace и
cache. Выполнены `dvc pull` и `python check_data.py --expect both`.

Результат:

```text
3 files fetched and 2 files added
iris.csv: 150 × 7, SHA-256 3e1ba63f55da2aabc432d00b1670140f5162bf9ef34b837598ec2fc176c9ff26
wine.csv: 178 × 14, SHA-256 38860ba04ace4d402242340bcf40be4bd6f4ebde9144a3dc89dc12c20f7f8e60
```

Хэши, формы и столбцы совпали с исходным репозиторием.

## ClearML Dataset

Использованы:

```text
project: MIIT/MLOps/practice_3/puchkov
dataset name: sklearn-tabular-puchkov
```

### Идентификаторы и lineage

```text
BASE_ID=55f4c4c2fd8b41fb891123bf8f8bfde4
WINE_ID=fb3ef373e5b44071bf82b1ee35efaac9
IRIS_FEATURES_ID=93d8981c391d49b09bdee6f943f01beb
```

Dependency graph:

```text
55f4c4c2fd8b41fb891123bf8f8bfde4 -> []
fb3ef373e5b44071bf82b1ee35efaac9 -> [55f4c4c2fd8b41fb891123bf8f8bfde4]
93d8981c391d49b09bdee6f943f01beb -> [55f4c4c2fd8b41fb891123bf8f8bfde4]
```

Таким образом, версии `1.1.0` и `2.0.0` образуют две отдельные ветви от базы;
`WINE_ID` не является предком `IRIS_FEATURES_ID`.

### Проверка скачанных версий

Каждая версия была получена строго по Dataset ID и скачана в отдельную пустую
директорию.

#### Version 1.0.0

- ID: `55f4c4c2fd8b41fb891123bf8f8bfde4`;
- parents: отсутствуют;
- полный состав: `iris.csv`;
- added: `iris.csv`; modified: нет; removed: нет;
- `iris.csv`: SHA-256
  `6d700503c9c2e2c71d187b889a87af8a8d3a6dd5bae1266d46f4ee4db5a6349f`,
  форма 150 × 5, исходные признаки Iris и `target`.

#### Version 1.1.0

- ID: `fb3ef373e5b44071bf82b1ee35efaac9`;
- parent: `55f4c4c2fd8b41fb891123bf8f8bfde4`;
- полный состав: `iris.csv`, `wine.csv`;
- added: `wine.csv`; modified: нет; removed: нет;
- `iris.csv`: SHA-256
  `6d700503c9c2e2c71d187b889a87af8a8d3a6dd5bae1266d46f4ee4db5a6349f`,
  форма 150 × 5;
- `wine.csv`: SHA-256
  `38860ba04ace4d402242340bcf40be4bd6f4ebde9144a3dc89dc12c20f7f8e60`,
  форма 178 × 14.

#### Version 2.0.0

- ID: `93d8981c391d49b09bdee6f943f01beb`;
- parent: `55f4c4c2fd8b41fb891123bf8f8bfde4`;
- полный состав: `iris.csv`;
- added: нет; modified: `iris.csv`; removed: нет;
- `iris.csv`: SHA-256
  `3e1ba63f55da2aabc432d00b1670140f5162bf9ef34b837598ec2fc176c9ff26`,
  форма 150 × 7, исходные столбцы плюс `sepal_area` и `petal_area`.

## Сравнение DVC и ClearML Dataset

| Наблюдение | DVC | ClearML Dataset |
|---|---|---|
| Идентификатор версии | Git commit выбирает конкретный `data.dvc`; внутри него находится DVC-хэш каталога | Каждый созданный Dataset получил отдельный неизменяемый ID |
| Расположение метаданных | `.dvc/config`, `data.dvc` и их Git history | ClearML Server хранит version, ID, tags и lineage |
| Расположение файлов | Локальный DVC remote вне репозитория | ClearML File Server; все три версии удалось скачать по ID |
| Создание дочерней версии | Новая Git-ветка, изменение данных, `dvc add`, Git commit | Новый `Dataset.create(..., parent_datasets=[BASE_ID])` |
| Переключение версии | `git switch` меняет метаданные, затем `dvc checkout` меняет workspace | `Dataset.get(dataset_id=...)` выбирает точную версию независимо от текущей ветви |
| Чистое восстановление | Clone получил файлы через `dvc pull` из remote | Три пустые директории заполнены через скачивание соответствующих Dataset ID |
| Ветвление | `feature/wine` и `feature/iris-features` созданы от `main` | `1.1.0` и `2.0.0` имеют один `BASE_ID`, но не являются предками друг друга |
| Слияние | DVC merge driver объединил directory output; итог проверен и отправлен в remote | Автоматического аналога Git merge не использовалось; при необходимости создаётся новый Dataset с выбранными parents и явным разрешением файлов |
| Связь с Git | Версия данных определяется содержимым `data.dvc` в конкретном commit | Dataset IDs существуют на ClearML Server независимо от Git commits |
| Доступность через UI | Репозиторий показывает только DVC-метаданные; содержимое находится в remote | ClearML UI показывает версии, статусы Completed, файлы и lineage |

## Ответы на вопросы

1. **Какой объект однозначно определяет версию данных в DVC?**  
   DVC-хэш output в `data.dvc`. В Git-процессе конкретное состояние выбирается
   Git-коммитом, содержащим этот `data.dvc`.

2. **Почему одного Git-коммита недостаточно без DVC remote?**  
   Git хранит метаданные и хэш, но не содержимое CSV. После удаления локального
   cache восстановить файлы можно только из DVC remote.

3. **Чем Dataset version отличается от Dataset ID в ClearML?**  
   Version (`1.0.0`, `1.1.0`, `2.0.0`) — читаемая метка внутри имени и проекта.
   Dataset ID — глобальный идентификатор конкретного объекта, по которому он был
   однозначно получен и скачан.

4. **Почему `finalize()` нельзя считать созданием следующей версии?**  
   `finalize()` делает текущий Dataset неизменяемым и переводит его в Completed.
   Следующая версия появляется только после отдельного `Dataset.create()` и
   получает новый ID.

5. **Как доказать, что version 2.0.0 создана от базы, а не от 1.1.0?**  
   Dependency graph для `IRIS_FEATURES_ID` содержит единственного родителя
   `BASE_ID`; `WINE_ID` в графе отсутствует. Полный состав `2.0.0` также не
   содержит `wine.csv`.

6. **Что произойдёт, если после `git switch` не выполнить DVC checkout?**  
   `data.dvc` будет относиться к новой ветке, а файлы workspace могут остаться от
   предыдущей. Возникает несогласованное состояние, которое покажет `dvc status`.

7. **В каком сценарии удобнее DVC, а в каком ClearML Dataset?**  
   DVC удобнее для данных, которые должны меняться вместе с Git-ветками кода и
   объединяться в Git workflow. ClearML Dataset удобнее для публикации
   неизменяемых версий, явного lineage, скачивания по ID и просмотра через UI
   без переключения Git-веток.
