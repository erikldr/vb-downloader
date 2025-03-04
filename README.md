# VB Downloader

Um aplicativo para download automático do programa "A Voz do Brasil" para emissoras de rádio.

## Sobre o Projeto

O VB Downloader foi desenvolvido para automatizar o processo de download diário do programa "A Voz do Brasil", transmitido de segunda a sexta-feira. Este aplicativo é utilizado por várias emissoras de rádio em todo o Brasil para facilitar a retransmissão do programa obrigatório.

## Funcionalidades

- Download automático do programa "A Voz do Brasil" em dias úteis
- Tentativas em múltiplas fontes para garantir o sucesso do download
- Interface gráfica simples e intuitiva
- Personalização da pasta de destino e nome do arquivo
- Monitoramento contínuo com possibilidade de interrupção
- Registro detalhado de operações (logs)

## Como Usar

1. Inicie o aplicativo executando `python gui.py`
2. Selecione a pasta de destino para os arquivos baixados
3. Defina o nome do arquivo (opcional)
4. Clique em "Iniciar" para começar o monitoramento
5. O programa irá aguardar até às 20:20 em dias úteis para iniciar o download
6. O download será tentado até às 20:58, após esse horário o programa aguardará até o próximo dia útil

## Requisitos

- Python 3.6 ou superior
- Bibliotecas: requests, tkinter

## Instalação

```bash
# Clone o repositório ou baixe os arquivos
git clone https://github.com/seu-usuario/vb-downloader.git

# Instale as dependências
pip install -r requirements.txt
```

## Uso em Emissoras de Rádio

Este projeto é atualmente utilizado por diversas emissoras de rádio em todo o Brasil para automatizar o download e a retransmissão do programa "A Voz do Brasil", facilitando o cumprimento da obrigatoriedade de transmissão.

## Desenvolvedor

- **Erik Rocha** - e.lucasrocha@gmail.com

## Contribuições

Contribuições são bem-vindas! Se você encontrar bugs ou tiver sugestões de melhorias, por favor abra uma issue ou envie um pull request.

Para contribuições financeiras, utilize o PIX: e.lucasrocha@gmail.com
