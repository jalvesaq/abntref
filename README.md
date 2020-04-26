# ABNTref

This software is no longer being developed. It requires the use of `bib`
files, but it is much better to extract citation keys and references directly
from Zotero database. See [zotcite](https://github.com/jalvesaq/zotcite).

ABNTref formats citations and references in a markdown document according to
ABNT rules. The documentation below is in Portuguese.

Formatação de referências bibliográficas em arquivos markdown, seguindo
o sistema autor-data das normas da ABNT.

## Instalação

No Linux, os arquivos `abntref` e `ABNTref.py` devem estar no mesmo diretório,
e o arquivo `abntref` deve ser executável e ele próprio ou link simbólico
apontando para ele deve estar no `PATH` do sistema. Por exemplo, se a pasta
`~/bin` estiver no `PATH`, digite o seguinte no terminal (substituindo
`/caminho/para/abntref/` pelo endereço completo da pasta do `abntref`:

```
cd ~/bin
ln -s /caminho/para/abntref/abntref
```

Além disso, é necessário instalar a biblioteca `pybtex` para *Python 3*. No
Ubuntu e em outras distros derivadas do Debian, o comando para instalação é:

```
sudo apt install python3-pybtex
```

## Uso

O aplicativo `abntref` pode ser usado de duas formas diferentes: (1) como
filtro do `pandoc`, em substituição ao `pandoc-citeproc`; e (2) como um conversor de
documento markdown com códigos de citação (que se iniciam com `@`) em outro
documento markdown com as citações e referências já formatadas.

Exemplo de uso como filtro:

```
pandoc arquivo.md -o arquivo.pdf --filter abntref
```

Exemplo de uso como conversor:

```
abntref arquivo.md > novo_arquivo.md
```

O `abntref` possui alguns argumentos que modificam o resultado obtido:

  - *ajuda* : Mostra este texto de ajuda.

  - *sem-links* : Não cria link do ano citado para a referência.

  - *latex* : Usa código LaTeX para produzir links.

  - *negrito* : Usa **negrito** para enfatizar títulos.

  - *discreto* : Omite texto de alerta para citações ausentes.

  - *subtítulo* : Realça a parte do título após :?!

  - *completo* : Mostra primeiro nome completo.

  - *url-completa*: Mostra o valor do campo `url` (endereço de internet)
    completo cercado por chevron (`<` e `>`) e sem link ativo. Se esta opção
    estiver ausente, o endereço no link será completo, mas o texto exibido
    para o leitor não incluirá o prefixo “http://” e o restante do endereço
    após a primeira “/”, e também não será incluído chevron.

  - *repetido* : Não substitui nomes repetidos por sublinhados.

  - *normalsize* ou *footnotesize* : Comando LaTeX indicativo do tamanho da
    fonte a ser usada nas referências em arquivos pdf. Se não for indicado,
    será usado tamanho *small*.

  - *singlespacing*, *onehalfspacing* ou *doublespacing* : Comando LaTeX
    indicativo do espaçamento entre parágrafos nas referências. Requer que o
    pacote `setspace` seja carregado no LaTex. Se não for indicado, será
    mantido o espaçamento dos parágrafos anteriores.

  - *obediente* : Contraria regras da língua portuguesa e obedece a ABNT,
    usando ponto-e-vírgula para separar coautores em citações.

  - *arquivo.bib* : Se não for indicado o nome do arquivo .bib, o arquivo.md
    deverá ter um cabeçalho YAML com o campo bibliography definido.

  - *arquivo.md* : Se não for indicado o nome do arquivo .md, o conteúdo
    markdown deve ser passado como input padrão (stdin).


Se o `abntref` estiver sendo usado como filtro, as opções devem ser passadas no
campo `abntref` do cabeçalho `YAML` do arquivo markdown separados por espaço em
branco (veja os [exemplos](https://github.com/jalvesaq/abntref/exemplos)).
Se estiver sendo usado como conversor isoladamente, os argumentos podem ser
passados em qualquer ordem, como nos exemplos abaixo.

```
abntref arquivo.md arquivo.bib > novo.md
abntref arquivo.bib sem-links negrito arquivo.md > novo.md
cat arquivo.md | abntref arquivo.bib | pandoc -o arquivo.html
cat arquivo.md | abntref latex | pandoc -o arquivo.pdf
```

## Tipos de referência reconhecidos

O ABNTref reconhece somente os seguintes tipos de referência em arquivos .bib:

  - *Article* : Artigo de periódico acadêmico ou de jornal de notícias.

  - *Book* : Livro.

  - *InBook* : Capítulo de livro (usado quando foi lido apenas um capítulo de
    um livro escrito por apenas um autor ou uma equipe de coautores).

  - *InCollection* : Capítulo de livro que é uma coletânea de capítulos
    escritos por diferentes autores ou equipes de coautores.

  - *PhdThesis*, *MasterThesis* ou *Monography* : Tese de doutorado,
    Dissertação de mestrado ou Monografia de conclusão de curso.

Se as referências forem de um tipo diferente, serão tratadas como um dos tipos acima.


## Comparação com pandoc-citeproc

  - *Desvantagens*:
 
    - Menor variedade nos tipos de referência formatados.

    - Funciona apenas com bibliografia no formato `.bib`.

    - Desenvolvido e testado apenas no Linux com Pyton 3 e XeLaTex, ou seja,
      com caracteres codificados em UTF-8 (Unicode).

  - *Vantagem*:

    - Segundo as regras da ABNT, os sobrenomes dos autores devem ser escritos
      com letras maiúsculas nas citações entre parênteses, mas deve ser
      escritos normalmente (apenas as iniciais maiúsculas) fora dos
      parênteses. Assim como o `abnTeX2cite`, pacote do LaTeX, o `abntref`
      também faz distinção entre citações que estão dentro e fora dos
      parênteses.

  - *Diferente*:

    - O `abntref` é mais exagerado ao avisar que falta uma referência. Além de
      colocar interrogações no ano da citação não encontrada, ele adiciona um
      texto de alerta em letras maiúsculas na citação e outro nas referências.

    - Se o campo `author` estiver ausente, o campo `organization`, se
      presente, será usado como autor e, neste caso, o nome do “autor” não
      será apresentado de forma invertida nas referências — SOBRENOME, Nome —
      e será apresentado o nome completo nas citações. Isso é útil quando a
      autoria de uma obra é atribuída a uma organização. Se, por exemplo, for
      citada uma lei do estado do Rio Grande do Norte de 2001, espera-se (RIO
      GRANDE DO NORTE, 2001) e não (NORTE, 2001).

    - O campo `org-short` ou o campo `shortauthor`, se presente, será usado
      nas citações e, nas referências, inserida antes do nome do autor ou da
      organização. No exemplo acima, a citação poderia ser resumida para
      (RN, 2001).

    - Quando o output é LaTeX (para produção de pdf), o caractere `\x00ad`
      (*soft hyphen*) é inserido entre cada uma das letras do texto de um link
      nas referências (resultante do campo `url` do arquivo .bib). Isso
      garante que o link seja hifenizado imediatamente antes da primeira letra
      que ultrapassaria a margem do texto.

    - Endereços de internet são abreviados nas referências. Motivo: se o
      trabalho estiver impresso, será mais fácil para o leitor encontrar a
      página referenciada procurando por parte do título ou do endereço da
      página do que tentando digitar com exatidão um longo endereço completo
      na barra de endereços do navegador e, se não estiver impresso, bastará
      clicar no link e, este, sim, precisa estar completo.
