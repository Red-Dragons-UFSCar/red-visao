# RED 2020

Repositório contendo o código de 2020 utilizado pela equipe Red Dragons

## Para executar o código

- Na raiz do projeto, utilizar os comandos abaixo no terminal para instalar todas as bibliotecas necessárias
```shell
pip install -r requirements.txt
pip install -e ./
```
- Executar o arquivo bin/main.py 
```shell
python ./bin/main.py
```

## Execução com Docker

- Na raiz do projeto, utilize o seguinte comando para criar a imagem:
```shell
docker build -t red ./
```
- Executar a imagem:
```shell
docker run -ti --rm \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    --device /dev/video0 \
    red
```
## Para realizar mudanças
- Crie um branch com o nome de sua mudança.
- Faça as alterações.
- De um merge dela com o código principal apenas quando terminar as alterações.
