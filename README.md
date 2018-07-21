# ABNTref

Format citations and references in a markdown document according to ABNT rules
(documentation in Portuguese)

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

Além disso, é necessário instalar as bibliotecas `pypandoc` e `pybtex` para
*Python 3*. No Ubuntu e em outras distros derivadas do Debian, os comandos para
instalação são:

```
sudo apt install python3-pypandoc python3-pybtex
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


 -------------------------------------------------------------------------
 **Opção**     **Efeito**
 ------------  -----------------------------------------------------------
 ajuda         mostra este texto de ajuda

 sem-links     não criar link do ano citado para a referência.

 latex         usar código LaTeX para produzir links.

 negrito       usar **negrito** para enfatizar títulos.

 discreto      omitir texto de alerta para citações ausentes.

 subtítulo     realçar a parte do título após :?!

 completo      mostrar primeiro nome completo.

 repetido      não substituir nomes repetidos por sublinhados.

 obediente     contrariar regras da língua portuguesa e obedecer a
               ABNT, usando ponto-e-vírgula para separar coautores
               em citações.

 arquivo.bib   se não for indicado o nome do arquivo .bib, o
               arquivo.md deverá ter um cabeçalho YAML com o campo
               bibliography definido.

 arquivo.md    se não for indicado o nome do arquivo .md, o conteúdo
               markdown deve ser passado como input padrão (stdin).
 -------------------------------------------------------------------------


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

O ABNTref reconhece somente os seguintes tipos de referência:

 -------------------------------------------------------------------------
 **Nome BibTeX**   **Significado**
 ----------------  -------------------------------------------------------
 Article           Artigo de periódico acadêmico ou de jornal de notícias.

 Book              Livro.

 InBook            Capítulo de livro (usado quando foi lido apenas um
                   capítulo de um livro escrito por apenas um autor ou
                   uma equipe de coautores).

 InCollection      Capítulo de livro que é uma coletânea de capítulos
                   escritos por diferentes autores ou equipes de
                   coautores.

 PhdThesis,        Tese de doutorado, Dissertação de mestrado ou
 MasterThesis,     Monografia de conclusão de curso.
 Monography
 -------------------------------------------------------------------------

Se suas referências forem de um tipo diferente, serão tratadas como um dos tipos acima.

## Comparação com pandoc-citeproc

  - *Desvantagens*:
 
    - Menor variedade nos tipos de referência formatados.

    - Funciona apenas com bibliografia no formato `.bib`.

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
