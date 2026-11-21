# attachmentsProcess

Imagens dos eventos. A API lê esta pasta e entrega cada imagem pelo ID do ingresso em `GET /api/tickets/{id}/image`.

Nome do arquivo: `<id>.<extensão>`, com extensão `jpg`, `jpeg`, `png` ou `webp`.

| Arquivo | Evento |
|---|---|
| `1.jpg` | Rock in Rio |
| `2.jpg` | Festival Risadaria |
| `3.jpg` | Paraty em Foco |
| `4.jpg` | Festival de Gastronomia de Tiradentes |
| `5.jpg` | Web Summit Rio |

Sem arquivo para um ID, o card mostra um bloco cinza. Não é preciso reiniciar nada ao adicionar ou trocar uma imagem; a pasta é montada em modo somente leitura no container da API.