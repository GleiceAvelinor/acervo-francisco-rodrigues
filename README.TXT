🏛️ Acervo Francisco Rodrigues - Gestão de Biblioteca Digital
Este é um sistema de gerenciamento de acervo pessoal desenvolvido em Python utilizando o framework Streamlit. O objetivo do projeto é permitir o cadastro, a consulta e a exportação de inventários de livros de forma rápida, moderna e eficiente.

✨ Funcionalidades
📥 Cadastro de Livros: Interface simples para inserir título, autor, ISBN, editora, categoria e upload de foto da capa.

🔍 Busca Inteligente: Filtro em tempo real por qualquer termo (Título, Autor ou Categoria).

📑 Paginação de Alta Performance: Otimizado para suportar milhares de registros sem perda de velocidade.

📄 Exportação em PDF: Geração automática de inventário alinhado com fotos e dados técnicos.

💾 Banco de Dados Local: Utiliza SQLite para armazenamento seguro e sem necessidade de servidores externos.

📱 Design Responsivo: Interface que se adapta perfeitamente a computadores e dispositivos móveis.

🛠️ Tecnologias Utilizadas
Linguagem: Python 3.x

Interface: Streamlit

Banco de Dados: SQLite

Manipulação de Dados: Pandas

Geração de PDF: ReportLab

Processamento de Imagem: Pillow (PIL)

🚀 Como Executar o Projeto
1. Clonar ou baixar o projeto
Certifique-se de ter os arquivos livraria.py em sua pasta.

2. Criar um Ambiente Virtual (Recomendado)
No terminal, execute:

Bash
python -m venv venv
Ative o ambiente:

Windows: .\venv\Scripts\activate

Linux/Mac: source venv/bin/activate

3. Instalar as Dependências
Instale as bibliotecas necessárias com o comando:

Bash
pip install streamlit pandas pillow reportlab
4. Rodar a Aplicação
Execute o comando abaixo e o sistema abrirá automaticamente no seu navegador:

Bash
streamlit run livraria.py
📂 Estrutura de Arquivos
livraria.py: Código principal da aplicação.

biblioteca_web.db: Arquivo do banco de dados (gerado automaticamente na primeira execução).

README.md: Documentação do projeto.

👨‍💻 Desenvolvedora
Gleice Avelino Versão 1.0 - Alta Performance

📝 Notas de Versão
v1.0: Implementação de paginação, busca otimizada e exportação de PDF.