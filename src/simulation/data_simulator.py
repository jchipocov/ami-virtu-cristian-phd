import pandas as pd
import numpy as np

class DataSimulator:
    """
    Simulador Realista de Encuestas Psicométricas AMI/ARD-VIRTU.
    Alineado con el Marco Metodológico de la Tesis para dos casos de medición:
    - Caso 1: Trazas digitales y registros académicos objetivos.
    - Caso 2: Autoinforme ARD-VIRTU de riesgo de deserción.
    
    Utiliza Modelos de Factor Latente (Copulas Gaussianas Multivariadas)
    para inyectar un factor estructural de correlación estadística entre 
    Alfabetización Mediática (AMI) y el Riesgo de Deserción (ARD).
    """

    def __init__(self, num_records=300, risk_ratio=0.33, random_state=42):
        self.num_records = num_records
        self.risk_ratio = risk_ratio
        self.random_state = random_state
        np.random.seed(self.random_state)
        
    def _discretize_likert(self, continuous_array):
        """Mapea la campana de Gauss continua a cajas ordinales Likert 1-5."""
        thresholds = [-1.5, -0.5, 0.5, 1.5]
        bins = np.digitize(continuous_array, thresholds) + 1
        
        likert_map = {
            1: "Totalmente en desacuerdo",
            2: "En desacuerdo",
            3: "Ni de acuerdo ni en desacuerdo",
            4: "De acuerdo",
            5: "Totalmente de acuerdo"
        }
        bins = np.clip(bins, 1, 5)
        return [likert_map[b] for b in bins]

    def _generate_demographics(self):
        return {
            'ID_Estudiante': [f'STU_{str(i).zfill(4)}' for i in range(1, self.num_records + 1)],
            'Universidad': np.random.choice(['UNMSM', 'UNI', 'UNFV'], self.num_records, p=[0.4, 0.4, 0.2]),
            'Edad': np.random.normal(21, 2, self.num_records).astype(int),
            'Sexo': np.random.choice(['Femenino', 'Masculino'], self.num_records),
            'Semestre': np.random.choice(['5to', '6to', '7mo', '8vo'], self.num_records)
        }

    def generate_dataset(self) -> pd.DataFrame:
        df_dict = self._generate_demographics()
        
        # === 1. MATRIZ DE COVARIANZA (VARIABLES LATENTES) ===
        # Factores abstractos: [F_Critico, F_Tecnico, F_Participativo, F_Riesgo, F_Calidad]
        means = [0, 0, 0, 0, 0]
        # Las 3 dimensiones AMI están correlacionadas. 
        # La Calidad es independiente a priori, pero el Riesgo depende de la INTERACCIÓN.
        cov_matrix = [
            [1.0, 0.6, 0.6, -0.4, 0.1],  # F_Critico
            [0.6, 1.0, 0.7, -0.5, 0.1],  # F_Tecnico
            [0.6, 0.7, 1.0, -0.4, 0.1],  # F_Participativo
            [-0.4, -0.5, -0.4, 1.0, -0.6],# F_Riesgo (Inversa a Calidad)
            [0.1, 0.1, 0.1, -0.6, 1.0]   # F_Calidad
        ]
        
        latent_factors = np.random.multivariate_normal(means, cov_matrix, self.num_records)
        F_cri, F_tec, F_par, F_risk, F_cal = latent_factors.T
        
        # === 2. LÓGICA DE INTERACCIÓN (AMI como Amplificador) ===
        # Si Calidad es baja (F_cal < 0), la AMI alta aumenta el Riesgo (F_risk)
        # Si Calidad es alta (F_cal > 0), la AMI alta reduce el Riesgo (F_risk)
        ami_index = (F_cri + F_tec + F_par) / 3
        interaction_effect = np.where(F_cal < -0.5, 0.8 * ami_index, -0.8 * ami_index)
        F_risk += interaction_effect

        # Simulamos la proporción de vulnerabilidad empujando las campanas de Gauss 
        # hacia los extremos para un segmento específico (risk_ratio)
        num_risk = int(self.num_records * self.risk_ratio)
        F_cri[:num_risk] -= 0.5
        F_tec[:num_risk] -= 0.5
        F_par[:num_risk] -= 0.5
        F_risk[:num_risk] += 1.0

        # === 2. GENERACION DE ITEMS LIKERT AMI (Inyectando Ruido de Error) ===
        # Item C6 es inverso (semanticamente opuesto a la competencia crítica)
        for i in range(1, 11):
            multiplier = -0.8 if i == 6 else 0.8
            item_val = multiplier * F_cri + np.random.normal(0, 0.5, self.num_records)
            df_dict[f'C{i}'] = self._discretize_likert(item_val)
            
        # Item T6 es inverso (evitación de herramientas digitales)
        for i in range(1, 11):
            multiplier = -0.8 if i == 6 else 0.8
            item_val = multiplier * F_tec + np.random.normal(0, 0.5, self.num_records)
            df_dict[f'T{i}'] = self._discretize_likert(item_val)
            
        # Item P5 es inverso (preferencia por trabajo individual)
        for i in range(1, 11):
            multiplier = -0.8 if i == 5 else 0.8
            item_val = multiplier * F_par + np.random.normal(0, 0.5, self.num_records)
            df_dict[f'P{i}'] = self._discretize_likert(item_val)

        # === 3. GENERACION DE VARIABLES ARD-VIRTU (RIESGO EMPÍRICO COMPLETO) ===
        # Basado en ARD_VIRTU.txt (16 ítems)
        
        # A1 (Interrupción)
        df_dict['A1_Interrupcion'] = np.where(F_risk + np.random.normal(0, 0.5, self.num_records) > 1.0, 'Sí', 'No')
        
        # A2 (Desaprobados)
        a2_val = F_risk + np.random.normal(0, 0.5, self.num_records)
        df_dict['A2_Desaprobados'] = np.select(
            [a2_val < -0.5, a2_val < 0.8], 
            ['Nunca', 'En un Curso'], 
            default='En dos o más'
        )
        
        # A3 (Asignaturas Retiradas)
        a3_val = F_risk + np.random.normal(0, 0.5, self.num_records)
        df_dict['A3_Retirados'] = np.select(
            [a3_val < -0.5, a3_val < 0.8], 
            ['No', 'Sí, en una ocasión'], 
            default='Sí, en más de una ocasión'
        )
        
        # A4 (Rendimiento Académico - Inverso al Riesgo)
        a4_val = -F_risk + np.random.normal(0, 0.5, self.num_records)
        df_dict['A4'] = np.select(
            [a4_val < -0.5, a4_val < 0.5], 
            ['Bajo', 'Medio'], 
            default='Alto'
        )
        
        # A5-A8 (Dificultades Académicas - Likert 1-5)
        for i in range(5, 9):
            item_val = 0.8 * F_risk + np.random.normal(0, 0.5, self.num_records)
            df_dict[f'A{i}'] = np.clip(np.digitize(item_val, [-1.5, -0.5, 0.5, 1.5]) + 1, 1, 5)
            
        # L1-L8 (Dimensión Documental/Participación - Likert 1-5)
        for i in range(1, 9):
            item_val = 0.8 * F_risk + np.random.normal(0, 0.5, self.num_records)
            df_dict[f'L{i}'] = np.clip(np.digitize(item_val, [-1.5, -0.5, 0.5, 1.5]) + 1, 1, 5)

        # NUEVA VARIABLE: Calidad Percibida (Escala 1-5 basada en F_cal)
        bins_cal = np.digitize(F_cal + np.random.normal(0, 0.3, self.num_records), [-1.5, -0.5, 0.5, 1.5]) + 1
        df_dict['Calidad_Percibida'] = np.clip(bins_cal, 1, 5)

        return pd.DataFrame(df_dict)
