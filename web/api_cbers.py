from datetime import date


def get_images(api, bbox, initial_date, final_date, cloud=0, limit=0):
    '''
    Método para buscar imagens CBERS4A disponíveis em uma determinada área de interesse e período de tempo.

    :param api: Instância da classe API do CBERS4A.
    :param bbox: Bounding box da área de interesse no formato (min_lon, min_lat, max_lon, max_lat).
    :param initial_date: Data inicial no formato (ano, mês, dia).
    :param final_date: Data final no formato (ano, mês, dia).
    :param cloud: Cobertura de nuvens máxima permitida (em %).
    :param limit: Número máximo de imagens a serem retornadas.
    '''


    # Convertendo tuplas de datas em objetos date, caso sejam passadas como tupla
    if isinstance(initial_date, tuple):
        initial_date = date(*initial_date)
    if isinstance(final_date, tuple):
        final_date = date(*final_date)

    # Download das imagens
    query = api.query(location=bbox,
                      initial_date=initial_date,
                      end_date=final_date,
                      cloud=cloud,
                      limit=limit,
                      collections=['CBERS4A_WPM_L2_DN', 'CBERS4A_WPM_L4_DN'],)

    # Retornando uma lista de tuplas (scene_id, coleção)
    scene_info = [(feature['id'], feature['collection']) for feature in query['features']]
    return scene_info



def download_cbers(api, scene, output_folder):
    '''
    Baixa uma imagem CBERS4A a partir de um scene_id e coleção.

    :param api: Instância da classe API do CBERS4A.
    :param scene: Scene ID da imagem CBERS4A.
    :param output_folder: Pasta onde a imagem será salva.
    '''
    try:
        scene, collection_image = scene.split(' - ')
        if collection_image == 'L2':
            product = api.query_by_id(scene_id=scene, collection='CBERS4A_WPM_L2_DN')
            api.download(product,
                        bands=['blue', 'green', 'red', 'nir', 'pan'],
                        threads=5,
                        outdir=output_folder)
        elif collection_image == 'L4':
            product = api.query_by_id(scene_id=scene, collection='CBERS4A_WPM_L4_DN')
            api.download(product,
                        bands=['blue', 'green', 'red', 'nir', 'pan'],
                        threads=5,
                        outdir=output_folder)
    except Exception as e:
        raise Exception(f"Error while downloading CBERS4A product: {e}")
    
         

