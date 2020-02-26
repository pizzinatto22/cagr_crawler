import requests
from lxml import html
from lxml import etree as ET



url1 = "http://cagr.sistemas.ufsc.br/modules/comunidade/cadastroTurmas/index.xhtml"
headers = {
    "Connection" : "keep-alive",
    "Origin" : "http://cagr.sistemas.ufsc.br",
    "Content-Type": "application/x-www-form-urlencoded"
}
data = "AJAXREQUEST=_viewRoot&formBusca%3AselectSemestre={0}&formBusca%3AselectDepartamento=&formBusca%3AselectCampus=1&formBusca%3AselectCursosGraduacao={1}&formBusca%3AcodigoDisciplina=&formBusca%3Aj_id98_selection=&formBusca%3AfilterDisciplina=&formBusca%3Aj_id102=&formBusca%3Aj_id106_selection=&formBusca%3AfilterProfessor=&formBusca%3AselectDiaSemana=0&formBusca%3AselectHorarioSemana=&formBusca=formBusca&autoScroll=&javax.faces.ViewState=j_id1&formBusca%3Aj_id119=formBusca%3Aj_id119&isoladas=&formBusca%3AdataScroller1={2}"


semestre = "20201"
cursos = [
    {
        "nome": "Administração Diurno",
        "origem": 301,
        "destino": 1
    },
    {
        "nome": "Administração noturno",
        "origem": 316,
        "destino": 1
    },

    {
        "nome": "Contábeis Diurno",
        "origem": 302,
        "destino": 2
    },
    {
        "nome": "Contábeis Noturno",
        "origem": 317,
        "destino": 2
    },

    {
        "nome": "Economia Diurno",
        "origem": 304,
        "destino": 3
    },

    {
        "nome": "Economia Noturno",
        "origem": 318,
        "destino": 3
    },

    {
        "nome": "Relações Internacionais",
        "origem": 340,
        "destino": 4
    },

    {
        "nome": "Serviço Social Diurno",
        "origem": 309,
        "destino": 5
    },
    {
        "nome": "Serviço Social Noturno",
        "origem": 339,
        "destino": 5
    },
]

s = requests.Session()
s.headers.update(headers)

page = s.get(url1) #pegar o cookie

turmas = []

print("** INICIANDO **")

for c in cursos:
    paginasTotal = 1
    paginasAtual = 1

    while paginasAtual <= paginasTotal:
        print("Analisando pagina {0} do curso {1}".format(paginasAtual, c["nome"]))

        page = s.post(url1, data = data.format(semestre, c["origem"], str(paginasAtual)))
        tree = html.fromstring(page.content)
        paginasTotal = len(tree.xpath("//table[@id='formBusca:dataScroller1_table']/tbody/tr/td[@class='rich-datascr-inact']")) + 1

        disciplinas = tree.xpath("//tbody[@id='formBusca:dataTable:tb']/tr")

        for d in disciplinas:
            turmas.append({
                "course_id" : c["destino"],
                "codigo" : d[3].text,
                "turma" : d[4].text,
                "descricao": d[5].text,
                "horario": d[12].xpath("./descendant-or-self::*/text()"),
                "professor":  d[13].xpath("./descendant-or-self::*/text()")
            })
        paginasAtual += 1

print("Gerando o arquivo CSV")

file = open("turmas.csv", "w")
file.truncate()

file.write("course_id;codigo;turma;descricao;horario;professor\n")

for t in turmas:
    file.write(
        '"' + str(t["course_id"]) + '";' +
        '"' + str(t["codigo"]) + '";' +
        '"' + str(t["turma"]) + '";' +
        '"' + str(t["descricao"]) + '";' +
        '"' + "\n".join(t["horario"]) + '";' +
        '"' + "\n".join(t["professor"]) + '"' +
        "\n"
     )
file.close()

print("** FIM **")


# #colunas = "curso;horas;link"

# file.write(colunas + "\n")

# #page = requests.get(url1)
# tree = html.fromstring(page.content)

# courses = tree.xpath("//a[@class='cursoCard']")
# for c in courses:
#     url  = c.get("href")
#     name = c.xpath(".//div[@class='cursoCard-nome']/text()")
#     hour = c.xpath(".//div[@class='cursoCard-infos-tempoEstimado']/p[1]/text()")

#     print(name, hour, url);
#     file.write(name[0] + ";" + hour[0] + ";alura.com.br" + url + "\n")

# file.close()
