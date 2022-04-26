# BLACKJACK GAME
Game desenvolvido para o Trabalho Prático da disciplina de Redes de Computadores.
O propósito é fazer uma aplicação usando os conceitos aprendidos em aula. O jogo tem um modelo Cliente-Servidor e utiliza TCP como protocolo de transporte.  

- Darlei Matheus Schmegel [dmschmegel@inf.ufpel.edu.br]
- Felipe Avila Silva [fasilva@inf.ufpel.edu.br]

## Executando o jogo
1.Clone o repositório e instale as dependências
````buildoutcfg
pip install -r requirements.txt
````
2.Na pasta Raiz execute o arquivo server.py e então use o arquivo run.py para rodar o game. O cliente é instanciado dentro do arquivo game.py. 

3.Para rodar o Servidor 

3.1.Parâmetros server.py_ IP PORT
````buildoutcfg
python server.py 127.0.0.1 5555
````
###### Se não passar os argumentos, o _default_ normalmente é  <127.0.0.1> <5555>
4.Então para rodar o Game

4.1Parâmetros run.py IP PORT
`````buildoutcfg
python run.py 127.0.0.1 5555
`````
###### Se não passar os argumentos, o _default_ é normalmente <127.0.0.1> <5555>