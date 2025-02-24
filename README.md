# SophIA - Assistente Virtual para Professores

SophIA é um assistente virtual baseado em Inteligência Artificial projetado para apoiar professores na análise de desempenho estudantil. A ferramenta permite consultas interativas sobre notas, frequência e métricas pedagógicas, gerando insights visuais e relatórios para facilitar a personalização do ensino.

## Objetivo
Facilitar a análise do desempenho dos alunos, fornecendo informações rápidas e visuais que ajudem professores e gestores a tomar decisões educacionais mais embasadas.

## Principais Funcionalidades
- **Consulta Interativa**: Permite que professores perguntem sobre médias, notas e tendências de desempenho.
- **Geração de Gráficos**: Visualização intuitiva de informações acadêmicas.
- **Relatórios Automatizados**: Sumários de desempenho por aluno, turma ou período letivo.
- **Análise de Frequência**: Monitoramento da presença dos alunos.

<div id="carousel-container" style="width: 100%; max-width: 600px; margin: auto; overflow: hidden; position: relative;">
  <div id="carousel" style="display: flex; transition: transform 0.5s ease-in-out;">
  <img src="00.jpg" alt="Image 0" style="width: 100%; display: block; min-width: 100%;">
    <img src="001.jpg" alt="Image 1" style="width: 100%; display: block; min-width: 100%;">
    <img src="002.jpg" alt="Image 2" style="width: 100%; display: block; min-width: 100%;">
    <img src="003.jpg" alt="Image 3" style="width: 100%; display: block; min-width: 100%;">
    <img src="004.jpg" alt="Image 4" style="width: 100%; display: block; min-width: 100%;">
    <img src="005.jpg" alt="Image 5 " style="width: 100%; display: block; min-width: 100%;">
  </div>
  <a href="#" onclick="plusSlides(-1)" style="position: absolute; top: 50%; left: 10px; transform: translateY(-50%); font-size: 24px;">&#10094;</a>
  <a href="#" onclick="plusSlides(1)" style="position: absolute; top: 50%; right: 10px; transform: translateY(-50%); font-size: 24px;">&#10095;</a>
</div>

<script>
let slideIndex = 0;
const slides = document.getElementById("carousel").getElementsByTagName("img");
const totalSlides = slides.length;

function showSlides(index) {
  slideIndex = (index + totalSlides) % totalSlides;
  const translateX = -slideIndex * 100;
  document.getElementById("carousel").style.transform = `translateX(${translateX}%)`;
}

function plusSlides(n) {
  showSlides(slideIndex + n);
}

// Automatically change slides every 2 seconds
setInterval(() => {
  plusSlides(1);
}, 2000);

// Initialize the carousel
showSlides(slideIndex);
</script>

## Tecnologias Utilizadas
- **Python** - Linguagem principal do projeto
- **LangChain** - Orquestração das interações com LLMs
- **Hugging Face** - Modelos de linguagem para processamento de perguntas
- **Streamlit** - Interface web interativa
- **Plotly** - Geração de gráficos interativos
- **sqlite/Mysql** - Armazenamento estruturado dos dados acadêmicos


# Desenvolvedores
- **[Alisson Pereira]**  - - https://www.linkedin.com/in/alisson-pereira-ds/
```
Data Scientist | Python - SQL - LLM - Gen AI | Machine Learning
E-mail : alissonpereira.contato@gmail.com
```
- **[Tiago Fernando]** - https://www.linkedin.com/in/alisson-pereira-ds/
```
Data Scientist | Python - SQL - LLM - Gen AI | Machine Learning
E-mail : alissonpereira.contato@gmail.com
```

# Status do Projeto

Atualmente, SophIA está em fase de desenvolvimento e aprimoramento, com testes em andamento para validação pedagógica e ajustes na interação com os usuários.

# Contribuição

Se você deseja contribuir com o projeto, sinta-se à vontade para entrar em contato conosco.



