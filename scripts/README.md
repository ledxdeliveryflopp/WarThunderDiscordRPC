## Сборка приложения

```shell
python -m scripts.builder --version "<tag>" --installer-version "<tag>" --path main.py --icon-path <icon/path> --onefile --additional-files <assets/path>
```

## Публикация релиза
```shell
python -m scripts.release --tag "<tag>" --manifest <manifest/path> --assets <assets/path>
```