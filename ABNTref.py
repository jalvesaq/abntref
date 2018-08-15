# -*- coding: utf-8 -*-

import sys
import io
import re
import json
import subprocess
from pybtex.database import parse_file

class ABNTref(object):
    """ Format citations and references in a markdown document according to ABNT rules """

    _m = None  # Lines of markdown document
    _b = None  # Name of bib file
    _k = []    # List of cited keys
    _e = {}    # Dictionary with bib entries
    _j = False # Is the standard input JSON?
    _d = ''    # Metadata in JSON format

    # Options
    _o = {'type': 'html', 'anchor': True, 'em': '*', 'discreet': False,
          'compl': False, 'oldurl': False, 'repeat': False, 'obey': False,
          'subttl': False, 'spacing': '', 'font-size': 'small'}

    def __init__(self, md=None, bib=None, op={}):
        """ Convert a markdown document with citation code into another one
        with formatted citations and references.

        Arguments:

           md:

              If defined, it might be the name of the markdown file or a list
              with the lines of the markdown file. If not defined, the class
              will read the standard input which should be either the markdown
              file or the markdown converted into json by pandoc.

           bib:

             If defined, should the name of the .bib file. If not defined, the
             class will try to find it in the markdown's YAML header.

           op:

             A dictionary with options. If not defined, the default ones will
             be used.
        """
        if md is not None:
            self._m = md

        if bib is not None:
            self._b = bib

        for k in op:
            self._o[k] = op[k]

        # Command line arguments overwrite __init__ arguments
        for a in sys.argv:
            self._parse_arg(a)

        if self._m is None:
            self._get_md_from_stdin()

        if bib is None:
            self._get_bib_from_md()

        self._GetKeys()              # Get list of cited keys
        self._GetBibData()           # Get data from bib file, but keep only cited entries
        self._FormatAuthorTitle()    # Required to add letters to years
        self._AddLettersToYears()    # Required to format 'cite' and 'citep'
        self._FinishFormattingRefs() # Now it's possible to finish formatting the refs,
        self._FormatCits()           # and the citations
        self._AddFormattedRefs()     # Finally, add the formatted refs to the markdown document

    def _parse_arg(self, a):
        if a.lower() == 'sem-links':
            self._o['anchor'] = False
        elif a.lower() == 'negrito':
            self._o['em'] = '**'
        elif a.lower() == 'discreto':
            self._o['discreet'] = True
        elif a.lower() == 'completo':
            self._o['compl'] = True
        elif a.lower() == 'url-completa':
            self._o['oldurl'] = True
        elif a.lower() == 'repetido':
            self._o['repeat'] = True
        elif a.lower() == 'obediente':
            self._o['obey'] = True
        elif a.lower() in ['subtítulo', 'subtitulo']:
            self._o['subttl'] = True
        elif re.search('\.bib$', a):
            self._b = a
        elif a.lower() == 'normalsize':
            self._o['font-size'] = 'normalsize'
        elif a.lower() == 'footnotesize':
            self._o['font-size'] = 'footnotesize'
        elif a.lower() == 'singlespacing':
            self._o['spacing'] = 'singlespacing'
        elif a.lower() == 'onehalfspacing':
            self._o['spacing'] = 'onehalfspacing'
        elif a.lower() == 'doublespacing':
            self._o['spacing'] = 'doublespacing'
        elif a.lower() in ['?', 'h', 'help', '-h', '--help', 'a', 'ajuda', '-a', '--ajuda']:
            # The help and names of arguments are in Portuguese because only
            # Brazilians follow ABNT rules.
            print('Uso: ' + sys.argv[0] + ' argumentos_opcionais\n'
                  '\n'
                  'Argumentos válidos (em qualquer ordem):\n'
                  '\n'
                  '  ajuda       : mostra este texto de ajuda.\n'
                  '\n'
                  '  sem-links   : não criar link do ano citado para a referência.\n'
                  '\n'
                  '  latex       : usar código LaTeX para produzir links.\n'
                  '\n'
                  '  negrito     : usar **negrito** para enfatizar títulos.\n'
                  '\n'
                  '  discreto    : omitir texto de alerta para citações ausentes.\n'
                  '\n'
                  '  subtítulo   : realçar a parte do título após :?!\n'
                  '\n'
                  '  completo    : mostrar primeiro nome completo.\n'
                  '\n'
                  '  repetido    : não substituir nomes repetidos por sublinhados.\n'
                  '\n'
                  '  obediente   : contrariar regras da língua portuguesa e obedecer a\n'
                  '                ABNT, usando ponto-e-vírgula para separar coautores\n'
                  '                em citações..\n'
                  '\n'
                  '  nome_de_arquivo_com_extensão.bib :\n'
                  '      se não for indicado o nome do arquivo .bib, o arquivo.md deverá\n'
                  '      ter um cabeçalho YAML com o campo bibliography definido.\n'
                  '\n'
                  '  nome_de_arquivo_com_extensão.md :\n'
                  '      se não for indicado o nome do arquivo .md, o conteúdo\n'
                  '      markdown deve ser passado como input padrão (stdin).\n'
                  '\n'
                  'Exemplos:\n'
                  '\n'
                  '   ' + sys.argv[0] + ' arquivo.md arquivo.bib > novo.md\n'
                  '   ' + sys.argv[0] + ' arquivo.bib sem-links negrito arquivo.md > novo.md\n'
                  '   cat arquivo.md | ' + sys.argv[0] + ' arquivo.bib | pandoc -o arquivo.html\n'
                  '   cat arquivo.md | ' + sys.argv[0] + ' latex | pandoc -o arquivo.pdf\n'
                  '   pandoc arquivo.md -o arquivo.pdf --filter ' + sys.argv[0] + '\n'
                  '', file=sys.stderr)
            if not self._j:
                quit()

        if self._j:
            return

        # Options that should not be set in the YAML header:
        if re.search('\.md$', a):
            f = open(a, 'r')
            self._m = f.readlines()
            f.close()
        elif a.lower() == 'latex':
            self._o['type'] = 'latex'


    def _get_md_from_stdin(self):
        t = sys.stdin.read()
        if t[0] == '{':
            self._j = True
            j = json.load(io.StringIO(t))
            self._d = j['meta']
            if 'bibliography' in self._d:
                self._b = self._d['bibliography']['c'][0]['c']
            if 'abntref' in self._d:
                opt = self._d['abntref']['c']
                for i in range(len(opt)):
                    if opt[i]['t'] == 'Str':
                        self._parse_arg(opt[i]['c'])
            p = subprocess.run(['pandoc', '-t', 'markdown', '-f', 'json'],
                               stdout=subprocess.PIPE,
                               input=json.dumps(j).encode('utf-8'))
            t = p.stdout.decode()
        t = t.split('\n')
        self._m = t

    def _get_bib_from_md(self):
        for l in self._m:
            if re.search('^\s*bibliography\s*:', l):
                if re.search('^\s*bibliography\s*:\s*".*"', l):
                    self._b = re.sub('^\s*bibliography\s*:\s*"(.*)"\s*', '\\1', l)
                elif re.search("^\s*bibliography\s*:\s*'.*'", l):
                    self._b = re.sub("^\s*bibliography\s*:\s*'(.*)'\s*", '\\1', l)
                else:
                    self._b = re.sub("^\s*bibliography\s*:\s*(.*)\s*$", '\\1', l)

        if self._b is None:
            print('Arquivo bib indefinido. Para obter ajuda, digite o comando:', file=sys.stderr)
            print('', file=sys.stderr)
            print('    ' + sys.argv[0] + ' ajuda', file=sys.stderr)
            quit()

    def _GetKeys(self):
        md = ' '.join(self._m)
        keys = re.findall(r'[\W^\\]@([a-zA-Z0-9à-öø-ÿÀ-ÖØ-ß_:#-]+)', md)
        self._k = set(keys)

    def _GetBibData(self):
        try:
            bib = parse_file(self._b)
        except Exception as ERR:
            print('Erro lendo ' + self._b + ':', file=sys.stderr)
            print(ERR, file=sys.stderr)
            quit()

        for k in self._k:
            e = {}
            e['bibkey'] = k
            if not k in bib.entries:
                e['etype'] = 'unknown'
                e['author'] = k
                e['sortkey'] = '00' + k
                if self._o['discreet']:
                    e['cite'] = k
                    e['citep'] = k
                else:
                    e['cite'] = k + ':REFERÊNCIA NÃO ENCONTRADA'
                    e['citep'] = k + ':REFERÊNCIA NÃO ENCONTRADA'
                e['ref'] = k + ': CHAVE AUSENTE DO ARQUIVO “' + self._b + '”'
                e['year'] = '????'
                self._e[k] = e
                print('Chave ausente do arquivo “' + self._b + '”: ' + k, file=sys.stderr)
                continue
            b = bib.entries[k]
            if not 'title' in b.fields:
                e['etype'] = 'unknown'
                e['author'] = k
                e['sortkey'] = '01' + k
                if self._o['discreet']:
                    e['cite'] = k
                    e['citep'] = k
                else:
                    e['cite'] = 'REFERÊNCIA SEM TÍTULO: ' + k
                    e['citep'] = 'REFERÊNCIA SEM TÍTULO: ' + k
                e['ref'] = k + ': REFERÊNCIA SEM TÍTULO'
                e['year'] = '????'
                self._e[k] = e
                print('Referência sem título: ' + k, file=sys.stderr)
                continue

            for f in b.fields:
                e[f] = b.fields[f]

            # Conflate all types of entry in 6 types: book, inbook, article,
            # incollection, thesis, and misc.
            e['etype'] = 'misc'
            if b.type in ['thesis', 'phdthesis', 'masterthesis', 'monography']:
                e['etype'] = 'thesis'
                if 'type' not in b.fields:
                    if b.type == 'phdthesis':
                        e['type'] = 'Tese de Doutorado'
                    elif b.type == 'masterthesis':
                        e['type'] = 'Dissertação de Mestrado'
                    elif b.type == 'monography':
                        e['type'] = 'Monografia'
            elif b.type in ['incollection', 'inproceedings']:
                e['etype'] = 'incollection'
            elif b.type in ['inbook', 'bookinbook', 'suppbook']:
                e['etype'] = 'inbook'
            elif b.type == 'article':
                e['etype'] = 'article'
            elif b.type in ['book', 'mvbook', 'booklet', 'proceedings', 'collection', 'mvcollection', 'suppcollection']:
                e['etype'] = 'book'

            if not 'year' in b.fields:
                e['year'] = 's.d.'
            aa = self._get_authors(b.persons, 'author')
            if aa[0]:
                if 'shortauthor' in e:
                    e['cite_author'] = e['shortauthor']
                    p = b.persons['author'][0]
                    p = ' '.join([' '.join(p.first()), ' '.join(p.middle()), ' '.join(p.prelast()), ' '.join(p.last()), ' '.join(p.lineage())])
                    p = p.strip()
                    e['author'] = e['shortauthor'] + ' — ' + p
                else:
                    e['author'] = aa[0]
                    e['cite_author'] = aa[1]
            else:
                e['author'] = ''
            eds = self._get_authors(b.persons, 'editor')
            if eds[0]:
                e['editor'] = eds[0]
                e['cite_editor'] = eds[1]

            # Fix wrong type of entry
            if e['etype'] == 'inbook' and 'author' in e and 'editor' in e and e['author'] != e['editor']:
                e['etype'] == 'incollection'

            if e['etype'] == 'inbook':
                if e['author'] == '' and 'editor' in e:
                    e['author'] = e['editor']
                if 'editor' not in e or ('editor' in e and e['author'] == e['editor']):
                    if not self._o['repeat']:
                        e['editor'] = '\\_\\_\\_\\_\\_'
            if e['etype'] == 'incollection' and 'editor' in e and 'editortype' not in e:
                e['editortype'] = 'Org.'
            if e['etype'] in ['book', 'inbook', 'incollection'] and 'address' not in e:
                e['address'] = '[S.l.]'
            if e['etype'] in ['book', 'inbook', 'incollection'] and 'publisher' not in e:
                e['publisher'] = '[s.n.]'
            if 'urlaccessdate' in e and 'urldate' not in e:
                e['urldate'] = e['urlaccessdate']
            if 'subtitle' in e:
                e['title'] += ': ' + e['subtitle']
            if 'booksubtitle' in e:
                e['booktitle'] += ': ' + e['booksubtitle']
            self._e[k] = e.copy()


    def _FormatAuthorTitle(self):
        for k in self._e:
            self._e[k] = self._begin_formatting(self._e[k])

    def _AddLettersToYears(self):
        # Sort the keys and add letters to repeated years:
        s = {}
        for k in self._e:
            s[k] = self._e[k]['sortkey']
        self._k = [k for k in sorted(s, key=s.get)]

        lastciteyear = ''
        lastcite = ''
        lastkey = ''
        n = 0
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                   'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'x', 'w', 'y', 'z']

        for k in self._k:
            curciteyear = self._e[k]['sortkey']
            curcite = self._e[k]['cite']
            curkey = k
            if curciteyear == lastciteyear:
                n += 1
                if n == 1:
                    self._e[lastkey]['year'] += letters[n-1]
                self._e[curkey]['year'] += letters[n]
            else:
                n = 0
            if curcite == lastcite and not self._o['repeat']:
                self._e[k]['ref'] = '\\_\\_\\_\\_\\_. ' + self._e[k]['ref'].partition('. ')[2]
            lastkey = curkey
            lastcite = curcite
            lastciteyear = curciteyear


    def _FinishFormattingRefs(self):
        for k in self._e:
            if self._e[k]['etype'] != 'unknown':
                self._e[k]['ref'] = self._finish_formatting(self._e[k])

    def _FormatCits(self):
        m = '\x05'.join(self._m) + '\n'
        m = re.sub('(\[[^]]*\])', self._sub_in_paren, m)
        for k in self._e:
            if self._o['anchor']:
                cleankey = re.sub('[#_:-]', '', self._e[k]['bibkey'])
                m = re.sub('-@' + self._e[k]['bibkey'] + r'\b', '([' + self._e[k]['year'] + '](#ref-' + cleankey + '))', m)
                m = re.sub('@' + self._e[k]['bibkey'] + r'\b', self._e[k]['cite'] + ' ([' + self._e[k]['year'] + '](#ref-' + cleankey + '))', m)
            else:
                m = re.sub('-@' + self._e[k]['bibkey'] + r'\b', '(' + self._e[k]['year'] + ')', m)
                m = re.sub('@' + self._e[k]['bibkey'] + r'\b', self._e[k]['cite'] + ' (' + self._e[k]['year'] + ')', m)
        m = m.split('\x05')
        self._m = m.copy()


    def _AddFormattedRefs(self):
        if self._o['type'] == 'latex':
            if self._o['spacing'] == '':
                self._m.append('\\setlength{\\parskip}{6pt} \\setlength{\\parindent}{0pt} ' +
                               ' \\' + self._o['font-size'] + '\n')
            else:
                self._m.append('\\setlength{\\parskip}{6pt} \\setlength{\\parindent}{0pt} ' +
                               '\\' + self._o['spacing'] + ' \\' + self._o['font-size'] + '\n')
        self._m.append('\n')
        for k in self._k:
            self._m.append(self._e[k]['ref'])

    def _formated_elements(self, nn, e):
        edict = {'editor'    : [' ', ''],
                 'editortype': [' (', ')'],
                 'booktitle' : ['. ' + self._o['em'], self._o['em'] + '.'],
                 'edition'   : ['. ', '. ed.'],
                 'address'   : ['. ', ''],
                 'section'   : [' — ', ''],
                 'publisher' : [': ', ''],
                 'volume'    : [', v. ', ''],
                 'series'    : [' (', ')'],
                 'pages'     : [', p. ', ''],
                 'chapter'   : [', cap. ', ''],
                 'journal'   : [' ' + self._o['em'], self._o['em']],
                 'number'    : [', n. ', ''],
                 'month'     : [', ', ''],
                 'type'      : ['. ', ''],
                 'school'    : [' — ', ''],
                 'issn'      : ['. ISSN ', '.'],
                 'isbn'      : ['. ISBN ', '.'],
                 'institution': ['. ', ''],
                 'howpublished': ['. ', ''],
                 'urldate': [' Acesso em ', '.'],
                 'note': [' ', '.']
                }
        r = ''
        for n in nn:
            if n in e:
                r += edict[n][0] + e[n] + edict[n][1]
        return r

    def _begin_formatting(self, e):

        def first_upper(m):
            return m.group(1).upper() + ' ' + m.group(2)

        if e['etype'] == 'unknown':
            if self._o['anchor']:
                cleankey = re.sub('[#_:-]', '', e['bibkey'])
                if self._o['type'] == 'latex':
                    e['ref'] = '\\hypertarget{ref-' + cleankey + '}{}' + e['ref'] + '\n\n'
                else:
                    e['ref'] = '<a id="ref-' + cleankey + '"></a>' + e['ref'] + '\n\n'
            else:
                e['ref'] += '\n\n'
            return e

        # Add both 'author' and 'cite' to 'ref'
        ttl = False
        if e['author']:
            ref = e['author']
            e['cite'] = e['cite_author']
        elif e['etype'] == 'inbook' and e['editor']:
            ref = e['editor'] + self._formated_elements(['editortype'], e)
            e['cite'] = e['cite_editor']
        elif 'organization' in e:
            if 'org-short' in e:
                e['cite'] = e['org-short']
                e['author'] = ref = e['org-short'].upper() + ' — ' + e['organization']
            else:
                e['author'] = e['cite'] = e['organization']
                ref = e['organization'].upper()
            del e['organization']
        else:
            e['title'] = re.sub('([^ ]*) (.*)', first_upper, e['title'])
            e['cite'] = re.sub('([^ ]*) .*', '\\1', e['title'].title())
            ref = e['title'] + '.'
            ttl = True

        e['citep'] = re.sub('ET AL\*\.', 'et al*.', e['cite'].upper())
        if self._o['obey']:
            e['citep'] = re.sub(' E ', '; ', e['citep'])
            e['citep'] = re.sub(', ', '; ', e['citep'])
        else:
            e['citep'] = re.sub(' E ', ' e ', e['citep'])
        e['sortkey'] = e['cite'] + ':' + e['year']

        if not ttl:
            if e['etype'] in ['article', 'inbook', 'incollection']:
                ref += '. ' + e['title'] + '.'
            else:
                if not self._o['subttl'] and re.search('[?!:] ', e['title']):
                    ref += '. ' + self._o['em'] + re.sub('(.*)([?!:]) (.*)', '\\1\\2' + self._o['em'] + ' \\3', e['title']) +'.'
                else:
                    ref += '. ' + self._o['em'] + e['title'] + self._o['em'] + '.'
        e['ref'] = ref
        return e

    def _finish_formatting(self, e):

        def format_month(m):
            mon = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'Jun.', 'Jul.', 'Aug.', 'Sep.', 'Oct.', 'Nov.', 'Dec.']
            mes = ['jan.', 'fev.', 'mar.', 'abr.', 'maio', 'jun.', 'jul.', 'ago.', 'set.', 'out.', 'nov.', 'dez.']
            for i in range(1, 13):
                m = m.replace(mon[i-1], mes[i-1])
                if str(i) == m:
                    m = mes[i-1]
            return m

        # If either 'editor' or 'publisher' is empty, use 'organization' instead.
        if e['etype'] == 'incollection' and 'editor' not in e and 'organization' in e:
            e['editor'] = e['organization']
            del e['organization']
        if 'publisher' not in e and 'organization' in e:
            e['publisher'] = e['organization']
            del e['organization']

        # Format items after author and title according to type of entry:
        ref = e['ref']
        if e['etype'] == 'article':
            ref += self._formated_elements(['journal', 'section', 'address', 'volume', 'number', 'pages'], e)
        elif e['etype'] in ['inbook', 'incollection']:
            ref += ' In: '
            ref += self._formated_elements(['editor', 'editortype', 'booktitle', 'edition', 'address', 'publisher'], e)
        elif e['etype'] == 'thesis':
            if 'month' in e:
                ref += ', ' + format_month(e['month']) + ' ' + e['year'] + '.'
            else:
                ref += ', ' + e['year']
            if 'pages' in e:
                ref += '. ' + e['pages'] + ' f.'
            ref += self._formated_elements(['type', 'school', 'publisher'], e)
            if 'address' in e:
                ref += ', ' + e['address']
            ref += '.'
        else:
            ref += self._formated_elements(['edition', 'address', 'publisher'], e)

        ref += self._formated_elements(['howpublished'], e)

        # Format final items that common to almost all types
        if e['etype'] != 'thesis':
            if 'month' in e:
                ref += ', ' + format_month(e['month']) + ' ' + e['year'] + '.'
            else:
                ref += ', ' + e['year'] + '.'

        # Format more items
        if e['etype'] in ['inbook', 'incollection']:
            ref += self._formated_elements(['volume', 'chapter', 'pages'], e)
        elif e['etype'] not in ['article', 'thesis']:
            if 'pages' in e:
                ref += ', ' + e['pages'] + ' p.'
            ref += self._formated_elements(['volume'], e)

        if e['etype'] not in ['article', 'thesis']:
            ref += self._formated_elements(['series'], e)

        # Format the remaining items
        ref += self._formated_elements(['issn', 'isbn'], e)
        if 'url' in e:
            if self._o['oldurl']:
                ref += ' Disponível em \\<<' + e['url'] + '>\\>.'
            else:
                surl = re.sub('http[s]*://', '', e['url'])
                surl = re.sub('/.*', '', surl)
                surl = re.sub('\xad$', '', re.sub('(.)', '\\1\xad', surl)) # soft hyphen
                ref += ' Disponível em [' + surl + '](' + e['url'] + ').'
        ref += self._formated_elements(['urldate', 'note'], e) + '.'

        # Fix punctuation errors that were not avoided
        ref = re.sub('([\.?!:,])\. ', '\\1 ', ref)
        ref = re.sub('([\.?!:,])\.$', '\\1', ref)
        ref = re.sub('\.,', '.', ref)

        # Add either anchors (html) or hypertargets (latex)
        if self._o['anchor']:
            cleankey = re.sub('[#_:-]', '', e['bibkey'])
            if self._o['type'] == 'latex':
                ref = '\\hypertarget{ref-' + cleankey + '}{}' + ref + '\n\n'
            else:
                ref = '<a id="ref-' + cleankey + '"></a>' + ref + '\n\n'
        else:
            ref += '\n\n'
        return ref


    def _get_authors(self, prsns, tp):
        if tp not in prsns:
            return [False, False]

        persons = prsns[tp]
        cit = ''
        ref = ''
        isetal = False
        if len(persons) > 3:
            isetal = True

        for p in persons:
            lname = ' '.join(p.last())
            fnames = p.first() + p.middle()
            if lname == 'others':
                cit += ' *et al*.'
                ref += ' *et al*.'
                break
            if not self._o['compl']:
                fini = []
                for i in range(len(fnames)):
                    if fnames[i][0] == (fnames[i][0]).upper():
                        fini.append((fnames[i][0]).upper())
                fnames = '. '.join(fini) + '.'
            else:
                fnames = ' '.join(fnames)
            cit += ', ' + lname.title()
            ref += '; ' + lname.upper() + ', ' + fnames
            if isetal:
                cit += ' *et al*.'
                ref += ' *et al*.'
                break

        ref = re.sub('^; ', '', ref)
        cit = re.sub('^, ', '', cit)
        cit = re.sub('(.*), (.*)', '\\1 e \\2', cit)

        return [ref, cit]


    def _sub_in_paren(self, m):
        g = m.group(1)
        if re.search(r'[^\\]@[a-zA-Z0-9-]', g):
            g = g.replace('[', '(')
            g = g.replace(']', ')')
            for k in self._e:
                if self._o['anchor']:
                    cleankey = re.sub('[#_:-]', '', self._e[k]['bibkey'])
                    g = re.sub('-@' + self._e[k]['bibkey'] + r'\b',
                               '[' + self._e[k]['year'] + '](#ref-' + cleankey + ')', g)
                    g = re.sub('@' + self._e[k]['bibkey'] + r'\b',
                               self._e[k]['citep'] + ', [' + self._e[k]['year'] + '](#ref-' + cleankey + ')', g)
                else:
                    g = re.sub('-@' + self._e[k]['bibkey'] + r'\b', self._e[k]['year'], g)
                    g = re.sub('@' + self._e[k]['bibkey'] + r'\b', self._e[k]['citep'] + ', ' + self._e[k]['year'], g)
        return g

    def Print(self):
        """ Print the list of lines of the transformed markdown documment. """
        if self._j:
            t = '\n'.join(self._m)
            p = subprocess.run(['pandoc', '-f', 'markdown', '-t', 'json'],
                               stdout=subprocess.PIPE,
                               input=t.encode('utf-8'))
            t = p.stdout.decode()
            j = json.load(io.StringIO(t))
            j['meta'] = self._d
            sys.stdout.write(json.dumps(j))
        else:
            print(''.join(self._m) + '\n')

    def GetMD(self):
        """ Return the list of lines of the transformed markdown documment. """
        return self._m
