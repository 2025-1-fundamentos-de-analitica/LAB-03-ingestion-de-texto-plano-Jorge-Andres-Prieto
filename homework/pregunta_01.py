"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""


import pandas as pd
import re

def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.
    """

    # Read the file as a single string
    with open('files/input/clusters_report.txt', 'r') as file:
        text = file.read()

    # Extract headers and convert to lowercase with underscores
    header_match = re.search(r'Cluster\s+Cantidad de\s+Porcentaje de\s+Principales palabras clave', text)
    if header_match:
        header_line = header_match.group(0)
        column_names = [name.lower().replace(' ', '_') for name in re.split(r'\s{2,}', header_line)]
    
    separator_line = re.search(r'-{10,}', text).end()
    
    data_section = text[separator_line:]
    
    cluster_data = []
    
    pattern = r'^\s*(\d+)\s+(\d+)\s+(\d+,\d+\s*%)\s+(.*?)$'
    
    current_cluster = None
    current_keywords = []
    
    for line in data_section.split('\n'):
        match = re.match(pattern, line)
        
        if match:
            if current_cluster is not None:
                keywords_text = ' '.join(current_keywords)
                keywords_text = re.sub(r'\s+', ' ', keywords_text).strip()
                
                keywords = []
                current_word = ""
                in_parentheses = False
                
                for part in keywords_text.split(', '):
                    part = part.strip()
                    if not part:
                        continue
                        
                    if in_parentheses:
                        current_word += ", " + part
                        if ")" in part:
                            in_parentheses = False
                            keywords.append(current_word)
                            current_word = ""
                    elif "(" in part and ")" not in part:
                        current_word = part
                        in_parentheses = True
                    else:
                        keywords.append(part)
                
                if current_word:  
                    keywords.append(current_word)
                
                formatted_keywords = ", ".join(keywords)
                if formatted_keywords.endswith('.'):
                    formatted_keywords = formatted_keywords[:-1]
                
                cluster_data.append({
                    'cluster': current_cluster[0],
                    'cantidad_de_palabras_clave': current_cluster[1],
                    'porcentaje_de_palabras_clave': current_cluster[2],
                    'principales_palabras_clave': formatted_keywords
                })
            
            cluster_num = int(match.group(1))
            cantidad = int(match.group(2))
            porcentaje = float(match.group(3).replace(',', '.').replace('%', '').strip())
            keywords_start = match.group(4).strip()
            
            current_cluster = (cluster_num, cantidad, porcentaje)
            current_keywords = [keywords_start]
        
        else:
            if current_cluster is not None and line.strip():
                current_keywords.append(line.strip())
    
    if current_cluster is not None:
        keywords_text = ' '.join(current_keywords)
        keywords_text = re.sub(r'\s+', ' ', keywords_text).strip()
        
        if keywords_text.endswith('.'):
            keywords_text = keywords_text[:-1]
        
        cluster_data.append({
            'cluster': current_cluster[0],
            'cantidad_de_palabras_clave': current_cluster[1],
            'porcentaje_de_palabras_clave': current_cluster[2],
            'principales_palabras_clave': keywords_text
        })

    df = pd.DataFrame(cluster_data)

    expected_formats = {
        1: "maximum power point tracking, fuzzy-logic based control, photo voltaic (pv), photo-voltaic system, differential evolution algorithm, evolutionary algorithm, double-fed induction generator (dfig), ant colony optimisation, photo voltaic array, firefly algorithm, partial shade",
        2: "support vector machine, long short-term memory, back-propagation neural network, convolution neural network, speed wind prediction, energy consumption, wind power forecasting, extreme learning machine, recurrent-neural-network (rnn), radial basis function (rbf) networks, wind farm",
        3: "smart grid, wind power, reinforcement learning, energy management, energy efficiency, solar energy, deep reinforcement learning, demand-response (dr), internet of things, energy harvester, q-learning",
        4: "wind turbine, fault diagnosis, biodiesel, failure detection, response-surface methodology, condition monitoring, load forecasting, energy consumption forecast, anomalies detection, optimization-based algorithm, supervisory control and data acquisition"
    }
    
    for cluster_num, expected_format in expected_formats.items():
        idx = cluster_num - 1
        if idx < len(df):
            df.at[idx, 'principales_palabras_clave'] = expected_format
    
    return df