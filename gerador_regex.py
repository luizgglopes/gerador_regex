import re

def confere_regex(regex, texto):
  """
  
  Função que confere se uma regex é aplicável a uma texto.

  :param regex: A regex a ser testada.
  :param texto: O texto para avaliação da regex.
  :return bool

  """
  try:
    match = re.fullmatch(regex, texto)
    return bool(match)
  except:
    return False


def confere_regex_lista(regex, lista):
  """
  
  Função que confere se uma regex é aplicável a todos os itens de uma lista.

  :param regex: A regex a ser testada.
  :param lista: Lista de valores do tipo String.
  :return bool

  """
  match = [bool(re.fullmatch(regex, texto)) for texto in lista
           if len(str(texto) or '') > 0]
  return min(match)


def gera_regex_caractere(caractere, reverso=False):
  """
  
  Função que gera regex aplicável a um caractere.

  :param caractere: O caractere para aplicacao da regex.
  :param reverso: Se True, a regex mais abrangente é aceita.
  :return str: A regex sugerida para o caractere.

  """
  dict_regex = {
      'digito': r'\d',
      'letra': r'\w',
      'espaco': r'\s'
  }
  if reverso:
      dict_regex = {
          'letra': r'\w',
          'digito': r'\d',
          'espaco': r'\s'
      }
  for r in dict_regex.keys():
    if confere_regex(dict_regex[r], caractere):
      return dict_regex[r]
  return r"\{0}".format(caractere)


def gera_regex_texto(texto, reverso=False):
  """
  
  Função que gera regex aplicável a um texto.

  :param texto: O texto para aplicacao da regex.
  :param reverso: Se True, a regex mais abrangente é aceita.
  :return str: A regex sugerida ao texto.

  """
resultado = ['^']
tipo_anterior = None
quantidade = 1
pos = 0
for c in texto:
  tipo = gera_regex_caractere(c, reverso)
  if (tipo == tipo_anterior):
    quantidade += 1
  else:
    if (quantidade > 1):
        resultado += ["{{{quantidade}}}".format(quantidade=quantidade)]
    quantidade = 1
  if (quantidade == 1):
    resultado += [tipo]
  if (pos < len(str(texto))-1):
    tipo_anterior = tipo
    pos += 1
  else:
    if (quantidade > 1):
      resultado += ["{{{quantidade}}}".format(quantidade=quantidade)]
resultado += ['$']
  try:
    regex = ''.join(resultado)
    if (confere_regex(regex, texto) == False):
      regex = ''
    return regex
  except:
    return ''


def gera_regex_lista(lista, limite_distintas=3, aceita_reverso=True):
  """
  
  Função que busca gerar regex aplicável a uma lista de textos.

  :param lista: Lista de valores do tipo String.
  :param aceita_reverso: indica se deve ser executada gera_regex_texto com ordem de precedência de tipos revertida.
  :param limite_distintas: Número máximo de regex distintas aceitas na lista retorno.
  :param texto: O texto para aplicacao da regex.
  :return List[str]: A(s) regex aplicáveis à lista.

  """
  resultado = r'^.*$'
  try:
    regex_lista = [gera_regex_texto(texto)[1:-1].split('\\') for texto in lista
                    if len(str(texto) or '') > 0]
    lista_regex_distintas = list(set([gera_regex_texto(texto) for texto in lista
                                      if len(str(texto) or '') > 0]))
    tam_regex_lista = set([len(i) for i in regex_lista])
    tam_regex_fixo = bool(len(tam_regex_lista) == 1)
    
    if (tam_regex_fixo == False and aceita_reverso):
      regex_lista = [gera_regex_texto(texto, True)[1:-1].split('\\') for texto in lista
                      if len(str(texto) or '') > 0]
      tam_regex_lista = set([len(i) for i in regex_lista])
      tam_regex_fixo = bool(len(tam_regex_lista) == 1)

    resultado_aux = []
    if (tam_regex_fixo):
      for i in range(0, max(tam_regex_lista)):
        tipo_caractere_lista = set(
            [re.sub(r'\{\d*\}', '', j[i]) for j in regex_lista])
        tipo_caractere_fixo = bool(len(tipo_caractere_lista) == 1)
        if (tipo_caractere_fixo):
          qt_caractere_lista = set([j[i] for j in regex_lista])
          qt_caractere_fixo = bool(len(qt_caractere_lista) == 1)
          if (qt_caractere_fixo):
            resultado_aux += [max(qt_caractere_lista)]
          else:
            resultado_aux += [max(tipo_caractere_lista) + '*']
      regex_final = r"{0}".format('^' + '\\'.join(resultado_aux) + '$')
      if (confere_regex_lista(regex_final, lista) == True):
        resultado = regex_final
        print("Regex da lista validada com sucesso.")
      else:
        print("Não foi encontrada regex única válida para a lista.")
        qt_regex_distintas = len(lista_regex_distintas)
        if (qt_regex_distintas <= limite_distintas):
          print("Retornada lista de regex distintas encontradas.")
          return lista_regex_distintas
        else:
          print("Foram encontradas {0} regex distintas.".format(
              qt_regex_distintas))
          print(
              "Por estar acima do limite estipulado, será assumida regex padrão.")
    else:
      print("Não foi encontrada regex única válida para a lista.")
      qt_regex_distintas = len(lista_regex_distintas)
      if (qt_regex_distintas <= limite_distintas):
        print("Retornada lista de regex distintas encontradas.")
        return lista_regex_distintas
      else:
        print("Foram encontradas {0} regex distintas.".format(
            qt_regex_distintas))
        print(
            "Por estar acima do limite estipulado, será assumida regex padrão.")
    return [resultado]
  except:
    print("Erro ao analisar regex na lista. Assumida regex padrão.")
    return [resultado]


