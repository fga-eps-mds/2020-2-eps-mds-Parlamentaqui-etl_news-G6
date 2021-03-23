# etl_news

0- ligar o docker da sua máquina caso não esteja ligado. `Caso esteja no windows`
        
        sudo service docker start

1- Criar um novo arquivo com o nome ".env"

2- Copiar o conteudo de .env.dev (que já está no projeto) para esse novo .env criado

3- `Caso seja algum módulo não seja encontrado` e gere algum erro de compilação, rode o comando:

        make rebuild

Esse comando irá buildar novamente seu docker com todos os módulos do requirements.txt. Caso tenha rodado esse comando, não precisa ir para o passo 4.

4- Rodar o comando:
        
        make start-dev

Esse comando sempre deve ser executado quando quiser iniciar o container do etl_news.

