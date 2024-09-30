# Bem-vindo ao aplicativo de fusão espacial!

Antes de tudo, verifique meu repositório GitHub para mais informações e/ou sugestões: **<https://github.com/VYR4L/Sensoriamento-Remoto>**

## Agora, para o tutorial:

1. Se você já baixou as imagens, pule ao passo 4. Caso deseje baixar imagens do CBERS, vá ao passo 2. Caso deseje baixar imagens do Landsat, passo 4.

2. Clique no botão "Baixar CBERS". Você vai precisar:
    * e-mail do seu cadastro em **<http://dgi.inpe.br/catalogo/explore>**;
    * Inserir a área de interesse (BBox) (em decimal, separados por virgula, exemplo: -97.1221, 43.0109, -96.9868, 43.0565).
    * Inserir a data inicial da busca das imagens;
    * Inserir a data final de busca das imagens;
    * Inserir a porcentagem máxima de nuvens;
    * Inserir o limite de datasets;
    * Clicar em "Carregar Imagens";
    * Nesse momento, os possíveis datasets serão carregados, espere até que eles apareçam;
    * Selecionar seu dataset dentre os listados. Sugestão: utilize o site do INPE para verificar se a área escolhida está dentro de todas as bandas do dataset;
    * Clicar em "Selecione o Diretório de Saída" e escolha o diretório em que deseja salvar as imagens;
    * Clicar em "Baixar Imagens". Elas serão salvas diretamente no seu computador.

3. Diferentemente das imagens do Landsat, as do CBERS não vem recortadas na área de interesse. Para isso, você deve clicar em "Recortar Imagem". Você vai precisar:
    * Selecionar a imagem a ser recortada;
    * Selecionar o diretório onde a imagem recortada será salva;
    * Inserir um novo nome para a imagem recortada;
    * Inserir a Longitude mínima, Latitude mínima, Longitude máxima, Latitude máxima;
    * Clicar em recortar. Dependendo da banda pode levar algum tempo, espere o processo terminar!

4. Clique no botão "Baixar Landsat". Você vai precisar:
    * Habilitar sua API do Google Earth Engine, você pode fazer isso em **<https://console.cloud.google.com/apis/library>**;
    * Informar o nome do seu projeto;
    * Informar o diretório do Google Drive em que deseja salvar as imagens;
    * Inserir o ID do satélite. Você pode redimensionar e obter uma fatia melhor do terreno em **<https://earthexplorer.usgs.gov/>**
    * Inserir a área de interesse (em decimal, separados por virgula, exemplo: -97.1221, 43.0109, -96.9868, 43.0565).

5. Escolha um diretório onde a imagem fusionada será criada clicando em "Selecione o diretório de saída".

6. Você precisará importar 2 imagens caso utilize o download do landsat: uma para a imagem multiespectral (bandas 1 a 4) e uma para a banda pancromática (banda 8). Já para o CBERS, será necessário importar os arquivos de bandas individuais (Azul, Verde, Vermelha, Infravermelho-próxima, Pancromática).

7. Selecione o método de fusão que você desejar e clique nele, pode ser que demore um pouco, portanto espere a conclusão da fusão.

É isso, você está pronto para usar o aplicativo!