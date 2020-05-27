## Depois do Café - Telegram Bot

Este é o bot do telegram do Depois do Café, a razão dele existir é que temos episódios exclusivos para as pessoas que participam do [grupo](https://chat.depois.cafe) exclusivo do podcast, tendo estes episódios exclusivos, precisamos distribuir ele de alguma forma, então além de termos o FEED RSS, também temos o bot.

A ideia de abrir ele é que o pessoal que quiser ver o código e/ou contribuir, é possível.

### Colocando pra funcionar

Você vai precisar do `Pipenv` para fazer isso.

Além de ter uma key de bot para utilizar aqui, com isso você poderá interagir com o bot, veja [aqui](https://core.telegram.org/bots#6-botfather) como fazer isso.

Com um `pipenv install`, você vai instalar todas as dependencias do projeto e já poderá desenvolver e/ou testar o bot.

### O que o bot faz?

* Retorna a url do RSS FEED `/feed`
* Lista os episódios exclusivos `/episodios`
* Envia episódio selecionado para o grupo `/ouvir_episodio #numero`
* Fala um "Opa" a primeira vez que a pessoa interage no grupo no dia

#### Para ver os próximos passos, só dar uma olhada no [TODO.md](TODO.md)

### Quando tem coisa nova aqui?

Todas as Segundas, Terças e Quartas ás 4 ou 5 da tarde (o dia/horario pode mudar) eu faço live no http://twitch.tv/airtonzanon

