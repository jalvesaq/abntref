---
title: "Comparação: abnTeX2cite, pandoc-citeproc e abntref"
author: "Jakson Alves de Aquino"
date: "20 de julho de 2018"
bibliography: "bibliografia.bib"
abntref: "obediente url-completa"
csl: "abnt.csl"
...

## Citações

Colchetes são substituídos por parênteses, então, se quisermos citar dois
autores no próprio texto, o primeiro fora dos parênteses e o segundo entre
parênteses, basta digitar, por exemplo, @gomes1998 e [@costa1998]. Para citar
vários autores simultaneamente, basta separar os códigos de citação da forma
que se desejar [por exemplo: @nbr60232000; @secretaria1989; @ibict1993, p. 22].
Observe que o campo `shortauthor` ou `org-short` será usado para fazer a
citação se estiver presente no arquivo `.bib`, o que possibilita o uso de
siglas (como ABNT) em substituição a nomes completos, e que também é útil
quando o “autor” é uma organização, como o estado de São paulo, não tendo nome
e sobrenome.

O estilo definido no arquivo `abnt.csl` foi ajustado para produzir formatação
semelhante à do `abntref`. Por isso, a principal diferença será nas citações
fora dos parênteses, pois, com o `pandoc-citeproc`, não é possível seguir
regras diferentes para citações dentro e fora dos parênteses, sendo
necessário, no segundo caso, escrever, por exemplo, Gomes -@gomes1998. Esta é
a única vantagem importante do `abntref` sobre o `pandoc-citeproc`; outras
pequenas diferenças na formatação do `pandoc-citeproc` poderiam ser eliminadas
com ajustes no `abnt.csl` ou no `ABNTref.py`.

Para comparar o resultado do processamento deste documento pelo `abntref` com
o do `pandoc-citeproc`, use os seguintes comandos no terminal do Linux:

```
pandoc comparacao.md -o citeproc.pdf --filter pandoc-citeproc
pandoc comparacao.md -o abntref.pdf --filter abntref
```

## Referências copiadas do abnTeX2cite

Esta seção contém alguns exemplos de referências copiadas de:

ARAUJO, Lauro César.
*O pacote abnTeX2cite:* Estilos bibliográficos compatíveis com a ABNT NBR 6023.
26 de fevereiro de 2016, v-1.9.6.

O objetivo é permitir a comparação da formatação do `abnTeX2cite` com a que é
feita pelo `abntref` e pelo `pandoc-citeproc`.

A principal diferença entre o `abntref` e o `abnTeX2cite` é que o `abntref`
usa o campo `shortauthor` (ou `org-short`) nas citações e insere este campo
antes do nome do autor nas referências, usando um travessão para separar os
dois, como no primeiro exemplo a seguir em que é citado um manual da ABNT.

  - **Manual** [@nbr60232000]:

    ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. *NBR 6023*:
    Informação e documentação — referências — elaboração. Rio de Janeiro, 2000. 22 p.

  - **Tese** [@barcelos1998]:

    BARCELOS, M. F. P.
    *Ensaio tecnológico, bioquímico e sensorial de soja e gandu enlatados no estágio verde e maturação de colheita*. 1998. 160 f.
    Tese (Doutorado em Nutrição) — Faculdade de Engenharia de Alimentos, Universidade Estadual de Campinas, Campinas.

  - **Artigo** de periódico com *section* [@costa1998]:

    COSTA, V. R. À margem da lei: o programa comunidade solidária. *Em Pauta*
    — Revista da Faculdade de Serviço Social da UERJ, Rio de Janeiro, n. 12, p.
    131–148, 1998.

  - **Livro** parte de coleção [@gomes1998]:

    GOMES, L. G. F. F. *Novela e sociedade no Brasil*. Niterói:
    EdUFF, 1998. 137 p., 21 cm. (Coleção Antropologia e Ciência Política, 15).
    Bibliografia: p. 131–132. ISBN 85-228-0268-8.

  - **Livreto** [@ibict1993]:

    IBICT. *Manual de normas de editoração do IBICT*. 2. ed. Brasília, DF, 1993. 41 p.

  - **InCollection** [@romano1996]:

    ROMANO, G. Imagens da juventude na era moderna.
    In: LEVI, G.; SCHMIDT, J. (Org.). *História dos jovens 2*: a época contemporânea.
    São Paulo: Companhia das Letras, 1996. p. 7–16.

  - **Inbook** sem definição de editor [@santos1994]:

    SANTOS, F. R. dos. A colonização da terra do tucujús.
    In: \_\_\_\_\_. *História do Amapá, 1º grau*. 2. ed. Macapá: Valcan, 1994. cap. 3, p. 15–24.

  - **Manual** [@secretaria1989]:

    SÃO PAULO (Estado). Secretaria do Meio Ambiente. Coordenadoria de Planejamento Ambiental.
    *Estudo de impacto ambiental — EIA, Relatório de Impacto Ambiental — RIMA*: manual de orientação.
    São Paulo, 1989. 48 p. (Série Manuais).

  - **Livro** com coautores não identificados [@franca1996]:

    FRANÇA, J. L. et al. *Manual para normalização de publicações técnico-científicas*. 3. ed. rev. e aum.
    Belo Horizonte: Ed. da UFMG, 1996. 

  - **Anais** de congresso [@martin1997]:

    MARTIN NETO, L.; BAYER, C.; MIELNICZUK, J. Alterações qualitativas
    da matéria orgânica e os fatores determinantes da sua estabilidade num solo
    podzólico vermelho-escuro em diferentes sistemas de manejo. In: CONGRESSO
    BRASILEIRO DE CIÊNCIA DO SOLO, 26., 1997, Rio de Janeiro. *Resumos...* Rio
    de Janeiro: Sociedade Brasileira de Ciência do Solo, 1997. p. 443. Ref. 6–141.

  - *Artigo* de lei [@brasil1999] com endereço da página e data de acesso
    atualizados:

    BRASIL. Lei n o 9.887, de 7 de dezembro de 1999. altera a legislação
    tributária federal. *Diário Oficial \[da\] República Federativa do Brasil*,
    Brasília, DF, 8 dez. 1999.
    Disponível em: \<<http://www.in.gov.br/mp_leis/leis_texto.aps?Id=Lei%209887>\>.
    Acesso em: 22 dez. 1999.

# Referências
